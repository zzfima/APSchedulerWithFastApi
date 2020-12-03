import datetime
import threading

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import Response, JSONResponse

threads_names = set()
app = FastAPI()
scheduler = BackgroundScheduler()


@app.get("/get_thread_names")
async def get_thread_names():
    print('get_thread_names')
    json_compatible_item_data = jsonable_encoder(threads_names)
    return JSONResponse(content=json_compatible_item_data, status_code=status.HTTP_200_OK)


@app.get("/start_scheduler")
async def start_scheduler():
    print('Run scheduler')
    if scheduler.state == 0:
        scheduler.start()
    return Response('Started', status_code=status.HTTP_200_OK)


@app.get("/add_job")
async def add_job():
    print('Add job to scheduler')
    scheduler.add_job(do_job, 'interval', seconds=5)
    return Response('Job Added', status_code=status.HTTP_200_OK)


def do_job():
    print(datetime.datetime.now())
    ti = threading.get_ident()
    if ti not in threads_names:
        threads_names.add(ti)
        print(ti)


uvicorn.run(app)
