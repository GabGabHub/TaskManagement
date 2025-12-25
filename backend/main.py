from fastapi import FastAPI
import uvicorn
from routers import taskRoute,userRoute

app = FastAPI(
    title="Task Management Website",
    summary="Just a website to create and manage tasks.",
)

app.include_router(taskRoute.router)
app.include_router(userRoute.router)

@app.get("/")
def root():
 return {"status": "ok"}


uvicorn.run(app, host= '127.0.1.1', port = 8008)