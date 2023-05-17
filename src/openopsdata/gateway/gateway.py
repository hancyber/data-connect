from openopsdata.aggregator import Aggregator
from openopsdata.common import COMMON, logger


class Gateway:
    def __init__(self, conf):
        self._config = conf

    def _executor(self, msg, **kwargs):
        try:
            executor = Aggregator(conf=self._config, msg=msg)
            if executor:
                sync_type = executor.get_message(COMMON.KEY_SYNC_TYPE())
                if not sync_type:
                    sync_type = COMMON.VALUE_SYNC_TYPE_DEFAULT()
                if sync_type == COMMON.VALUE_SYNC_TYPE_ASYNC():
                    self._async_executor(msg=msg, executor=executor, **kwargs)
                elif sync_type == COMMON.VALUE_SYNC_TYPE_SYNC():
                    self._sync_executor(msg=msg, executor=executor, **kwargs)
                else:
                    logger.error("unknown sync type")
        except Exception as err:
            logger.error(str(err))

    def _async_executor(self, executor: Aggregator, **kwargs):
        raise Exception("Cannot use this")

    def _sync_executor(self, executor: Aggregator, **kwargs):
        raise Exception("Cannot use this")

    def run(self):
        raise Exception("Cannot use this")
