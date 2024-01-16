from fastapi import UploadFile
from minio import Minio

from api.utils.setup import set_up_minio


class MinioClient():
        def __init__(self):
            self.config = set_up_minio()
            self.client = Minio(
                self.config["ENDPOINT"],
                access_key=self.config["USER"],
                secret_key=self.config["SECRET"]
            )

        def uploadToMinio(self, file: UploadFile, bucket_name: str):
            bucket_exists = self.client.bucket_exists(bucket_name)
            if not bucket_exists:
                self.client.make_bucket(bucket_name)
                print(f'Creating bucket named {bucket_name}.')
            else:
                print(f'Bucket named {bucket_name} already exists.')

            result = self.client.put_object(bucket_name, file.filename, file.file, file.size)
            return result

        def downloadFromMinio(bucket_name: str, file_name: str):
            pass