import logging
import boto3

from innotter.settings import (
    LOCALSTACK_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    S3_BUCKET,
    AWS_DEFAULT_REGION,
    AWS_PROFILE,
    ALLOWED_FILE_EXTENSIONS,
    SOURCE_EMAIL
)


boto3.set_stream_logger('botocore', level=logging.DEBUG)

boto3.setup_default_session(profile_name=AWS_PROFILE,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_DEFAULT_REGION)

s3_client = boto3.client("s3", region_name=AWS_DEFAULT_REGION, endpoint_url=LOCALSTACK_ENDPOINT_URL)

ses_client = client = boto3.client('ses', region_name=AWS_DEFAULT_REGION, endpoint_url=LOCALSTACK_ENDPOINT_URL)
ses_client.verify_email_identity(EmailAddress=SOURCE_EMAIL)


def get_file_extension(file) -> str:
    return file.name.split('.')[-1]


def is_allowed_file_extension(extension: str) -> bool:
    return extension in ALLOWED_FILE_EXTENSIONS


def upload_file_to_s3(key, file_path):
    extension = get_file_extension(file_path)
    if not is_allowed_file_extension(extension):
        return

    s3_client.put_object(
        Body=file_path,
        Bucket=S3_BUCKET,
        Key=(key + '.' + extension),
    )

    return key + '.' + extension


def get_presigned_url(key):
    if not key:
        return

    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': key},
        ExpiresIn=3600
    )


def send_email(post_owner, followers_emails: list):
    ses_client.send_email(
        Source=SOURCE_EMAIL,
        Destination={'ToAddresses': followers_emails},
        Message={
            'Subject': {
                'Data': f'Do not pass new post from {post_owner}! ',
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': f'{post_owner} has published a new post',
                    'Charset': 'utf-8'
                },
            }
        }
    )
