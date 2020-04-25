import numpy as np
import sounddevice


class AudioHandler:
    def __init__(self, device, status_in, event_terminate):
        channels = len(status_in)
        assert channels < 8
        self.sounddevice = sounddevice.OutputStream(
            samplerate=48000,
            blocksize=64,
            channels=channels,
            device=device,
            callback=self.callback,
            finished_callback=self.finished_callback
        )
        self.status_in = status_in
        self.event_terminate = event_terminate

    def create_block(self, frames):
        # print(AudioHandler.status_in)
        channels = len(self.status_in)
        block = np.ones((frames, channels)) * self.status_in
        return block

    def callback(*args):
        self = args[0]
        outdata = args[1]
        frames = args[2]
        # time = args[3]
        # status = args[4]
        block = self.create_block(frames)
        outdata[:] = block*0.5

    def finished_callback(*args):
        print("Executing finished_callback")
        pass

    def run(self):
        with self.sounddevice:
            self.event_terminate.wait()
