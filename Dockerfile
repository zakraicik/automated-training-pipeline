# Use a base image with Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Install dependencies (if any)
RUN pip install requests boto3

# Copy your function code from the src/data directory to the Lambda task root directory
COPY src/data/fetch_iris_data.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["fetch_iris_data.lambda_handler"]
