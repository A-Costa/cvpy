import numpy as np
from .types import BaseOutput


class Outputs:
    def __init__(self, outputs: list):
        self.output_needed = 0
        self.listening = dict()
        for output in outputs:
            assert isinstance(output, BaseOutput)
            self.output_needed += output.output_used

            output_channel = output.listen_on['channel']

            if output_channel not in self.listening:
                self.listening[output_channel] = {'note': set(),
                                                  'control': set()}

            for note in output.listen_on['note']:
                assert note not in self.listening[output_channel]['note']
                self.listening[output_channel]['note'].add(note)

            for control in output.listen_on['control']:
                assert control not in self.listening[output_channel]['control']
                self.listening[output_channel]['control'].add(control)

        assert self.output_needed <= 8

        self.outputs = outputs[:]
        self.output_status = np.zeros(self.output_needed)

    def filter(self, msg):
        if msg.channel in self.listening:
            if msg.type in ['note_on', 'note_off']:
                return msg.note in self.listening[msg.channel]['note']
            elif msg.type == 'control_change':
                return msg.control in self.listening[msg.channel]['control']
            else:
                return False
        else:
            return False

    def update(self, msg):
        if self.filter(msg):
            for output in self.outputs:
                updated = output.update(msg)
                if updated:
                    break
        else:
            pass
