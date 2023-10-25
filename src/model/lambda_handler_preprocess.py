import boto3
import datetime


def lambda_handler(event, context):
    sagemaker_client = boto3.client("sagemaker")

    # Parameters for the processing job
    job_name = "iris-preprocessing-job-" + datetime.datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )
    role_arn = "arn:aws:iam::682355783671:role/service-role/AmazonSageMaker-ExecutionRole-20231023T125013"
    image_uri = (
        "682355783671.dkr.ecr.us-east-1.amazonaws.com/preprocess-iris-data:latest"
    )
    input_s3_uri = "s3://automated-training-pipeline/data/iris.data"
    preprocess_s3_uri = "s3://automated-training-pipeline/modeling/preprocess.py"
    output_s3_uri = "s3://automated-training-pipeline/data/"

    response = sagemaker_client.create_processing_job(
        ProcessingJobName=job_name,
        RoleArn=role_arn,
        ProcessingInputs=[
            {
                "InputName": "input-1",
                "S3Input": {
                    "S3Uri": input_s3_uri,
                    "LocalPath": "/opt/ml/processing/input",
                    "S3DataType": "S3Prefix",
                    "S3InputMode": "File",
                    "S3DataDistributionType": "FullyReplicated",
                    "S3CompressionType": "None",
                },
            },
            {
                "InputName": "code",
                "S3Input": {
                    "S3Uri": preprocess_s3_uri,
                    "LocalPath": "/opt/ml/processing/code",
                    "S3DataType": "S3Prefix",
                    "S3InputMode": "File",
                    "S3DataDistributionType": "FullyReplicated",
                    "S3CompressionType": "None",
                },
            },
        ],
        ProcessingOutputConfig={
            "Outputs": [
                {
                    "OutputName": "output-1",
                    "S3Output": {
                        "S3Uri": output_s3_uri,
                        "LocalPath": "/opt/ml/processing/output",
                        "S3UploadMode": "EndOfJob",
                    },
                }
            ]
        },
        ProcessingResources={
            "ClusterConfig": {
                "InstanceCount": 1,
                "InstanceType": "ml.t3.medium",
                "VolumeSizeInGB": 5,
            }
        },
        AppSpecification={
            "ImageUri": image_uri,
            "ContainerArguments": [
                "--input-data",
                "/opt/ml/processing/input/iris.data",
                "--output-data",
                "/opt/ml/processing/output",
            ],
            "ContainerEntrypoint": ["python3", "/opt/ml/processing/code/preprocess.py"],
        },
    )

    return {"statusCode": 200, "body": response}
