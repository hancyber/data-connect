import asyncio
import time

from concurrent.futures import ThreadPoolExecutor

from openopsredis.mredis import ConnectionMode, OpenopsRedis

from openopsdata.aggregator import Aggregator
from openopsdata.gateway.gateway import Gateway
from openopsdata import common
from openopsdata.common import COMMON, logger


class GatewayRedis(Gateway):
    __SHUTDOWN_MSG = "shutdown hgb aggregator"
    __DEFAULT_GATEWAY_SLEEP_OBSERVER = 1
    __DEFAULT_GATEWAY_SLEEP_WATCHER = 10
    __DEFAULT_GATEWAY_THREAD_MAX = 10

    def __init__(self, config):
        super().__init__(config)

        redis_info = self._config[COMMON.CONFIG_SECTION_REDIS()] \
            if COMMON.CONFIG_SECTION_REDIS() in self._config else None
        service_name = redis_info[COMMON.REDIS_SERVICE_NAME()] \
            if redis_info and COMMON.REDIS_SERVICE_NAME() in redis_info else None
        server = common.get_tuple_list(redis_info[COMMON.REDIS_SERVER_INFO()]) \
            if redis_info and COMMON.REDIS_SERVER_INFO() in redis_info else None
        ssl_ca_certs = redis_info[COMMON.REDIS_SSL_CA_CERTS()] \
            if redis_info and COMMON.REDIS_SSL_CA_CERTS() in redis_info else None
        self.__redis = OpenopsRedis(service_name=service_name, server=server, ssl_ca_certs=ssl_ca_certs) \
            if redis_info and service_name and ssl_ca_certs else None

        self.__gateway_channel = redis_info[COMMON.REDIS_GATEWAY_CHANNEL()] \
            if redis_info and COMMON.REDIS_GATEWAY_CHANNEL() in redis_info else None

        self.__gateway_sleep_observer = int(redis_info[COMMON.REDIS_GATEWAY_SLEEP_OBSERVER()]) \
            if redis_info and COMMON.REDIS_GATEWAY_SLEEP_OBSERVER() in redis_info \
            else self.__DEFAULT_GATEWAY_SLEEP_OBSERVER

        self.__gateway_sleep_watcher = int(redis_info[COMMON.REDIS_GATEWAY_SLEEP_WATCHER()]) \
            if redis_info and COMMON.REDIS_GATEWAY_SLEEP_WATCHER() in redis_info \
            else self.__DEFAULT_GATEWAY_SLEEP_WATCHER

        gateway_thread_max = int(redis_info[COMMON.REDIS_GATEWAY_THREAD_MAX()]) \
            if redis_info and COMMON.REDIS_GATEWAY_THREAD_MAX() in redis_info else self.__DEFAULT_GATEWAY_THREAD_MAX
        self.__th_executor = ThreadPoolExecutor(max_workers=gateway_thread_max)

        self.__is_wait = True

    async def __start(self):
        self.__observer = asyncio.create_task(self.__start_observer())
        while self.__is_wait:
            await asyncio.sleep(self.__gateway_sleep_watcher)
            await self.__start_watcher()

    async def __start_watcher(self):
        if self.__is_wait:
            if self.__observer is not None and (self.__observer.done() or self.__observer.cancelled()):
                self.__observer = None
                logger.info("try to restart observer")
                self.__observer = asyncio.create_task(self.__start_observer())
            else:
                logger.debug(self.__class__.__name__ + "\'s message: I\'m alive!")

    async def __start_observer(self):
        try:
            observer = self.__redis.get_connection(ConnectionMode.READWRITE)
        except Exception as err:
            logger.critical(str(err))
            return None

        logger.info("start observer [ %s ]" % self.__gateway_channel)
        start_time = time.time()
        while self.__is_wait:
            message = observer.lpop(name=self.__gateway_channel)
            if message:
                info = message.decode("utf-8")
                logger.debug("received msg: " + info)
                # to-do: graceful exit
                if info == self.__SHUTDOWN_MSG:
                    self.__is_wait = False
                    logger.info("quiting signal received")
                else:
                    self.__th_executor.submit(self._executor, msg=info)
            end_time = time.time()
            if self.__is_wait and end_time - start_time >= self.__gateway_sleep_observer:
                await asyncio.sleep(self.__gateway_sleep_observer)
                start_time = time.time()

    def _async_executor(self, executor: Aggregator, **kwargs):
        rst, msg = executor.execute()
        logger.debug("result: " + str(rst) + ", " + str(msg))

    def _sync_executor(self, executor: Aggregator, **kwargs):
        logger.warning("synchronization method not supported. It runs asynchronously.")
        self._async_executor(executor=executor, kwargs=kwargs)

    def run(self):
        if self.__redis and self.__gateway_channel:
            asyncio.run(self.__start())
            self.__th_executor.shutdown(wait=True)
        else:
            logger.critical("not found redis info")
        logger.info("closed")
