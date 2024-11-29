aws s3 cp https://text-to-image-bucket-lcl50j80.s3.us-west-2.amazonaws.com/SEdufit-Build-Project/function.zip /tmp/function.zip

aws lambda update-function-code \
  --function-name callback-lambda \
  --zip-file fileb:////tmp/function.zip
