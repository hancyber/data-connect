import os
import sys

from openopsdata.config import Config
from openopsdata.common import COMMON, logger
from openopsdata.gateway.gateway_socket import GatewaySocket
from openopsdata.gateway.gateway_redis import GatewayRedis


class AggregatorRunner:
    def __init__(self, conf_file):
        self.__configuration = {}
        self.__gateway = None
        conf_obj = Config(conf_file)
        dict_conf = conf_obj.get_config(COMMON.CONFIG_SECTION_BASE())
        if COMMON.BASE_CONFIG_SECTION() in dict_conf:
            self.__deepcopy(conf_obj=conf_obj, src=dict_conf[COMMON.BASE_CONFIG_SECTION()].split(","))
        else:
            raise Exception("init error")
        self.__gateway_factory()

    def __deepcopy(self, conf_obj, src):
        for section in src:
            data = conf_obj.get_config(section)
            tmp_dict = {}
            if data:
                for key in data:
                    tmp_dict[key] = data[key]
            self.__configuration[section] = tmp_dict

    def __gateway_factory(self):
        if COMMON.CONFIG_SECTION_COMMON() not in self.__configuration:
            raise Exception("not found gateway")
        info = self.__configuration[COMMON.CONFIG_SECTION_COMMON()]
        if COMMON.COMMON_GATEWAY() not in info:
            raise Exception("not found gateway info")
        gw = info[COMMON.COMMON_GATEWAY()]
        if gw == COMMON.GATEWAY_SOCKET():
            self.__gateway = GatewaySocket(config=self.__configuration)
        elif gw == COMMON.GATEWAY_REDIS():
            self.__gateway = GatewayRedis(config=self.__configuration)
        # TODO: add gateway sub class instance
        else:
            raise Exception("unknown gateway")

    def run(self):
        if self.__gateway:
            self.__gateway.run()
        else:
            logger.critical("configuration error")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        logger.error("argument error")
    else:
        arg_config = None
        if os.path.isfile(sys.argv[1]):
            arg_config = sys.argv[1]
            runner = AggregatorRunner(arg_config)
            runner.run()
        else:
            logger.error("incorrect file")

    sys.exit(1)
