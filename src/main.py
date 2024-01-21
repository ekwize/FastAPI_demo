from contextlib import asynccontextmanager
import time
import sentry_sdk

from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator


from src.admin.auth import authentication_backend
from src.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from src.bookings.router import router as router_bookings
from src.config import settings
from src.database import engine
from src.images.router import router as router_images
from src.users.router import router as router_users
from src.logger import logger
from src.prometheus.router import router as router_prometheus


app = FastAPI()

if settings.MODE != "TEST":
    sentry_sdk.init(
        dsn="https://3bc1586d6be75f9136eb62087827cd40@o4506603598184448.ingest.sentry.io/4506603603558400",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )




app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_images)
app.include_router(router_prometheus)
# app.include_router(router_pages)


app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')
#     description='Greet users with a nice message',
#     middleware=[
#         Middleware(SessionMiddleware, secret_key='mysecretkey')
#     ]
# )
if settings.MODE == "TEST":
    # При тестировании через pytest, необходимо подключать Redis, чтобы кэширование работало.
    # Иначе декоратор @cache из библиотеки fastapi-cache ломает выполнение кэшируемых эндпоинтов.
    # Из этого следует вывод, что сторонние решения порой ломают наш код, и это бывает проблематично поправить.
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield
    ...

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin*.", "/metrics"],
)

instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response




