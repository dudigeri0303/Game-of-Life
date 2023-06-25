class Scenehandler:
    def __init__(self, method, running):
        self.method = method
        self.running = running

    def call_method(self):
        self.method()