# livevoicetranslator/controllers/main_controller.py
import asyncio

from livevoicetranslator.workers import RawAudioProducerWorker, VoiceTranscriptorWorker, TextTranslatorWorker, \
    VoiceoverWorker


class MainController:
    def __init__(self):
        SOURCE_LANGUAGE = "en"
        TRANSLATE_RULES = {
            'ru': 'en',
            'en': 'ru',
            'pl': 'ru'
        }
        self.raw_audio_queue = asyncio.Queue()
        self.transcripted_text_queue = asyncio.Queue()
        self.translated_text_queue = asyncio.Queue()

        self.audio_producer = RawAudioProducerWorker(chunk_duration=1, output_queue=self.raw_audio_queue)
        self.voice_transcriptor = VoiceTranscriptorWorker(
            model_name="large-v3",
            download_root="../resources/models",
            language=SOURCE_LANGUAGE,
            input_queue=self.raw_audio_queue,
            output_queue=self.transcripted_text_queue
        )
        self.text_translator = TextTranslatorWorker(
            translate_map=TRANSLATE_RULES,
            source_language=SOURCE_LANGUAGE,
            input_queue=self.transcripted_text_queue,
            output_queue=self.translated_text_queue
        )
        self.voiceover_worker = VoiceoverWorker(
            input_queue=self.translated_text_queue,
            language=TRANSLATE_RULES[SOURCE_LANGUAGE],
            voices_dir='resources/voices',
            voices_map={
                #'ru': 'ru_RU-ruslan-medium.onnx',
                'ru': 'ru_RU-irina-medium.onnx',
                'en': 'en_GB-jenny_dioco-medium.onnx',
                'pl': 'pl_PL-gosia-medium.onnx'
            }
        )

    async def run(self):
        producer_task = asyncio.create_task(self.audio_producer.start())
        transcriptor_task = asyncio.create_task(self.voice_transcriptor.start())
        translator_task = asyncio.create_task(self.text_translator.start())
        voiceover_task = asyncio.create_task(self.voiceover_worker.start())

        try:
            L = await asyncio.gather(producer_task, transcriptor_task, translator_task, voiceover_task)
            print(L)
        except Exception as e:
            raise
        finally:
            self.audio_producer.stop()
            self.voice_transcriptor.stop()
            self.text_translator.stop()
            self.voiceover_worker.stop()
