import mido
import numpy as np

from cvpy.outputs import Outputs


class MidiHandler:
    def __init__(self, input_device: str, outputs: Outputs):
        self.midi_in = mido.open_input(input_device)
        self.outputs = outputs

    def run(self):
        for msg in self.midi_in:
            print(dir(msg))
            print(msg.dict())
            print(type(msg))
            # self.outputs.update(msg)


"""
    def update_status(self, note, value):
        if note in self.listen_on:
            index = self.listen_on.index(note)
            self.status_array[index] = value

    def update_status_array(self, midi_message):
        if midi_message.type == 'note_on':
            self.update_status(midi_message.note, 1)
        if midi_message.type == 'note_off':
            self.update_status(midi_message.note, 0)
"""
