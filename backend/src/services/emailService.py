import boto3
from fastapi import HTTPException, status
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import json
import os


load_dotenv()

SUBJECT = "API Gateway"
BODY_TEXT = "API Gateway test"
AWS_REGION = os.getenv("AWS_REGION")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID") 

client = boto3.client("ses",
                    region_name=AWS_REGION,
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY)



def send_email( user_data = None, subject: str = SUBJECT, body: str = BODY_TEXT):

    if user_data:
        user_info = user_data.to_dict()
        user_info = json.dumps(user_info)
        user_info = "Data received from API Gateway:\n" + user_info
    else:
        user_info = body

    try:
        response = client.send_email(
            Destination={"ToAddresses": ["ryanchanenator@gmail.com"],},
            Message={"Body": {"Text": {"Data": user_info,},},
                    "Subject": {"Data": subject,},},
            Source="APIAdmin@ryanchanwy.cyou",
        )
        print("Email sent"),
    except ClientError as e:
        print(str(e.response["Error"]))
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e.response["Error"]}")
    