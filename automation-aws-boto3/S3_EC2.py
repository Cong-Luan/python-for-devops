#Import module
import logging
import boto3
from botocore.exceptions import ClientError, BotoCoreError
import os

#Using logging to record and print to terminal and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("aws.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

#Tạo class
class AWS:
#Thêm hàm __init__ và các thuộc tính
    def __init__(self, region = None):
        self.session = boto3.session.Session(region_name = region)
        self.region = self.session.region_name
        self.s3 = self.session.client("s3")
        self.ec2 = self.session.client("ec2")

#Function list_buckets
    def list_buckets(self):
        response = self.s3.list_buckets()
        return [bucket['Name'] for bucket in response.get('Buckets', [])]

#Function list_region
    def list_region(self):
        response = self.ec2.describe_regions()
        return [region['RegionName'] for region in response['Regions']]

#Function create bucket
    def create_bucket(self, bucket_name, region = None):
        region = region or self.region
        s3 = self.s3 if region == self.region else self.session.client("s3", region_name = region)
        params = {"Bucket": bucket_name}

        if region != "us-east-1":
            params['CreateBucketConfiguration'] = {"LocationConstraint": region}
        
        try:
            s3.create_bucket(**params)
            logger.info(f"Bucket {bucket_name} đã tạo thành công vùng {region}")
            return True
        except ClientError as exc:
            logger.error(f"Error:{exc}")
            return False
#Function upload file
    def upload_file(self, file_path, bucket, key):
        if not os.path.isfile(file_path):
            logger.error(f"Error: File {file_path} không tồn tại")
            return False

        try:
            self.s3.upload_file(file_path, bucket, key)
            logger.info(f"File {file_path} đã upload thành công")
            return True
        except (BaseException, ClientError) as exc:
            logger.error(f"Error:{exc}")
            return False

def main():
    try:
        aws = AWS()
        logger.info(f"Vùng: {aws.region}")

        logger.info("S3 bucket:")
        for name in aws.list_buckets():
            logger.info(f'    - {name}')
        
        logger.info("Regions: ")
        for name in aws.list_region():
            logger.info(f"    - {name}")
    except (BotoCoreError, ClientError) as exc:
        logger.error(f"Error: {exc}")

if __name__ == "__main__":
    main()