from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    host_name: str
    host_port: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    class Config:
        env_file = "../.env"
