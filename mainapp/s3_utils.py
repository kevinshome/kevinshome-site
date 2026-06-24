import io
import boto3
from botocore.config import Config

BUCKET_NAME = 'khcsrv-bucket'

def _s3_list_bucket():
    s3 = boto3.resource('s3')
    csrv_bucket = s3.Bucket(BUCKET_NAME)
    items = [item.key for item in csrv_bucket.objects.all()]
    return items

def _s3_get_presign_url(file: str):
    s3 = boto3.client(
        's3',
        region_name="us-east-1",
        config=Config(
            signature_version='s3v4',
            s3={'addressing_style': 'virtual'},
        ),
    )

    response = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': f"{file}"},
            ExpiresIn=60*5, # url is good for 5 minutes
        )

    s3.close()
    return response

def _s3_dl2ibuf(file: str):
    ibuf = io.BytesIO()
    s3 = boto3.client('s3')
    s3.download_fileobj(BUCKET_NAME, f'{file}', ibuf)
    ibuf.seek(0) # rewind object
    s3.close()
    return ibuf

def _s3_upload_file(fileobj, filename):
    s3 = boto3.client('s3')
    s3.upload_fileobj(fileobj, BUCKET_NAME, filename)
    s3.close()
    return