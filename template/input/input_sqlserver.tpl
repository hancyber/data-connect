in:
  type: sqlserver
  driver_path: /home/hgb/lib/sqljdbc_9.4/kor/mssql-jdbc-9.4.0.jre11.jar
  host: {{ INPUT.HOST }}
  user: {{ INPUT.USER }}
  port: {{ INPUT.PORT }}
  password: {{ INPUT.PASSWORD }}
  instance: {{ INPUT.INSTANCE if INPUT.INSTANCE else '' }}
  database: {{ INPUT.DATABASE }}
  query: |
    {{ INPUT.QUERY }}