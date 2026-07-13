from pyrate_limiter import Duration, Limiter, Rate, RedisBucket

from packages.redis.redis_client import AsyncRedisConnManager as AsyncRedis

limiter = None


async def init_limiter():
    global limiter
    redis = AsyncRedis().get_master()
    rates = [Rate(20, Duration.MINUTE)]
    bucket = await RedisBucket.init(rates, redis, "rate-limiter")
    limiter = Limiter(bucket)
    return limiter
