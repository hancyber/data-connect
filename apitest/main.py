from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from dataformat import MysqlS3ConfigFormat, MysqlFileConfigFormat, \
    AzureBlobS3ConfigFormat, AzureBlobFileConfigFormat, \
    PostgresqlS3ConfigFormat, PostgresqlFileConfigFormat, \
    OracleS3ConfigFormat, OracleFileConfigFormat, \
    SqlserverS3ConfigFormat, SqlserverFileConfigFormat, \
    BigqueryS3ConfigFormat, BigqueryFileConfigFormat

from socketclient import SocketClient
from redisclient import RedisClient

app = FastAPI()


@app.get("/")
def read_root():
    return "hgb hancyberML data-connector tester"


def __socket(data):
    msg = jsonable_encoder(data)
    print(msg)
    sc = SocketClient(host=data.HOST, port=data.PORT)
    resp = sc.test_socket(msg)
    return resp


def __redis(data):
    msg = jsonable_encoder(data)
    print(msg)
    rc = RedisClient()
    resp = rc.test_redis(msg=msg)
    return resp


@app.post("/mysql/s3/socket")
def config_mysql_s3_socket(config_base: MysqlS3ConfigFormat):
    return __socket(config_base)


@app.post("/mysql/file/socket")
def config_mysql_file_socket(config_base: MysqlFileConfigFormat):
    return __socket(config_base)


@app.post("/mysql/s3/redis")
def config_mysql_s3_redis(config_base: MysqlS3ConfigFormat):
    return __redis(config_base)


@app.post("/mysql/file/redis")
def config_mysql_file_redis(config_base: MysqlFileConfigFormat):
    return __redis(config_base)


@app.post("/azure-blob/s3/socket")
def config_azure_blob_s3_socket(config_base: AzureBlobS3ConfigFormat):
    return __socket(config_base)


@app.post("/azure-blob/file/socket")
def config_azure_blob_file_socket(config_base: AzureBlobFileConfigFormat):
    return __socket(config_base)


@app.post("/azure-blob/s3/redis")
def config_azure_blob_s3_redis(config_base: AzureBlobS3ConfigFormat):
    return __redis(config_base)


@app.post("/azure-blob/file/redis")
def config_azure_blob_file_redis(config_base: AzureBlobFileConfigFormat):
    return __redis(config_base)


@app.post("/pgsql/s3/socket")
def config_pgsql_s3_socket(config_base: PostgresqlS3ConfigFormat):
    return __socket(config_base)


@app.post("/pgsql/file/socket")
def config_pgsql_file_socket(config_base: PostgresqlFileConfigFormat):
    return __socket(config_base)


@app.post("/pgsql/s3/redis")
def config_pgsql_s3_redis(config_base: PostgresqlS3ConfigFormat):
    return __redis(config_base)


@app.post("/pgsql/file/redis")
def config_pgsql_file_redis(config_base: PostgresqlFileConfigFormat):
    return __redis(config_base)


@app.post("/oracle/s3/socket")
def config_oracle_s3_socket(config_base: OracleS3ConfigFormat):
    return __socket(config_base)


@app.post("/oracle/file/socket")
def config_oracle_file_socket(config_base: OracleFileConfigFormat):
    return __socket(config_base)


@app.post("/oracle/s3/redis")
def config_oracle_s3_redis(config_base: OracleS3ConfigFormat):
    return __redis(config_base)


@app.post("/oracle/file/redis")
def config_oracle_file_redis(config_base: OracleFileConfigFormat):
    return __redis(config_base)


@app.post("/sqlserver/s3/socket")
def config_sqlserver_s3_socket(config_base: SqlserverS3ConfigFormat):
    return __socket(config_base)


@app.post("/sqlserver/file/socket")
def config_sqlserver_file_socket(config_base: SqlserverFileConfigFormat):
    return __socket(config_base)


@app.post("/sqlserver/s3/redis")
def config_sqlserver_s3_redis(config_base: SqlserverS3ConfigFormat):
    return __redis(config_base)


@app.post("/sqlserver/file/redis")
def config_sqlserver_file_redis(config_base: SqlserverFileConfigFormat):
    return __redis(config_base)


@app.post("/bigquery/s3/socket")
def config_bigquery_s3_socket(config_base: BigqueryS3ConfigFormat):
    return __socket(config_base)


@app.post("/bigquery/file/socket")
def config_bigquery_file_socket(config_base: BigqueryFileConfigFormat):
    return __socket(config_base)


@app.post("/bigquery/s3/redis")
def config_bigquery_s3_redis(config_base: BigqueryS3ConfigFormat):
    return __redis(config_base)


@app.post("/bigquery/file/redis")
def config_bigquery_file_redis(config_base: BigqueryFileConfigFormat):
    return __redis(config_base)
