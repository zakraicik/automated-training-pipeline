# Use a standard Python base image
FROM python:3.11-slim-buster

# Install necessary libraries: requests, boto3, scikit-learn, pandas, numpy, etc.
RUN pip install requests boto3 scikit-learn pandas numpy

# No need to copy any Python script here since it will be provided from S3 at runtime

# Set working directory
WORKDIR /app

# Set a default CMD or ENTRYPOINT in case you want to run the container for testing, but this isn't strictly necessary
# since the Processing job will override this with ContainerEntrypoint from your Lambda function
CMD ["python", "-c", "print('Container started successfully')"]