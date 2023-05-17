import os

from configparser import ConfigParser
from openopsdata import common
from openopsdata.common import COMMON


class Config:
    def __init__(self, config: str):
        if not os.path.isfile(config):
            raise Exception("configuration not found")
        self.__data = {}
        self.__path = config
        self.__init_config()

    def __init_config(self):
        parser = ConfigParser()
        parser.read(self.__path)
        self.__data[COMMON.CONFIG_SECTION_BASE()] = \
            common.get_config_section(config=parser, key=COMMON.CONFIG_SECTION_BASE())
        if COMMON.BASE_CONFIG_SECTION() in self.__data[COMMON.CONFIG_SECTION_BASE()]:
            for section in self.__data[COMMON.CONFIG_SECTION_BASE()][COMMON.BASE_CONFIG_SECTION()].split(","):
                self.__data[section] = common.get_config_section(config=parser, key=section)

    def reload(self):
        if self.__path:
            self.__init_config()

    def get_config(self, section):
        if section in self.__data:
            return self.__data[section]
        else:
            return {}
