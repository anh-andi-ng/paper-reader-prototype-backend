from dependency_injector import containers, providers

from . import redis

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    redis_pool = providers.Resource(
        redis.init_redis_pool,
        host=config.redis_host,
        password=config.redis_password,
    )