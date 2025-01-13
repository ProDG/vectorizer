from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.defs import CalculationDevice


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')

    device: CalculationDevice = CalculationDevice.cpu
    auth_token: str = 'not set'


settings = AppSettings()
