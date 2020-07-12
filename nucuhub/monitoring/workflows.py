from nucuhub.monitoring import ConsumerStage


class PrintWorkflow(ConsumerStage):
    name = "PrintWorkflow"

    def process(self, message):
        print(message)
