import boto3
import requests


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    data_url = (
        "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    )
    response = requests.get(data_url)

    # Assuming the data is small enough to fit into memory
    s3.put_object(
        Bucket="automated-training-pipeline-example",
        Key="data/iris.data",
        Body=response.content,
    )
