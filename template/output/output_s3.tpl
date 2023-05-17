out:
  type: s3
  path_prefix: {{ NAME }}/{{ VERSION }}
  file_ext: {{ OUTPUT.FILE_EXT if OUTPUT.FILE_EXT else '.csv' }}
  bucket: {{ OUTPUT.BUCKET }}
  endpoint: {{ OUTPUT.ENDPOINT }}
  access_key_id: {{ OUTPUT.ACCESS_KEY_ID }}
  secret_access_key: {{ OUTPUT.SECRET_ACCESS_KEY }}
  formatter:
    type: {{ OUTPUT.FORMATTER.TYPE if OUTPUT.FORMATTER and OUTPUT.FORMATTER.TYPE else 'csv' }}