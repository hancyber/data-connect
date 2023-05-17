in:
  type: oracle
  driver_path: /home/hgb/lib/ojdbc8-full/ojdbc8.jar
  url: {{ INPUT.URL }}
  user: {{ INPUT.USER }}
  password: {{ INPUT.PASSWORD }}
  query: |
    {{ INPUT.QUERY }}