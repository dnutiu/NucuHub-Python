from nucuhub.monitoring import internals


class MockConsumerStage(internals.ConsumerStage):
    name = "mock consumer stage"

    def __init__(self):
        super(MockConsumerStage, self).__init__()
        self.processed = False

    def process(self, message):
        self.processed = True
        return True


class MockConsumerStageException(internals.ConsumerStage):
    name = "mock consumer stage ex"

    def process(self, message):
        raise ValueError("This is an intentional exception.")
