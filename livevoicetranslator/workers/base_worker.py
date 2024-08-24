# livevoicetranslator/workers/base_worker.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Worker(ABC, Generic[T]):
    def __init__(self, input_queue=None, output_queue=None):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self._running = False

    @abstractmethod
    async def processed(self) -> T:
        pass

    def before_start(self):
        pass

    def after_stop(self):
        pass

    async def start(self):
        self._running = True
        print("Start " + self.__class__.__name__)
        self.before_start()
        while self._running:
            result_item = await self.processed()
            if result_item != None and result_item:
                await self.output_queue.put(result_item)
        self.after_stop()

    def stop(self):
        print("Stop " + self.__class__.__name__)
        self._running = False
