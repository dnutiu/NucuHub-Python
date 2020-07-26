import concurrent.futures
import queue
import signal
import time
import traceback
import typing

from nucuhub import logging

from nucuhub.monitoring import (  # isort:skip
    ConsumerStage,
    infrastructure,
    internals,
    workflows,
)


class MonitoringMain:
    def __init__(self):
        self.message_broker = infrastructure.Messaging()
        self.logger = logging.get_logger("MonitoringLogger")
        self.sleep_time = 10

        self._shared_queue = queue.Queue(maxsize=100)
        self.monitoring_topics = None
        self.monitoring_stages = None
        self._consumer_loop_is_running = True
        self._producer_loop_in_running = True
        self._main_loop_is_running = True
        self._producer = None
        self._consumer = None

    def add_topics(self, topics: typing.List[str]):
        """
            Initializes the topics of interest that will be monitored.
        :param topics: A list of strings representing topics
        """
        self.monitoring_topics = topics

    def add_stages_workflow(self, stages: typing.List[ConsumerStage]):
        """
            Add the stages workflow for the monitoring process.
        :param stages: A list of ConsumerStage objects.
        """
        self.monitoring_stages = stages

    def _producer_work_loop(self):
        self.producer = internals.Producer(self._shared_queue)
        self.logger.debug(f"Monitoring topics: {self.monitoring_topics}")
        self.producer.set_topics(self.monitoring_topics)
        self.producer.loop_forever()

    def _consumer_work_loop(self):
        self._consumer = internals.Consumer(self._shared_queue)
        for stage in self.monitoring_stages:
            self.logger.debug(f"Loading consumer workflow stage: {stage}")
            self._consumer.add_stage(stage)
        self._consumer.loop_forever()

    # noinspection DuplicatedCode
    def loop_forever(self):
        """
            Starts the monitoring process.
        """
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGTSTP, self.shutdown)
        self.logger.info("Looping forever!")

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            producer_loop = executor.submit(self._producer_work_loop)
            consumer_loop = executor.submit(self._consumer_work_loop)
            while self._main_loop_is_running:
                try:
                    if not producer_loop.running() and self._main_loop_is_running:
                        producer_loop.cancel()
                        exception_tb = "".join(
                            traceback.TracebackException.from_exception(
                                producer_loop.exception(timeout=2)
                            ).format()
                        )
                        self.logger.warning(
                            f"restarting producer_loop because it's not running! Err: {exception_tb}"
                        )
                        producer_loop = executor.submit(self._producer_work_loop)
                        time.sleep(2)
                    if not consumer_loop.running() and self._main_loop_is_running:
                        consumer_loop.cancel()
                        exception_tb = "".join(
                            traceback.TracebackException.from_exception(
                                consumer_loop.exception(timeout=2)
                            ).format()
                        )
                        self.logger.warning(
                            f"restarting consumer_loop because it's not running! Err: {exception_tb}"
                        )
                        consumer_loop = executor.submit(self._consumer_work_loop)
                        time.sleep(2)
                except concurrent.futures.CancelledError as e:
                    # We get a canceled error when we cancel tasks.
                    self.logger.warning(e)
                time.sleep(self.sleep_time)

    def shutdown(self, signum, frame):
        """
            Stops the monitoring worker.
        """
        self.logger.info("Shutting down... waiting for loops to finish work.")
        self._consumer_loop_is_running = False
        self._producer_loop_in_running = False
        self._main_loop_is_running = False
        if self.producer:
            self.producer.shutdown()
        if self._consumer:
            self._consumer.shutdown()


def main():
    monitoring = MonitoringMain()
    monitoring.add_topics(["sensors"])
    monitoring.add_stages_workflow([workflows.SensorsWorkflow()])
    monitoring.loop_forever()


if __name__ == "__main__":
    main()
