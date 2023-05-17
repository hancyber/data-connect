from openopsredis import common as comm
from openopsredis.common import logger


class AggregationHelper:
    pass


LOG_PREFIX = AggregationHelper.__class__.__name__


class AggregationHelper:
    _dict_args = {}
    _last_error = None

    __VALID_LIST = [
        "CUSTOMER_ID", "PROJECT_ID", "CREATE_DATE", "REQUEST_DATE", "MSG_TYPE", "MSG_SUBTYPE", "NAME", "VERSION",
        "INPUT_TYPE", "OUTPUT_TYPE", "INPUT", "OUTPUT"
    ]

    _INPUT_TPL_PATH = "input/"
    _INPUT_TYPE_MAPPER = {
        "mysql": (
            _INPUT_TPL_PATH + "input_mysql.tpl",
            [
                "HOST", "USER", "PASSWORD", "DATABASE"
            ]
        ),
        "bigquery": (
            _INPUT_TPL_PATH + "input_bigquery.tpl",
            []
        )
        # TODO: write input-type-mapper here
    }

    _OUTPUT_TPL_PATH = "output/"
    _OUTPUT_TYPE_MAPPER = {
        "s3": (
            _OUTPUT_TPL_PATH + "output_s3.tpl",
            [
                "BUCKET", "ENDPOINT", "ACCESS_KEY_ID", "SECRET_ACCESS_KEY"
            ]
        )
        # TODO: write output-type-mapper here
    }

    def _check_msg(self, msg):
        self._dict_args = comm.validate_message(message=msg, validate_list=self.__VALID_LIST)
        if self._dict_args is None:
            _last_error = "validate_message error"
            return False

    def _check_input(self):
        if self._dict_args is None or len(self._dict_args) == 0:
            _last_error = "dictionary error"
            logger.error(LOG_PREFIX + self._last_error)
            return False
        if not comm.exist_keys(dict_msg=self._dict_args, validate_list=["INPUT_TYPE", "INPUT"]):
            _last_error = "input error"
            logger.error(LOG_PREFIX + self._last_error)
            return False
        if self._dict_args["INPUT_TYPE"] not in self._INPUT_TYPE_MAPPER:
            _last_error = "input-type error"
            logger.error(LOG_PREFIX + self._last_error)
            return False
        input_file, v_list = self._INPUT_TYPE_MAPPER[self._dict_args["INPUT_TYPE"]]
        self._dict_args["INPUT"]["FILE"] = input_file
        if not comm.exist_keys(dict_msg=self._dict_args["INPUT"], validate_list=v_list):
            _last_error = "input_func error"
            logger.error(LOG_PREFIX + self._last_error)
            return False
        return True

    def _check_output(self):
        if self._dict_args is None or len(self._dict_args) == 0:
            _last_error = "dictionary error"
            logger.error(LOG_PREFIX + self._last_error)
            return False
        if not comm.exist_keys(dict_msg=self._dict_args, validate_list=["OUTPUT_TYPE", "OUTPUT"]):
            _last_error = "input error"
            logger.error(LOG_PREFIX + self._last_error)
            return False
        if self._dict_args["OUTPUT_TYPE"] not in self._OUTPUT_TYPE_MAPPER:
            _last_error = "output-type error"
            logger.error(LOG_PREFIX + self._last_error)
            return False
        output_file, v_list = self._OUTPUT_TYPE_MAPPER[self._dict_args["OUTPUT_TYPE"]]
        self._dict_args["OUTPUT"]["FILE"] = output_file
        if not comm.exist_keys(dict_msg=self._dict_args["OUTPUT"], validate_list=v_list):
            _last_error = "output_func error"
            logger.error(LOG_PREFIX + self._last_error)
            return False
        return True

    def check_msg(self, msg):
        if self._check_msg(msg=msg):
            return self._dict_args
        else:
            return None

    def check_config(self):
        return self._check_input() and self._check_output()

    def get_last_error(self):
        return self._last_error
