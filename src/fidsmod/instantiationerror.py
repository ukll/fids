class InstantiationError(Exception):
    def __init__(self, message="InstantiationError: object could not be instantiated"):
        self.message = message