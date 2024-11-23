import json
from abc import abstractmethod
from dataclasses import dataclass

from confluent_kafka import Producer

from app.configs import Settings
from app.domain.events.base import BaseEvent
from app.infra.message_broker.converters.tariff.tariff_converter import TariffEventConverter
from app.infra.message_broker.producer.base import BaseProducer


@dataclass
class BaseTariffProducer(BaseProducer):

    @abstractmethod
    def produce(self, event: BaseEvent) -> None:
        ...


@dataclass
class KafkaTariffProducer(BaseTariffProducer):

    settings: Settings
    converter: TariffEventConverter
    topic = 'tariff_actions'

    def __post_init__(self):
        self.kafka_host = self.settings.KAFKA_HOST
        self.kafka_port = self.settings.KAFKA_PORT
        kafka_config = {
            'bootstrap.servers': f'{self.kafka_host}:{self.kafka_port}',
        }
        self.producer = Producer(kafka_config)

    def produce(self, event: BaseEvent) -> None:
        message = self.converter.convert_event_to_message(event)

        self.producer.produce(self.topic, key=message['oid'], value=json.dumps(message).encode('utf-8'))
        self.producer.poll(0)
