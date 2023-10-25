import boto3
import datetime


def lambda_handler(event, context):
    sagemaker_client = boto3.client("sagemaker")

    # Define parameters for the training job
    job_name = "iris-training-job-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    role_arn = "arn:aws:iam::682355783671:role/service-role/AmazonSageMaker-ExecutionRole-20231023T125013"  # Update the ARN as required

    # Image URI for Linear Learner in 'us-east-1'
    image_uri = "382416733822.dkr.ecr.us-east-1.amazonaws.com/linear-learner:1"

    training_data_s3_uri = "s3://automated-training-pipeline/data/train_data.csv"
    output_s3_uri = "s3://automated-training-pipeline/models/"

    response = sagemaker_client.create_training_job(
        TrainingJobName=job_name,
        RoleArn=role_arn,
        AlgorithmSpecification={
            "TrainingImage": image_uri,
            "TrainingInputMode": "File",
        },
        InputDataConfig=[
            {
                "ChannelName": "train",
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": training_data_s3_uri,
                        "S3DataDistributionType": "FullyReplicated",
                    },
                },
                "ContentType": "text/csv",  # Specify that we're using CSV format
            },
        ],
        OutputDataConfig={
            "S3OutputPath": output_s3_uri,
        },
        ResourceConfig={
            "InstanceCount": 1,
            "InstanceType": "ml.m5.large",
            "VolumeSizeInGB": 5,
        },
        HyperParameters={
            "predictor_type": "multiclass_classifier",
            "num_classes": "3",
            "mini_batch_size": "30",
        },
        StoppingCondition={
            "MaxRuntimeInSeconds": 3600,
        },
    )

    return {"statusCode": 200, "body": response}
