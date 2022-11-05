import asyncio, random

from sanic import Sanic
from sanic.response import text
from sanic.request import Request

from myqueue import QueueType, TaskQueue

app = Sanic("MyHelloWorldApp")

class MyTaskClass(QueueType):
    """
        Converted my task function to a class which extends
        the queue type and implemeneted the run function with
        the necessary updates
    """
    def __init__(self, task_name : str) -> None:
        self.task_name = task_name
        super().__init__()

    async def run(self):
        await self.my_long_task()

    async def my_long_task(self) -> None:
        seconds = random.randint(5, 15)
        print(f"{self.task_name} is going to run for {seconds} seconds")
        await asyncio.sleep(seconds)
        print(f"{self.task_name} is done")

@app.listener("after_server_start")
async def init_queue(app: Sanic, loop):
    app.queue = TaskQueue() 

    # start worker queue on the background
    app.add_task(app.queue.acquire_work())



@app.get("/")
async def hello_world(request : Request):
    task_name = request.args.get("name", "default_task")

    task = MyTaskClass(task_name=task_name)
    status = await request.app.queue.deposit_work(task)
    return text(f"Hello, world. - {task_name} : {status}")

if __name__ == "__main__" :
    app.run(port=8000)