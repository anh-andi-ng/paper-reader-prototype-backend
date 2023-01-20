from fastapi import FastAPI
from database.database_set_up import Database
from service.entity_service import EntityService
from fastapi import FastAPI
from model.request_body import Keyword
from dependency_injector.wiring import inject
from redis.containers import Container
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database("paper-reader-project-firebase-admins.json", 'https://paper-reader-project-default-rtdb.europe-west1.firebasedatabase.app/')

@app.get("/health")
def check_health():
    return "Server is running"

@app.post("/find")
@inject
async def find(input: Keyword):
    entity_service = EntityService(input.keyword, database.db)
    return entity_service.find()

@app.post("/original")
async def find_original(input: Keyword):
    entity_service = EntityService(input.keyword, database.db)
    return entity_service.original()

container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost")
container.config.redis_password.from_env("REDIS_PASSWORD", "password")
container.wire(modules=[__name__])