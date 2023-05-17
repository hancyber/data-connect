exec:
  max_threads: {{ EXEC.MAX_THREADS if EXEC and EXEC.MAX_THREADS else 8 }}
  min_output_tasks: {{ EXEC.MIN_OUTPUT_TASKS if EXEC and EXEC.MIN_OUTPUT_TASKS else 1 }}
{% if INPUT and INPUT.FILE %}
{% include INPUT.FILE ignore missing +%}
{% endif %}
{% if OUTPUT and OUTPUT.FILE %}
{% include OUTPUT.FILE ignore missing +%}
{% endif %}