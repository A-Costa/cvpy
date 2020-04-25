import numpy as np
from .types import BaseOutput


class Outputs:
    def __init__(self, outputs: list):
        self.output_needed = 0
        self.outputs = outputs[:]
        for output in outputs:
            assert isinstance(output, BaseOutput)
            self.output_needed += output.output_used
        self.output_status = np.zeros(self.output_needed)

    def filter(self, msg):
        return any([output.is_relevant(msg) for output in self.outputs])

    def update(self, msg):
        if self.filter(msg):
            for output in self.outputs:
                updated = output.update(msg)
                if updated:
                    break
        else:
            pass
