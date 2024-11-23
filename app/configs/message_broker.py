from app.configs.general import GeneralSettings


class MessageBrokerSettings(GeneralSettings):

    KAFKA_HOST: str
    KAFKA_PORT: int
