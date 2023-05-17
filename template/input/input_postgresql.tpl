in:
  type: postgresql
  host: {{ INPUT.HOST }}
  port: {{ INPUT.PORT }}
  user: {{ INPUT.USER }}
  password: {{ INPUT.PASSWORD }}
  database: {{ INPUT.DATABASE }}
  schema: {{ INPUT.SCHEMA }}
  query: |
    {{ INPUT.QUERY }}