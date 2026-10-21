aws glue create-job \
  --name banking-dq-job \
  --role GlueBankingDQRole \
  --glue-version "3.0" \
  --command '{"Name":"pythonshell","PythonVersion":"3.9","ScriptLocation":"s3://nandasamsu-banking-dq/code/aws_job.py"}' \
  --max-capacity 0.0625 \
  --default-arguments '{"library-set":"analytics","--extra-py-files":"s3://nandasamsu-banking-dq/code/banking_dq-0.1.0-py3-none-any.whl"}'