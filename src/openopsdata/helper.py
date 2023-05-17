from os import path, makedirs
from openopsdata import common
from openopsdata.common import COMMON


class AggregationHelper:
    def __init__(self):
        self.__last_error = "none"

    def __input(self, **kwargs):
        pass

    # TODO: write input-function here

    def __output(self, **kwargs):
        pass

    def __output_file(self, **kwargs):
        if COMMON.KEY_NAME() in kwargs and COMMON.KEY_ROOT_PATH() in kwargs[COMMON.KEY_OUTPUT()]:
            data_path = kwargs[COMMON.KEY_OUTPUT()][COMMON.KEY_ROOT_PATH()] + "/" + kwargs[COMMON.KEY_NAME()]
            if not path.isdir(data_path):
                try:
                    makedirs(data_path)
                except IOError as err:
                    self.__last_error = str(err)
        else:
            self.__last_error = "not found path"

    # TODO: write output-function here

    __VALID_LIST = [
        COMMON.KEY_CUSTOMER_ID(), COMMON.KEY_PROJECT_ID(),
        COMMON.KEY_CREATE_DATE(), COMMON.KEY_REQUEST_DATE(),
        COMMON.KEY_MSG_TYPE(), COMMON.KEY_MSG_SUBTYPE(),
        COMMON.KEY_NAME(), COMMON.KEY_VERSION()
    ]

    _INPUT_TPL_PATH = "input/"
    _INPUT_TYPE_MAPPER = {
        # type name
        "mysql": (
            # file path
            _INPUT_TPL_PATH + "input_mysql.tpl",
            # template validation variant
            [
                "HOST", "PORT", "USER", "PASSWORD", "DATABASE", "QUERY"
            ],
            __input
        ),
        "postgresql": (
            _INPUT_TPL_PATH + "input_postgresql.tpl",
            [
                "HOST", "PORT", "USER", "PASSWORD", "DATABASE", "SCHEMA", "QUERY"
            ],
            __input
        ),
        "oracle": (
            _INPUT_TPL_PATH + "input_oracle.tpl",
            [
                "URL", "USER", "PASSWORD", "QUERY"
            ],
            __input
        ),
        "sqlserver": (
            _INPUT_TPL_PATH + "input_sqlserver.tpl",
            [
                "HOST", "PORT", "USER", "PASSWORD", "DATABASE", "QUERY"
            ],
            __input
        ),
        # type name
        "azure_blob": (
            # file path
            _INPUT_TPL_PATH + "input_azure_blob.tpl",
            # template validation variant
            [
                "ACCOUNT_NAME", "ACCOUNT_KEY", "CONTAINER", "PATH_PREFIX"
            ],
            __input
        ),
        "bigquery": (
            _INPUT_TPL_PATH + "input_bigquery.tpl",
            [
                "PROJECT", "KEYFILE", "SQL"
            ],
            __input
        )
        # TODO: write input-type-mapper here
        # input-name: (
        #     input-file-path,
        #     [input-validation-keys],
        #     input-function
        # )
    }

    _OUTPUT_TPL_PATH = "output/"
    _OUTPUT_TYPE_MAPPER = {
        "s3": (
            _OUTPUT_TPL_PATH + "output_s3.tpl",
            [
                "BUCKET", "ENDPOINT", "ACCESS_KEY_ID", "SECRET_ACCESS_KEY"
            ],
            __output
        ),
        "file": (
            _OUTPUT_TPL_PATH + "output_file.tpl",
            [
                "ROOT_PATH"
            ],
            __output_file
        )
        # TODO: write output-type-mapper here
        # output-name: (
        #     output-file-path,
        #     [output-validation-keys],
        #     output-function
        # )
    }

    def check_msg(self, msg: str):
        return common.validate_message(message=str(msg), validate_list=self.__VALID_LIST)

    def check_input(self, dict_args: dict):
        if dict_args is None or len(dict_args) == 0:
            self.__last_error = "dictionary error"
            return None
        if not common.exist_keys(dict_msg=dict_args, validate_list=[COMMON.KEY_INPUT_TYPE(), COMMON.KEY_INPUT()]):
            self.__last_error = "input error"
            return None
        if dict_args[COMMON.KEY_INPUT_TYPE()] not in self._INPUT_TYPE_MAPPER:
            self.__last_error = "input type error"
            return None
        input_file, v_list, func = self._INPUT_TYPE_MAPPER[dict_args[COMMON.KEY_INPUT_TYPE()]]
        dict_args[COMMON.KEY_INPUT()][COMMON.KEY_FILE()] = input_file
        if not common.exist_keys(dict_msg=dict_args[COMMON.KEY_INPUT()], validate_list=v_list):
            self.__last_error = "input key error"
            return None
        func(self, **dict_args)
        return dict_args[COMMON.KEY_INPUT()] if self.__last_error == "none" else None

    def check_output(self, dict_args: dict):
        if dict_args is None or len(dict_args) == 0:
            self.__last_error = "dictionary error"
            return None
        if not common.exist_keys(dict_msg=dict_args, validate_list=[COMMON.KEY_OUTPUT_TYPE(), COMMON.KEY_OUTPUT()]):
            self.__last_error = "output error"
            return None
        if dict_args[COMMON.KEY_OUTPUT_TYPE()] not in self._OUTPUT_TYPE_MAPPER:
            self.__last_error = "output type error"
            return None
        output_file, v_list, func = self._OUTPUT_TYPE_MAPPER[dict_args[COMMON.KEY_OUTPUT_TYPE()]]
        dict_args[COMMON.KEY_OUTPUT()][COMMON.KEY_FILE()] = output_file
        if not common.exist_keys(dict_msg=dict_args[COMMON.KEY_OUTPUT()], validate_list=v_list):
            self.__last_error = "output key error"
            return None
        func(self, **dict_args)
        return dict_args[COMMON.KEY_OUTPUT()] if self.__last_error == "none" else None

    def get_last_error(self):
        return self.__last_error
