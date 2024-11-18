from app.configs.general import GeneralSettings


class DataBaseSettings(GeneralSettings):

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_CONNECTOR: str = "asyncpg"
    
    @property
    def POSTGRES_URL(self) -> str:
        return f'postgresql+{self.POSTGRES_CONNECTOR}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
    
    @property
    def TEST_POSTGRES_DB(self) -> str:
        return f"test_{self.POSTGRES_DB}"

    @property
    def TEST_POSTGRES_URL(self) -> str:
        return f'postgresql+{self.POSTGRES_CONNECTOR}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.TEST_POSTGRES_DB}'
