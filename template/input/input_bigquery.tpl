in:
  type: bigquery
  project: {{ INPUT.PROJECT }}
  keyfile:
    content: |
      {{ INPUT.KEYFILE }}
  sql: |
    {{ INPUT.SQL }}
