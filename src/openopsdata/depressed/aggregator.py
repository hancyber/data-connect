from src.openopsdata import AggregationHelper


class Aggregator:
    __dict_args = {}
    __return_msg = ""

    def execute(self, msg):
        helper = AggregationHelper()
        self.__dict_args = helper.check_msg(msg=msg)
        if self.__dict_args:
            if self.__dict_args["MSG_TYPE"] == "AGGR":
                if self.__dict_args["MSG_SUBTYPE"] == "CONFIG":
                    pass
                elif self.__dict_args["MSG_SUBTYPE"] == "PREVIEW":
                    pass
                elif self.__dict_args["MSG_SUBTYPE"] == "RUN":
                    pass
                else:
                    self.__return_msg = "unknown subtype"
            else:
                self.__return_msg = helper.get_last_error()
        else:
            self.__return_msg = helper.get_last_error()

    def __exec_config(self, helper):
        if helper.check_config():
            pass
        else:
            self.__return_msg = helper.get_last_error()
