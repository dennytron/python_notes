"""AWS functions"""
import json
from typing import Any
from collections.abc import Mapping
from pathlib import Path

import boto3
from boto3_type_annotations.s3 import Client


def get_secret(secret_name: str) -> str:
    """Get a password!"""
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name="us-east-2")
    response = client.get_secret_value(SecretId=secret_name)

    secret: Mapping[str, str] = json.loads(response["SecretString"])
    host: str = secret["host"]
    dbname: str = secret["dbname"]
    user: str = secret["username"]
    password: str = secret["password"]

    return f"host={host} dbname={dbname} user={user} password={password}"


def download_dir_from_s3(bucket: str, prefix: str, out_dir: Path) -> bool:
    """Download all files from a directory"""
    client: Client = boto3.client("s3")
    objects: dict[Any, Any] = client.list_objects(Bucket=bucket, Prefix=prefix)['Contents']

    for obj in objects:
        key: str = obj['Key']

        if not key.endswith(prefix + "/"):
            if not out_dir.exists():
                out_dir.mkdir(parents=True)
            out_file: str = str(out_dir) + "/" + key.split("/")[-1]
            client.download_file(bucket, key, out_file)

    return out_dir.exists()


def del_from_s3(bucket: str, prefix: str, suffix: str) -> None:
    """delete files from an s3 bucket based on prefix and suffix"""
    client: Client = boto3.client('s3')
    listing: dict[Any, Any] = client.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if "Contents" in listing:
        files: tuple[str, ...] = tuple(
            item["Key"]
            for item in listing["Contents"]
            if item["Key"].endswith(suffix)
        )

        for path in files:
            client.delete_object(Bucket=bucket, Key=path)


def download_from_s3(in_path: str, out_path: Path) -> Path:
    """
    Download a file from S3
    :param in_path:
    :param out_path:
    :return: local path of the file
    """
    print(f"Downloading {in_path}")
    bucket: str = in_path.replace("s3://", "").split("/")[0]
    key: str = in_path.split(bucket + "/")[-1]
    file_name: str = key.split("/")[-1]

    out_abs: str = str(out_path.absolute())
    out_file: str = out_abs + "/" + file_name

    s3_client: Client = boto3.client("s3")
    s3_client.download_file(bucket, key, out_file)

    return Path(out_file)


def upload_to_s3(in_path: Path, out_path: str) -> None:
    """
    Upload a file to S3
    :param in_path:
    :param out_path:
    :return: error code
    """
    bucket: str = out_path.replace("s3://", "").split("/")[0]
    key: str = out_path.replace("s3://", "").split(bucket)[-1].lstrip("/")

    print(f"Uploading to bucket={bucket} key={key}")
    in_abs: str = str(in_path.absolute())

    s3_client: Client = boto3.client("s3")
    s3_client.upload_file(in_abs, bucket, key)
