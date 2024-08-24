# src/workers/voice_transcriptor_worker.py
from .base_worker import Worker
from faster_whisper import WhisperModel
import numpy as np

class VoiceTranscriptorWorker(Worker[str]):
    def __init__(self, model_name, download_root, language, **kwargs):
        super().__init__(**kwargs)
        self.model = WhisperModel(model_name,
                                  device="cuda",
                                  compute_type="float16",
                                  # device_index=0,
                                  download_root=download_root)
        self.min_silence_duration_ms = 100
        self.vad_filter = True
        self.beam_size = 5
        self.language = language
        self.latest_ignored_message = None

    async def processed(self):
        raw_audio_data = await self.pull_all_data()
        segments, info = self.model.transcribe(
            np.frombuffer(raw_audio_data, np.int16).astype(np.float32) / 255.0,
            language=self.language,
            beam_size=self.beam_size,
            vad_filter=self.vad_filter,
            vad_parameters=dict(min_silence_duration_ms=self.min_silence_duration_ms)
        )
        segmentsText = " ".join([s.text for s in segments])
        # if model return text "To be continued..." ignore and try convert again
        if segmentsText.endswith("..."):
            if self.latest_ignored_message != segmentsText:
                self.latest_ignored_message = segmentsText
                await self.input_queue.put(raw_audio_data)
            print("[IGNORE:"+segmentsText+"]")
            return None

        return segmentsText


    async def pull_all_data(self):
        combined_bytes = bytearray()
        while True:
            data = await self.input_queue.get()
            combined_bytes.extend(data)
            if self.input_queue.qsize() == 0:
                break
        return bytes(combined_bytes)