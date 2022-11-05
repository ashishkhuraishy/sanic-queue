from __future__ import annotations
from asyncio import Queue

from abc import ABC, abstractmethod

class QueueType(ABC):
    """
        all the items that need to be 
        queued should be a subtype of 
        this class and should implement
        all the methods
    """
    @abstractmethod
    def run(self):
        pass

class TaskQueue(object):
    __slots__ = ("work_queue")

    def __init__(self):
        # The queue implements multi-producer, multi-consumer queues.
        self.work_queue: Queue[QueueType] = Queue()

    @property
    def qsize(self):
        return self.work_queue.qsize()

    @property
    def empty(self):
        return self.work_queue.empty()

    async def acquire_work(self):
        """
        Get a work object from the work queue
        """
        while True:
            try:
                task = await self.work_queue.get()
                await task.run()

            except Exception as e:
                print(f"error happened while processing item on queue\n{e}")

    async def deposit_work(self, task: QueueType) -> bool:
        """
        Add a work object to the work queue
        """
        try:
            await self.work_queue.put(task)
            return True
        except Exception as e:
            print(f"error happened while adding to queue - {e}")
        
        return False


    