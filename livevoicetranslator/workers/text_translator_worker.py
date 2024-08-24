# src/workers/text_translator_worker.py
from .base_worker import Worker
from libretranslatepy import LibreTranslateAPI
import re

class TextTranslatorWorker(Worker[str]):
    def __init__(self, translate_map, source_language="en", api_url = "http://localhost:5000", **kwargs):
        super().__init__(**kwargs)
        self.source_language = source_language
        self.translate_map = translate_map
        self.translator_client = LibreTranslateAPI(api_url)

    def before_start(self):
        self.translator_client.translate("Test translate", "en", "ru")

    async def processed(self):
        input_text = await self.full_input_text()

        return  self.translator_client.translate(input_text, self.source_language, self.translate_map[self.source_language])
        # if not re.search(r'[;!?]', translated_text):
        #     await self.input_queue.put(input_text)
        #     return None
        # return translated_text


    async def full_input_text(self):
        combined_string = ""
        while True:
            combined_string += await self.input_queue.get()
            if len(combined_string) > 90:
                break
            if combined_string and combined_string.endswith(('.', '?', '!', ';')):
            # if self.input_queue.qsize() == 0:
                break
        return combined_string

