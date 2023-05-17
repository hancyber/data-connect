import json

from openopsredis.mredis import OpenopsRedis


def get_tuple_list(tuple_string: str):
    tuple_list: list = []
    for x in tuple_string.split(","):
        y = x.split(":")
        if len(y) == 2:
            tuple_list.append((y[0].strip(), y[1].strip()))
    return tuple_list


class RedisClient:
    def __init__(self,
                 service_name="redis-service",
                 server_info="redis-sentinel-service:26379",
                 ssl_ca_certs="/etc/tls/certs/rootca.crt"):
        server = get_tuple_list(server_info) if server_info else [("redis-sentinel-service", 26379)]
        self.__redis_client = OpenopsRedis(service_name=service_name, server=server, ssl_ca_certs=ssl_ca_certs)

    def test_redis(self, msg: dict, channel="dc-gateway"):
        try:
            callback_channel = msg["CUSTOMER_ID"] + msg["PROJECT_ID"] + \
                               msg["MSG_TYPE"] + msg["MSG_SUBTYPE"] + msg["NAME"] + msg["VERSION"]
            observer = self.__redis_client.subscribe(callback_channel)

            msg["ASYNC_CALLBACK_TYPE"] = "REDIS"
            data = json.dumps(msg)
            self.__redis_client.rpush(channel, data)

            # add timeout-break
            while True:
                message = observer.get_message()
                if message and message['type'] == 'message':
                    ret_msg = message['data'].decode('utf-8')
                    break
            observer.unsubscribe()

            return ret_msg
        except Exception as err:
            return str(err)
