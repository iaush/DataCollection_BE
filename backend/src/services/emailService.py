import boto3
from botocore.exceptions import ClientError

SENDER = "ryanchanenator@gmail.com"
SUBJECT = "API Gateway"
BODY_TEXT = "Data received from API Gateway"

client = boto3.client("ses")



def send_email( send_to: str, subject: str = SUBJECT, body: str = BODY_TEXT):
    try:
        response = client.send_email(
            Destination={"ToAddresses": [send_to,],},
            Message={"Body": {"Text": {"Data": body,},},
                    "Subject": {"Data": subject,},},Source=SENDER,
        )
        print("Email sent"),
    except ClientError as e:
        print(e.response["Error"]["Message"])
        
    
