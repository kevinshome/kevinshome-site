import io
import boto3
from botocore.config import Config

def _s3_list_bucket():
    s3 = boto3.resource('s3')
    csrv_bucket = s3.Bucket("khcsrv-bucket")
    items = [item.key for item in csrv_bucket.objects.all()]
    return items

def _s3_get_presign_url(file: str):
    s3_client = boto3.client(
        's3',
        region_name="us-east-1",
        config=Config(
            signature_version='s3v4',
            s3={'addressing_style': 'virtual'},
        ),
    )

    response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': "khcsrv-bucket", 'Key': f"{file}"},
            ExpiresIn=60*5, # url is good for 5 minutes
        )

    return response

def _s3_dl2ibuf(file: str):
    ibuf = io.BytesIO()
    s3 = boto3.client('s3')
    s3.download_fileobj('khcsrv-bucket', f'{file}', ibuf)
    ibuf.seek(0) # rewind object
    return ibuf