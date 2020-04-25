import numpy as np
import sounddevice
import threading

from cvpy.outputs import Outputs


class AudioHandler:
    def __init__(self, device: str, outputs: Outputs,
                 event_terminate: threading.Event):

        self.channels = outputs.output_needed

        self.sounddevice = sounddevice.OutputStream(
            samplerate=48000,
            blocksize=64,
            channels=self.channels,
            device=device,
            callback=self.callback,
            finished_callback=self.finished_callback
        )

        self.outputs = outputs
        self.event_terminate = event_terminate

    def create_block(self, frames):
        # print(AudioHandler.status_in)
        block = np.ones((frames, self.channels)) * self.outputs.get_status()
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
