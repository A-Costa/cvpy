import mido
import numpy as np


class BaseOutput:
    def __init__(self, output_used):
        self.output_used = output_used
        self.output_status = np.zeros(output_used)
        self.listen_on = dict()

    def is_relevant(self, msg):
        assert isinstance(msg, mido.messages.messages.Message)
        check_channel = msg.channel == self.listen_on['channel']
        if msg.type in ['note_on', 'note_off']:
            check_message = msg.note in self.listen_on['note']
        elif msg.type == 'control_change':
            check_message = msg.control in self.listen_on['control']
        else:
            check_message = False

        return check_channel and check_message


class NoteOutput(BaseOutput):
    def __init__(self, channel):
        super().__init__(2)
        self.listen_on = {'channel': channel, 'note': set(range(128)), 'control': {}}

    def update(self, msg):
        if self.is_relevant(msg):
            if msg.type == 'note_on':
                self.output_status[0] = msg.note/128
                self.output_status[1] = 0.8
            elif msg.type == 'note_off':
                self.output_status[0] = msg.note/128
                self.output_status[1] = 0
            return True
        else:
            return False


class GateOutput(BaseOutput):
    def __init__(self, channel, note):
        super().__init__(1)
        self.listen_on = {'channel': channel, 'note': {note}, 'control': {}}

    def update(self, msg):
        if self.is_relevant(msg):
            if msg.type == 'note_on':
                self.output_status[0] = 1
            elif msg.type == 'note_off':
                self.output_status[0] = 0
            return True
        else:
            return False


class CvOutput(BaseOutput):
    def __init__(self, channel, control_change):
        super().__init__(1)
        self.listen_on = {'channel': channel, 'note': {}, 'control': {control_change}}

    def update(self, msg):
        if self.is_relevant(msg):
            if msg.type == 'control_change':
                self.output_status[0] = msg.value/128
            return True
        else:
            return False
