import mido
import numpy as np
import sounddevice
import threading


class MidiHandler:
    def __init__(self, input_device, listen_on, status_out):
        self.midi_in = mido.open_input(input_device)
        self.listen_on = listen_on[:]
        self.status_array = np.zeros(len(self.listen_on))
        self.status_out = status_out

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
            print(msg)
            self.update_status_array(msg)
            self.status_out[:] = self.status_array


class AudioHandler:
    status_in = None

    def __init__(self, device, status_in, event_terminate):
        channels = len(status_in)
        assert channels < 8
        if AudioHandler.status_in is None:
            AudioHandler.status_in = status_in
        self.sounddevice = sounddevice.OutputStream(
            samplerate=48000,
            blocksize=64,
            channels=channels,
            device=device,
            callback=self.callback,
            finished_callback=self.finished_callback
        )
        self.event_terminate = event_terminate

    @staticmethod
    def create_block(frames):
        # print(AudioHandler.status_in)
        channels = len(AudioHandler.status_in)
        block = np.ones((frames, channels)) * AudioHandler.status_in
        return block

    @staticmethod
    def callback(outdata, frames, time, status):
        block = AudioHandler.create_block(frames)
        outdata[:] = block*0.5

    @staticmethod
    def finished_callback():
        print("executing finished_callback")
        pass

    def run(self):
        with self.sounddevice:
            self.event_terminate.wait()


if __name__ == "__main__":
    event_terminate_audio = threading.Event()
    listen_on = [60, 61]
    status = np.zeros(len(listen_on))

    def midi_thread(status):
        handler = MidiHandler('Driver IAC Bus 1', listen_on, status)
        handler.run()

    def audio_thread(status, event_terminate):
        handler = AudioHandler('ES-8', status, event_terminate)
        handler.run()

    m_t = threading.Thread(target=midi_thread, args=(status,), daemon=True)
    a_t = threading.Thread(target=audio_thread, args=(status, event_terminate_audio))
    print(status)
    m_t.start()
    a_t.start()

    try:
        a_t.join()
    except KeyboardInterrupt:
        event_terminate_audio.set()

    print("Terminating...")
    a_t.join()
