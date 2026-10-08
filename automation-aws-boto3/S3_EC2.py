#Import module
import boto3
from botocore.exceptions import ClientError, BotoCoreError
#Tạo class
class AWS:
#Thêm hàm __init__ và các thuộc tính
    def __init__(seft, region_name = None):
        session = boto3.session.Session(region_name = region_name)
        seft.s3 = session.client("s3")
        seft.ec2 = session.resource("ec2")
#Function
    def list_buckets(self):
        response = self.s3.list_buckets()
        return [bucket['Name'] for bucket in response.get('Buckets', [])]
    
        