import os
from app.configs.database import DataBaseSettings
from app.configs.general import GeneralSettings
from app.configs.message_broker import MessageBrokerSettings


class Settings(DataBaseSettings,
               MessageBrokerSettings,
               GeneralSettings):
    
    def _print_value_sources(self):
        """
            Debug function
        """
        for field in self.model_fields:
            env_value = os.environ.get(field)
            file_value = self.__getattribute__(field)
            print(f"{field}:")
            print(f"  Environment: {env_value}")
            print(f"  Config Value: {file_value}")
            print(f"  Source: {'Environment' if env_value == file_value else '.env.local or .env'}")

