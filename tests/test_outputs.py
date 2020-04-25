import mido
import pytest

from cvpy.outputs import Outputs
from cvpy.outputs.types import NoteOutput, GateOutput, CvOutput

from mido.messages.messages import Message


@pytest.fixture
def outputs():
    return Outputs([NoteOutput(0), GateOutput(1, 72), CvOutput(0, 2)])


def make_note_on_message(channel, note):
    return Message.from_dict({'type': 'note_on',
                              'time': 0,
                              'note': note,
                              'velocity': 60,
                              'channel': channel})


def make_cc_message(channel, control):
    return Message.from_dict({'type': 'control_change',
                              'time': 0,
                              'control': control,
                              'value': 64,
                              'channel': channel})


def test_relevant_msg(outputs):
    note_on_messages = [make_note_on_message(0, n) for n in [0, 64, 127]]
    note_on_messages.append(make_note_on_message(1, 72))

    for m in note_on_messages:
        assert outputs.filter(m)

    cc_messages = [make_cc_message(0, 2)]

    for m in cc_messages:
        assert outputs.filter(m)


def test_non_relevant_msg(outputs):
    note_on_messages = [make_note_on_message(1, n) for n in [0, 64, 127]]

    for m in note_on_messages:
        assert not outputs.filter(m)

    cc_messages = [make_cc_message(0, n) for n in [0, 64, 127]]

    for m in cc_messages:
        assert not outputs.filter(m)


def test_output_update(outputs):
    note_message = make_note_on_message(0, 64)
    outputs.update(note_message)

    assert outputs.outputs[0].output_status[0] == 0.5
    assert outputs.outputs[0].output_status[1] == 0.8

    assert outputs.outputs[1].output_status[0] == 0

    gate_message = make_note_on_message(1, 72)
    outputs.update(gate_message)

    assert outputs.outputs[0].output_status[0] == 0.5
    assert outputs.outputs[0].output_status[1] == 0.8

    assert outputs.outputs[1].output_status[0] == 1

    cc_message = make_cc_message(0, 2)
    outputs.update(cc_message)

    assert outputs.outputs[2].output_status[0] == 0.5
