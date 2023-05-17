from pydantic import BaseModel
from typing import Optional


class BaseFormat(BaseModel):
    CUSTOMER_ID: str = "0"
    PROJECT_ID: str = "0"
    CREATE_DATE: str = ""
    REQUEST_DATE: str = ""
    MSG_TYPE: str = "AGGR"
    MSG_SUBTYPE: str
    NAME: str
    VERSION: str
    SYNC_TYPE: Optional[str] = "ASYNC"
    ASYNC_CALLBACK_TYPE: Optional[str] = "CONSOLE"
    PRE_ACTION: Optional[str]


class TestInfo(BaseModel):
    HOST: str = "localhost"
    PORT: int = 19999


class ExecFormat(BaseModel):
    MAX_THREADS: Optional[int] = None
    MIN_OUTPUT_TASKS: Optional[int] = None


class InputFormat(BaseModel):
    INPUT_TYPE: str


class OutputFormat(BaseModel):
    OUTPUT_TYPE: str


class FormatterFormat(BaseModel):
    TYPE: Optional[str] = "csv"


class InputFormatterFormat(FormatterFormat):
    pass


class OutputFormatterFormat(FormatterFormat):
    pass


class MysqlInput(BaseModel):
    HOST: str
    PORT: int = 3306
    USER: str
    PASSWORD: str
    DATABASE: str
    QUERY: str


class OracleInput(BaseModel):
    URL: str
    USER: str
    PASSWORD: str
    QUERY: str


class AzureBlobInput(BaseModel):
    ACCOUNT_NAME: str
    ACCOUNT_KEY: str
    CONTAINER: str
    PATH_PREFIX: str


class BigqueryInput(BaseModel):
    PROJECT: str
    KEYFILE: str
    SQL: str


class PostgresqlInput(MysqlInput):
    PORT: int = 5432
    SCHEMA: str = "public"


class SqlserverInput(MysqlInput):
    PORT: int = 1433
    INSTANCE: str = ""


class MysqlInputFormat(InputFormat):
    INPUT_TYPE = "mysql"
    INPUT: MysqlInput


class AzureBlobInputFormat(InputFormat):
    INPUT_TYPE = "azure_blob"
    INPUT: AzureBlobInput


class PostgresqlInputFormat(InputFormat):
    INPUT_TYPE = "postgresql"
    INPUT: PostgresqlInput


class OracleInputFormat(InputFormat):
    INPUT_TYPE = "oracle"
    INPUT: OracleInput


class SqlserverInputFormat(InputFormat):
    INPUT_TYPE = "sqlserver"
    INPUT: SqlserverInput


class BigqueryInputFormat(InputFormat):
    INPUT_TYPE = "bigquery"
    INPUT: BigqueryInput


class S3Output(BaseModel):
    FILE_EXT: Optional[str] = ".csv"
    BUCKET: str = ""
    ENDPOINT: str = ""
    ACCESS_KEY_ID: str = ""
    SECRET_ACCESS_KEY: str = ""
    FORMATTER: OutputFormatterFormat


class FileOutput(BaseModel):
    ROOT_PATH: str = ""
    FILE_EXT: Optional[str] = "csv"
    FORMATTER: OutputFormatterFormat


class S3OutputFormat(OutputFormat):
    OUTPUT_TYPE = "s3"
    OUTPUT: S3Output


class FileOutputFormat(OutputFormat):
    OUTPUT_TYPE = "file"
    OUTPUT: FileOutput


class ConfigFormat(BaseFormat):
    EXEC: ExecFormat = None


class MysqlS3ConfigFormat(S3OutputFormat, MysqlInputFormat, ConfigFormat, TestInfo):
    pass


class MysqlFileConfigFormat(FileOutputFormat, MysqlInputFormat, ConfigFormat, TestInfo):
    pass


class AzureBlobS3ConfigFormat(S3OutputFormat, AzureBlobInputFormat, ConfigFormat, TestInfo):
    pass


class AzureBlobFileConfigFormat(FileOutputFormat, AzureBlobInputFormat, ConfigFormat, TestInfo):
    pass


class PostgresqlS3ConfigFormat(S3OutputFormat, PostgresqlInputFormat, ConfigFormat, TestInfo):
    pass


class PostgresqlFileConfigFormat(FileOutputFormat, PostgresqlInputFormat, ConfigFormat, TestInfo):
    pass


class OracleS3ConfigFormat(S3OutputFormat, OracleInputFormat, ConfigFormat, TestInfo):
    pass


class OracleFileConfigFormat(FileOutputFormat, OracleInputFormat, ConfigFormat, TestInfo):
    pass


class SqlserverS3ConfigFormat(S3OutputFormat, SqlserverInputFormat, ConfigFormat, TestInfo):
    pass


class SqlserverFileConfigFormat(FileOutputFormat, SqlserverInputFormat, ConfigFormat, TestInfo):
    pass


class BigqueryS3ConfigFormat(S3OutputFormat, BigqueryInputFormat, ConfigFormat, TestInfo):
    pass


class BigqueryFileConfigFormat(FileOutputFormat, BigqueryInputFormat, ConfigFormat, TestInfo):
    pass
