import mido
import numpy as np


class MidiHandler:
    def __init__(self, input_device, listen_on):
        self.midi_in = mido.open_input(input_device)
        self.listen_on = listen_on[:]
        self.status_array = np.zeros(len(self.listen_on))

    def get_status(self, index=None):
        if not index:
            return self.note_status
        else:
            return self.note_status[index]

    def update_status(self, note, value):
        if note in self.listen_on:
            index = self.listen_on.index(note)
            self.status_array[index] = value

    def update_status_array(self, midi_message):
        if midi_message.type == 'note_on':
            self.update_status(midi_message.note, 1)
        if midi_message.type == 'note_off':
            self.update_status(midi_message.note, 0)

    def run(self):
        for msg in self.midi_in:
            self.update_status_array(msg)
