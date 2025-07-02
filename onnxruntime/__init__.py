class InferenceSession:
    def __init__(self, *args, **kwargs):
        pass

    def get_inputs(self):
        class Dummy:
            name = "input"
        return [Dummy()]

    def run(self, *args, **kwargs):
        import numpy as np
        return [np.zeros((1, 128), dtype=np.float32)]
