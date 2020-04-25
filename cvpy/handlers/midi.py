import mido

from cvpy.outputs import Outputs


class MidiHandler:
    def __init__(self, input_device: str, outputs: Outputs):
        self.midi_in = mido.open_input(input_device)
        self.outputs = outputs

    def run(self):
        for msg in self.midi_in:
            print(msg)
            self.outputs.update(msg)
