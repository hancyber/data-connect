in:
  type: mysql
  host: {{ INPUT.HOST }}
  port: {{ INPUT.PORT }}
  user: {{ INPUT.USER }}
  password: {{ INPUT.PASSWORD }}
  database: {{ INPUT.DATABASE }}
  query: |
    {{ INPUT.QUERY }}