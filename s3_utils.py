import boto3
import botocore
from utils import load_yaml_config


def download_file(local, remote):
    config = load_yaml_config('certificate.yml')
    session = boto3.session.Session(aws_access_key_id=config.AWS_ACCESS_ID,
                                    aws_secret_access_key=config.AWS_SECRET_KEY)
    s3 = session.resource('s3')

    try:
        s3.Bucket(config.AWS_BUCKET).download_file(remote, local)
        print("Download " + remote + " as " + local)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print("The object does not exists")
        print("Download fail.")
        return False

def upload_file(local, remote):
    config = load_yaml_config('certificate.yml')
    session = boto3.session.Session(aws_access_key_id=config.AWS_ACCESS_ID,
                                    aws_secret_access_key=config.AWS_SECRET_KEY)
    s3 = session.client('s3')

    try:
        s3.upload_file(local, config.AWS_BUCKET, remote)
        '''
        s3.put_object(Bucket=config.AWS_BUCKET,
                      Key=remote,
                      Body=local)
        '''
        print("Upload " + local + " as " + remote)
        return True
    except:
        print("Upload fail.")
        return False


