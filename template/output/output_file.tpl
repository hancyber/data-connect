out:
  type: file
  path_prefix: {{ OUTPUT.ROOT_PATH }}/{{ NAME }}/{{ VERSION }}_
  file_ext: {{ OUTPUT.FILE_EXT if OUTPUT.FILE_EXT else 'csv' }}
  formatter:
    type: {{ OUTPUT.FORMATTER.TYPE if OUTPUT.FORMATTER and OUTPUT.FORMATTER.TYPE else 'csv' }}