import boto3
from botocore.exceptions import ClientError

AWS_REGION = "ap-southeast-1"
SENDER = "ryanchanenator@gmail.com"
SUBJECT = "API Gateway"
BODY_TEXT = "Data received from API Gateway"

client = boto3.client("ses", region_name=AWS_REGION)


def send_email(subject: str, body: str, send_to: str):
    try:
        response = client.send_email(
            Destination={"ToAddresses": [send_to,],},
            Message={"Body": {"Text": {"Data": body,},},
                    "Subject": {"Data": subject,},},Source=SENDER,
        )
        print("Email sent"),
    except ClientError as e:
        print(e.response["Error"]["Message"])
        
    
