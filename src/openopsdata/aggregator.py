import json
import subprocess

from os import path, makedirs
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from openopsdata import common
from openopsdata.common import COMMON
from openopsdata.helper import AggregationHelper
from openopsrelay.callback import CallbackType


class Aggregator:
    __LOG_GUESS = 'log/guess'
    __LOG_PREVIEW = 'log/preview'
    __LOG_RUN = 'log/preview'

    def __init__(self, conf, msg):
        self.__init_conf(conf=conf)
        self.__init_msg(msg=msg)
        self.__init_callback()

    def __init_conf(self, conf):
        self.__conf = conf
        if COMMON.CONFIG_SECTION_EMBULK() not in self.__conf:
            raise Exception("not found tpl config")
        self.__init_info(info=self.__conf[COMMON.CONFIG_SECTION_EMBULK()])

    def __init_info(self, info):
        self.__tpl_path = info[COMMON.EMBULK_TPL_PATH()] if COMMON.EMBULK_TPL_PATH() in info else None
        self.__tpl_main = info[COMMON.EMBULK_TPL_MAIN()] if COMMON.EMBULK_TPL_MAIN() in info else None
        self.__path_conf = info[COMMON.EMBULK_PATH_CONF()] if COMMON.EMBULK_PATH_CONF() in info else None
        self.__path_log_guess = info[COMMON.EMBULK_PATH_LOG_GUESS()] \
            if COMMON.EMBULK_PATH_LOG_GUESS() in info else self.__LOG_GUESS
        self.__path_log_preview = info[COMMON.EMBULK_PATH_LOG_PREVIEW()] \
            if COMMON.EMBULK_PATH_LOG_PREVIEW() in info else self.__LOG_PREVIEW
        self.__path_log_run = info[COMMON.EMBULK_PATH_LOG_RUN()] \
            if COMMON.EMBULK_PATH_LOG_RUN() in info else self.__LOG_RUN
        self.__file_guess = info[COMMON.EMBULK_FILE_GUESS()] if COMMON.EMBULK_FILE_GUESS() in info else None
        self.__file_preview = info[COMMON.EMBULK_FILE_PREVIEW()] if COMMON.EMBULK_FILE_PREVIEW() in info else None
        self.__file_run = info[COMMON.EMBULK_FILE_RUN()] if COMMON.EMBULK_FILE_RUN() in info else None

    def __init_msg(self, msg):
        helper = AggregationHelper()
        self.__msg = helper.check_msg(msg)
        if not self.__msg:
            raise Exception("incorrect message")

    def __init_callback(self):
        self.__callback = common.get_callback(msg=self.__msg, conf=self.__conf)
        self.__msg[COMMON.KEY_CHANNEL()] = \
            str(self.__msg[COMMON.KEY_CUSTOMER_ID()]) + str(self.__msg[COMMON.KEY_PROJECT_ID()]) + \
            str(self.__msg[COMMON.KEY_MSG_TYPE()]) + str(self.__msg[COMMON.KEY_MSG_SUBTYPE()]) + \
            str(self.__msg[COMMON.KEY_NAME()]) + str(self.__msg[COMMON.KEY_VERSION()])
        self.__msg[COMMON.KEY_RETURN_RESULT()] = str(False)
        self.__msg[COMMON.KEY_RETURN_MSG()] = ""

    def __do_callback(self, status: bool, msg: str):
        callback_status = CallbackType.STATUS_SUCCESS if status else CallbackType.STATUS_FAIL
        self.__msg[COMMON.KEY_RETURN_RESULT()] = str(status)
        self.__msg[COMMON.KEY_RETURN_MSG()] = msg
        common.do_callback(callback=self.__callback, callback_status=callback_status, **self.__msg)

    def __guess_conf(self):
        rst = True
        msg = "success"
        if COMMON.KEY_PRE_ACTION() in self.__msg and \
                self.__msg[COMMON.KEY_PRE_ACTION()] == COMMON.VALUE_PRE_ACTION_GUESS():
            if self.__file_guess:
                conf_file = self.__path_conf + "/" + self.__msg[COMMON.KEY_NAME()] + "/" + \
                    self.__msg[COMMON.KEY_VERSION()] + ".yaml"
                log_file = self.__path_log_guess + "/" + \
                    self.__msg[COMMON.KEY_NAME()] + "_" + self.__msg[COMMON.KEY_VERSION()] + ".log"

                out = subprocess.Popen(
                    [self.__file_guess, conf_file, log_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                out_msg = ""
                for line in out.stdout.readlines():
                    out_msg += line.decode('utf-8')
                out.wait()
                rst = out.returncode == 0
                if not rst:
                    msg = out_msg
            else:
                rst, msg = False, "not found guess command"
        return rst, msg

    def __make_conf(self):
        helper = AggregationHelper()
        input_dict, output_dict = helper.check_input(dict_args=self.__msg), helper.check_output(dict_args=self.__msg)
        if input_dict is not None and output_dict is not None:
            self.__msg[COMMON.KEY_INPUT()] = input_dict
            self.__msg[COMMON.KEY_OUTPUT()] = output_dict
            env = Environment(loader=FileSystemLoader(self.__tpl_path), trim_blocks=True, lstrip_blocks=True)
            try:
                tpl = env.get_template(self.__tpl_main)
            except TemplateNotFound as err:
                return False, str(err)
            content = tpl.render(self.__msg)
            file_path = self.__path_conf + "/" + self.__msg[COMMON.KEY_NAME()]
            try:
                makedirs(file_path)
            except IOError:
                pass
            file_full = file_path + "/" + self.__msg[COMMON.KEY_VERSION()] + ".yaml"
            with open(file_full, "w") as fp:
                file_cnt = fp.write(content)
            if path.isfile(file_full) and file_cnt > 0:
                return self.__guess_conf()
            else:
                return False, "configuration fail"
        else:
            return False, helper.get_last_error()

    def __preview(self):
        rst, msg = False, "not found preview command"
        if self.__file_preview:
            conf_file = self.__path_conf + "/" + self.__msg[COMMON.KEY_NAME()] + "/" + \
                self.__msg[COMMON.KEY_VERSION()] + ".yaml"
            log_file = self.__path_log_preview + "/" + \
                self.__msg[COMMON.KEY_NAME()] + "_" + self.__msg[COMMON.KEY_VERSION()] + ".log"
            if not path.isfile(conf_file):
                msg = "not found conf file"
            else:
                out = subprocess.Popen(
                    [self.__file_preview, conf_file, log_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                preview = ""
                for line in out.stdout.readlines():
                    preview += line.decode('utf-8')
                out.wait()
                rst = out.returncode == 0
                msg = preview
        return rst, msg

    def __run(self):
        rst, msg = False, "not found run command"
        if self.__file_run:
            conf_file = self.__path_conf + "/" + self.__msg[COMMON.KEY_NAME()] + "/" + \
                self.__msg[COMMON.KEY_VERSION()] + ".yaml"
            log_file = self.__path_log_run + "/" + \
                self.__msg[COMMON.KEY_NAME()] + "_" + self.__msg[COMMON.KEY_VERSION()] + ".log"
            if not path.isfile(conf_file):
                msg = "not found conf file"
            else:
                out = subprocess.Popen(
                    [self.__file_run, conf_file, log_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                )
                preview = ""
                for line in out.stdout.readlines():
                    preview += line.decode('utf-8')
                out.wait()
                rst = out.returncode == 0
                msg = preview
        return rst, msg

    def get_message(self, column):
        return self.__msg[column] if column in self.__msg else None

    def execute(self):
        rst, msg = (False, "init status")
        if self.__msg[COMMON.KEY_MSG_TYPE()] != COMMON.VALUE_MSG_TYPE_AGGR():
            msg = "unknown message type"
        else:
            if self.__msg[COMMON.KEY_MSG_SUBTYPE()] == COMMON.VALUE_MSG_SUBTYPE_CONFIG():
                rst, msg = self.__make_conf()
            elif self.__msg[COMMON.KEY_MSG_SUBTYPE()] == COMMON.VALUE_MSG_SUBTYPE_PREVIEW():
                rst, msg = self.__preview()
            elif self.__msg[COMMON.KEY_MSG_SUBTYPE()] == COMMON.VALUE_MSG_SUBTYPE_RUN():
                rst, msg = self.__run()
            else:
                msg = "unknown sub message type"
        self.__do_callback(rst, msg)
        return rst, json.dumps(self.__msg)
