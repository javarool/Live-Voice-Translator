# src/workers/raw_audio_producer_worker.py
from .base_worker import Worker
import pyaudio
import asyncio

class RawAudioProducerWorker(Worker[bytearray]):
    def __init__(self, chunk_duration, **kwargs):
        super().__init__(**kwargs)
        self.chunk_duration = chunk_duration # sec
        self.sample_rate = 16000 #Hz
        self.chunk_size = int(self.sample_rate * self.chunk_duration)
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.p = pyaudio.PyAudio()
        self.device_index = self.p.get_default_input_device_info()['index']
        self.stream = None

    def before_start(self):
        self.stream = self.p.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=self.chunk_size
        )

    def after_stop(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.p.terminate()

    async def processed(self):
        if self.stream is None:
            raise RuntimeError("Audio stream is not started.")
        audio_chunk = await asyncio.to_thread(self.stream.read, self.chunk_size)
        return audio_chunk
        # if (len(list(filter(lambda x: x != 0, audio_chunk))) > 0):
        #     return audio_chunk
        # else:
        #     return None




