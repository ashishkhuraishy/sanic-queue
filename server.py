import asyncio, random

from sanic import Sanic
from sanic.response import text
from sanic.request import Request

app = Sanic("MyHelloWorldApp")

async def my_long_task(task_name : str) -> None:
    seconds = random.randint(5, 15)
    print(f"{task_name} is going to run for {seconds} seconds")
    await asyncio.sleep(seconds)

@app.get("/")
async def hello_world(request : Request):
    task_name = request.args.get("name", "default_task")

    await my_long_task(task_name)
    return text(f"Hello, world. - {task_name}")

if __name__ == "__main__" :
    app.run(port=8000)