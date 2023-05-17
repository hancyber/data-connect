import logging
import json
import re

from configparser import ConfigParser
from json.decoder import JSONDecodeError
from openopsrelay.callback import CallbackType
from openopsrelay.subject import Subject
from openopsrelay.observer import ObserverConsole
from openopsrelay.observerhttp_dc import ObserverHttpDC
from openopsrelay.observerredis import ObserverRedis

# for logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
stream = logging.StreamHandler()
stream.setFormatter(formatter)
logger.addHandler(stream)


class COMMON:
    # configuration variant
    __config_section_base = "base"
    __config_section_embulk = "embulk"
    __config_section_common = "common"
    __config_section_socket = "socket"
    __config_section_redis = "redis"
    __config_section_http = "http"

    __base_config_section = "config.section"

    __embulk_tpl_path = "tpl.path"
    __embulk_tpl_main = "tpl.main"
    __embulk_path_conf = "path.conf"
    __embulk_path_log_guess = "path.log.guess"
    __embulk_path_log_preview = "path.log.preview"
    __embulk_path_log_run = "path.log.run"
    __embulk_file_guess = "file.guess"
    __embulk_file_preview = "file.preview"
    __embulk_file_run = "file.run"

    __common_gateway = "gateway"

    __socket_host = "host"
    __socket_port = "port"
    __socket_backlog = "backlog"
    __socket_buffer_size = "buffer.size"

    __redis_service_name = "service.name"
    __redis_ssl_ca_certs = "ssl.ca.certs"
    __redis_server_info = "server.info"
    __redis_gateway_channel = "gateway.channel"
    __redis_gateway_sleep_observer = "gateway.sleep.observer"
    __redis_gateway_sleep_watcher = "gateway.sleep.watcher"
    __redis_gateway_thread_max = "gateway.thread.max"

    __http_baseurl = "baseurl"

    @classmethod
    def CONFIG_SECTION_BASE(cls):
        return cls.__config_section_base

    @classmethod
    def CONFIG_SECTION_EMBULK(cls):
        return cls.__config_section_embulk

    @classmethod
    def CONFIG_SECTION_COMMON(cls):
        return cls.__config_section_common

    @classmethod
    def CONFIG_SECTION_SOCKET(cls):
        return cls.__config_section_socket

    @classmethod
    def CONFIG_SECTION_REDIS(cls):
        return cls.__config_section_redis

    @classmethod
    def CONFIG_SECTION_HTTP(cls):
        return cls.__config_section_http

    @classmethod
    def BASE_CONFIG_SECTION(cls):
        return cls.__base_config_section

    @classmethod
    def EMBULK_TPL_PATH(cls):
        return cls.__embulk_tpl_path

    @classmethod
    def EMBULK_TPL_MAIN(cls):
        return cls.__embulk_tpl_main

    @classmethod
    def EMBULK_PATH_CONF(cls):
        return cls.__embulk_path_conf

    @classmethod
    def EMBULK_PATH_LOG_GUESS(cls):
        return cls.__embulk_path_log_guess

    @classmethod
    def EMBULK_PATH_LOG_PREVIEW(cls):
        return cls.__embulk_path_log_preview

    @classmethod
    def EMBULK_PATH_LOG_RUN(cls):
        return cls.__embulk_path_log_run

    @classmethod
    def EMBULK_FILE_GUESS(cls):
        return cls.__embulk_file_guess

    @classmethod
    def EMBULK_FILE_PREVIEW(cls):
        return cls.__embulk_file_preview

    @classmethod
    def EMBULK_FILE_RUN(cls):
        return cls.__embulk_file_run

    @classmethod
    def SOCKET_HOST(cls):
        return cls.__socket_host

    @classmethod
    def SOCKET_PORT(cls):
        return cls.__socket_port

    @classmethod
    def SOCKET_BACKLOG(cls):
        return cls.__socket_backlog

    @classmethod
    def SOCKET_BUFFER_SIZE(cls):
        return cls.__socket_buffer_size

    @classmethod
    def COMMON_GATEWAY(cls):
        return cls.__common_gateway

    @classmethod
    def REDIS_SERVICE_NAME(cls):
        return cls.__redis_service_name

    @classmethod
    def REDIS_SSL_CA_CERTS(cls):
        return cls.__redis_ssl_ca_certs

    @classmethod
    def REDIS_SERVER_INFO(cls):
        return cls.__redis_server_info

    @classmethod
    def REDIS_GATEWAY_CHANNEL(cls):
        return cls.__redis_gateway_channel

    @classmethod
    def REDIS_GATEWAY_SLEEP_OBSERVER(cls):
        return cls.__redis_gateway_sleep_observer

    @classmethod
    def REDIS_GATEWAY_SLEEP_WATCHER(cls):
        return cls.__redis_gateway_sleep_watcher

    @classmethod
    def REDIS_GATEWAY_THREAD_MAX(cls):
        return cls.__redis_gateway_thread_max

    @classmethod
    def HTTP_BASEURL(cls):
        return cls.__http_baseurl

    # configuration value
    __gateway_socket = "socket"
    __gateway_redis = "redis"

    @classmethod
    def GATEWAY_SOCKET(cls):
        return cls.__gateway_socket

    @classmethod
    def GATEWAY_REDIS(cls):
        return cls.__gateway_redis

    # interface variant
    # "CUSTOMER_ID", "PROJECT_ID", "CREATE_DATE", "REQUEST_DATE", "MSG_TYPE", "MSG_SUBTYPE", "NAME", "VERSION"
    __KEY_CUSTOMER_ID = "CUSTOMER_ID"
    __KEY_PROJECT_ID = "PROJECT_ID"
    __KEY_CREATE_DATE = "CREATE_DATE"
    __KEY_REQUEST_DATE = "REQUEST_DATE"
    __KEY_MSG_TYPE = "MSG_TYPE"
    __KEY_MSG_SUBTYPE = "MSG_SUBTYPE"
    __KEY_NAME = "NAME"
    __KEY_VERSION = "VERSION"
    __KEY_SYNC_TYPE = "SYNC_TYPE"
    __KEY_ASYNC_CALLBACK_TYPE = "ASYNC_CALLBACK_TYPE"
    # callback redis channel
    __KEY_CHANNEL = "CHANNEL"
    __KEY_PRE_ACTION = "PRE_ACTION"
    # return result
    __KEY_RETURN_RESULT = "RETURN_RESULT"
    # return message
    __KEY_RETURN_MSG = "RETURN_MSG"
    # __KEY_EXEC = "EXEC"
    __KEY_FILE = "FILE"
    __KEY_INPUT_TYPE = "INPUT_TYPE"
    __KEY_INPUT = "INPUT"
    __KEY_OUTPUT_TYPE = "OUTPUT_TYPE"
    __KEY_OUTPUT = "OUTPUT"
    __KEY_ROOT_PATH = "ROOT_PATH"

    @classmethod
    def KEY_CUSTOMER_ID(cls):
        return cls.__KEY_CUSTOMER_ID

    @classmethod
    def KEY_PROJECT_ID(cls):
        return cls.__KEY_PROJECT_ID

    @classmethod
    def KEY_CREATE_DATE(cls):
        return cls.__KEY_CREATE_DATE

    @classmethod
    def KEY_REQUEST_DATE(cls):
        return cls.__KEY_REQUEST_DATE

    @classmethod
    def KEY_MSG_TYPE(cls):
        return cls.__KEY_MSG_TYPE

    @classmethod
    def KEY_MSG_SUBTYPE(cls):
        return cls.__KEY_MSG_SUBTYPE

    @classmethod
    def KEY_NAME(cls):
        return cls.__KEY_NAME

    @classmethod
    def KEY_VERSION(cls):
        return cls.__KEY_VERSION

    @classmethod
    def KEY_SYNC_TYPE(cls):
        return cls.__KEY_SYNC_TYPE

    @classmethod
    def KEY_ASYNC_CALLBACK_TYPE(cls):
        return cls.__KEY_ASYNC_CALLBACK_TYPE

    @classmethod
    def KEY_CHANNEL(cls):
        return cls.__KEY_CHANNEL

    @classmethod
    def KEY_PRE_ACTION(cls):
        return cls.__KEY_PRE_ACTION

    @classmethod
    def KEY_RETURN_RESULT(cls):
        return cls.__KEY_RETURN_RESULT

    @classmethod
    def KEY_RETURN_MSG(cls):
        return cls.__KEY_RETURN_MSG

    '''
    @classmethod
    def KEY_EXEC(cls):
        return cls.__KEY_EXEC
    '''

    @classmethod
    def KEY_FILE(cls):
        return cls.__KEY_FILE

    @classmethod
    def KEY_INPUT_TYPE(cls):
        return cls.__KEY_INPUT_TYPE

    @classmethod
    def KEY_INPUT(cls):
        return cls.__KEY_INPUT

    @classmethod
    def KEY_OUTPUT_TYPE(cls):
        return cls.__KEY_OUTPUT_TYPE

    @classmethod
    def KEY_OUTPUT(cls):
        return cls.__KEY_OUTPUT

    @classmethod
    def KEY_ROOT_PATH(cls):
        return cls.__KEY_ROOT_PATH

    # interface value
    __VALUE_MSG_TYPE_AGGR = "AGGR"
    __VALUE_MSG_SUBTYPE_CONFIG = "CONFIG"
    __VALUE_MSG_SUBTYPE_PREVIEW = "PREVIEW"
    __VALUE_MSG_SUBTYPE_RUN = "RUN"
    __VALUE_SYNC_TYPE_ASYNC = "ASYNC"
    __VALUE_SYNC_TYPE_SYNC = "SYNC"
    __VALUE_SYNC_TYPE_DEFAULT = __VALUE_SYNC_TYPE_ASYNC
    __VALUE_CALLBACK_TYPE_CONSOLE = "CONSOLE"
    __VALUE_CALLBACK_TYPE_HTTP = "HTTP"
    __VALUE_CALLBACK_TYPE_REDIS = "REDIS"
    __VALUE_PRE_ACTION_GUESS = "GUESS"

    @classmethod
    def VALUE_MSG_TYPE_AGGR(cls):
        return cls.__VALUE_MSG_TYPE_AGGR

    @classmethod
    def VALUE_MSG_SUBTYPE_CONFIG(cls):
        return cls.__VALUE_MSG_SUBTYPE_CONFIG

    @classmethod
    def VALUE_MSG_SUBTYPE_PREVIEW(cls):
        return cls.__VALUE_MSG_SUBTYPE_PREVIEW

    @classmethod
    def VALUE_MSG_SUBTYPE_RUN(cls):
        return cls.__VALUE_MSG_SUBTYPE_RUN

    @classmethod
    def VALUE_SYNC_TYPE_ASYNC(cls):
        return cls.__VALUE_SYNC_TYPE_ASYNC

    @classmethod
    def VALUE_SYNC_TYPE_SYNC(cls):
        return cls.__VALUE_SYNC_TYPE_SYNC

    @classmethod
    def VALUE_SYNC_TYPE_DEFAULT(cls):
        return cls.__VALUE_SYNC_TYPE_DEFAULT

    @classmethod
    def VALUE_CALLBACK_TYPE_CONSOLE(cls):
        return cls.__VALUE_CALLBACK_TYPE_CONSOLE

    @classmethod
    def VALUE_CALLBACK_TYPE_HTTP(cls):
        return cls.__VALUE_CALLBACK_TYPE_HTTP

    @classmethod
    def VALUE_CALLBACK_TYPE_REDIS(cls):
        return cls.__VALUE_CALLBACK_TYPE_REDIS

    @classmethod
    def VALUE_PRE_ACTION_GUESS(cls):
        return cls.__VALUE_PRE_ACTION_GUESS


# substitute openopsredis.common
def get_config_section(config: ConfigParser, key: str):
    section = None
    if config and config.has_section(key):
        section = config[key]
    return section


def validate_message(message: str, validate_list: list):
    if validate_list is None:
        return None
    try:
        re_str = re.sub('(?<!\\\\)\'', '"', message)
        dict_msg: dict = json.loads(re_str)
    except JSONDecodeError:
        return None
    for key in validate_list:
        if key not in dict_msg:
            return None
    return dict_msg


def exist_keys(dict_msg: dict, validate_list: list):
    if validate_list is None:
        return False
    for key in validate_list:
        if key not in dict_msg:
            return False
    return True


def get_tuple_list(tuple_string: str):
    tuple_list: list = []
    for x in tuple_string.split(","):
        y = x.split(":")
        if len(y) == 2:
            tuple_list.append((y[0].strip(), y[1].strip()))
    return tuple_list


def get_callback(msg: dict, conf: dict):
    callback: Subject = Subject()
    if COMMON.KEY_ASYNC_CALLBACK_TYPE() in msg:
        callback_type = msg[COMMON.KEY_ASYNC_CALLBACK_TYPE()].split(",")
        if COMMON.VALUE_CALLBACK_TYPE_CONSOLE() in callback_type:
            callback.attach(ObserverConsole(logger=logger))
        if msg[COMMON.KEY_ASYNC_CALLBACK_TYPE()] == COMMON.VALUE_CALLBACK_TYPE_HTTP():
            kwargs = {}
            if COMMON.CONFIG_SECTION_HTTP() in conf:
                http_conf = conf[COMMON.CONFIG_SECTION_HTTP()]
                baseurl = \
                    http_conf[COMMON.HTTP_BASEURL()] if COMMON.HTTP_BASEURL() in http_conf else "http://localhost"
                kwargs['baseurl'] = baseurl
            callback.attach(ObserverHttpDC(**kwargs))
        if msg[COMMON.KEY_ASYNC_CALLBACK_TYPE()] == COMMON.VALUE_CALLBACK_TYPE_REDIS():
            if COMMON.CONFIG_SECTION_REDIS() in conf:
                redis_conf = conf[COMMON.CONFIG_SECTION_REDIS()]
                service_name = \
                    redis_conf[COMMON.REDIS_SERVICE_NAME()] if COMMON.REDIS_SERVICE_NAME() in redis_conf else None
                server = \
                    get_tuple_list(redis_conf[COMMON.REDIS_SERVER_INFO()]) \
                    if COMMON.REDIS_SERVER_INFO() in redis_conf else None
                ssl_ca_certs = \
                    redis_conf[COMMON.REDIS_SSL_CA_CERTS()] if COMMON.REDIS_SSL_CA_CERTS() in redis_conf else None
                if service_name and server and ssl_ca_certs:
                    callback.attach(
                        ObserverRedis(service_name=service_name, server=server, ssl_ca_certs=ssl_ca_certs)
                    )
    return callback


def do_callback(callback: Subject, callback_status: CallbackType, callback_type: CallbackType = CallbackType.AGGR_TYPE,
                **kwargs):
    callback.notify(notify_type=callback_type, notify_status=callback_status, **kwargs)
