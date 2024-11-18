import os

from pydantic_settings import BaseSettings


class GeneralSettings(BaseSettings):

    class Config:
        extra = 'allow'
