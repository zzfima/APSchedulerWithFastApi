import asyncio
import threading
import time

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from starlette import status
from starlette.responses import Response

threads_names = set()
app = FastAPI()
scheduler = BackgroundScheduler()
# scheduler = AsyncIOScheduler()

print(scheduler.state)


@app.get("/start_scheduler")
async def start_scheduler():
    print('Run scheduler')
    scheduler.start()
    print(scheduler.state)
    return Response('Started', status_code=status.HTTP_200_OK)


@app.get("/add_job")
async def add_job():
    print('Add job to scheduler')
    scheduler.add_job(job_function, 'interval', seconds=1)
    return Response(status_code=status.HTTP_200_OK)


def job_function():
    ti = threading.get_ident()
    if ti not in threads_names:
        threads_names.add(ti)
        print(ti)


uvicorn.run(app)

# # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
# try:
#     asyncio.get_event_loop().run_forever()
# except (KeyboardInterrupt, SystemExit):
#     pass

