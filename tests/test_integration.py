import numpy as np
import pytest
import threading


from cvpy.handlers import AudioHandler, MidiHandler
from cvpy.outputs import Outputs
from cvpy.outputs.types import NoteOutput, GateOutput, CvOutput

from mido.messages.messages import Message


@pytest.fixture
def event_terminate():
    return threading.Event()


@pytest.fixture
def outputs():
    return Outputs([NoteOutput(0), GateOutput(1, 72), CvOutput(0, 2)])


@pytest.fixture
def audio_handler(outputs, event_terminate):
    return AudioHandler('Soundflower (64ch)', outputs, event_terminate)


@pytest.fixture
def midi_handler(outputs):
    return MidiHandler('Driver IAC Bus 1', outputs)


def make_note_on_message(channel, note):
    return Message.from_dict({'type': 'note_on',
                              'time': 0,
                              'note': note,
                              'velocity': 60,
                              'channel': channel})


def test_audio_handler(audio_handler, outputs):
    m = make_note_on_message(0, 64)
    outputs.update(m)

    assert outputs.output_needed == 4
    assert len(outputs.output_status) == 4

    assert (outputs.output_status == np.array([0.5, 0.8, 0, 0])).all()
    # assert outputs.output_status[0] == 0.5

    block = audio_handler.create_block(64)
    assert block.shape == (64, 4)
    assert (block[0] == np.array([0.5, 0.8, 0, 0])).all()
