from typing import Optional
from pydantic_settings import BaseSettings
from sqlmodel import SQLModel, create_engine, Session
import boto3
import json

# Secrets Manager에서 시크릿 값 읽기 함수
def get_secret(secret_name, region_name):
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secret = response["SecretString"]
    return json.loads(secret)

# 시크릿 이름과 리전을 환경에 맞게 지정
secret_dict = get_secret("movie/deploy", "ap-northeast-2")

# 시크릿 값으로 Settings 객체 생성
class Settings:
    DATABASE_URL: Optional[str] = secret_dict.get("DATABASE_URL")
    SECRET_KEY: Optional[str] = secret_dict.get("SECRET_KEY")
    s3_bucket: str = secret_dict.get("S3_BUCKET")
    s3_region: str = secret_dict.get("S3_REGION")
    aws_access_key_id: str = secret_dict.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = secret_dict.get("AWS_SECRET_ACCESS_KEY")
    cloudfront_url: str = secret_dict.get("CLOUDFRONT_URL")
    allowed_origins: str = secret_dict.get("ALLOWED_ORIGINS")

# class Settings(BaseSettings):
#     DATABASE_URL: Optional[str] = None
#     SECRET_KEY: Optional[str] = None
#     print(SECRET_KEY)
#     s3_bucket: str
#     s3_region: str
#     aws_access_key_id: str
#     aws_secret_access_key: str
#     cloudfront_url: str
#     allowed_origins: str
    
#     class Config:
#         env_file = ".env"

settings = Settings()
    
#database_connection_string = "mysql+pymysql://fastapiuser:p%40ssw0rd@localhost:3306/fastapidb"
engine_url = create_engine(
    settings.DATABASE_URL,
    echo=True,
)

def conn():
    SQLModel.metadata.create_all(engine_url)

def get_session():
    with Session(engine_url) as session:
        yield session