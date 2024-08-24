# src/workers/voiceover_worker.py
from http.cookiejar import month

from .base_worker import Worker
import os
import sounddevice as sd
import subprocess
import numpy as np
import piper

class VoiceoverWorker(Worker):
    def __init__(self, language, voices_dir, voices_map, rate=22050, **kwargs):
        super().__init__(**kwargs)
        self.language = language
        self.rate = rate
        self.voices_dir = voices_dir
        self.voices_map = voices_map

    async def processed(self):
        text = await self.full_input_text()
        print(text, end=" ")
        model_path = os.path.join(self.get_project_root(), self.voices_dir, self.voices_map[self.language])
        command = [
            "piper",
            "--model",
            model_path,
            "--output_raw",
            # "--cuda"
        ]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output, _ = process.communicate(input=text.encode('utf-8'))
        audio_np = np.frombuffer(output, dtype=np.int16)
        sd.play(audio_np, samplerate=self.rate)
        sd.wait()

    async def full_input_text(self):
        combined_string = ""
        while True:
            combined_string += await self.input_queue.get()
            if self.input_queue.qsize() == 0:
                break
        return combined_string

    def get_project_root(self):
        python_path = os.getenv('PYTHONPATH', '')
        if python_path:
            return os.path.abspath(python_path.split(os.pathsep)[0])
        return os.path.dirname(__file__)
