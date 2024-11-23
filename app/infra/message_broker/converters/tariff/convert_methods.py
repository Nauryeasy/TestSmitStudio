from app.domain.events.tariff import UpdateTariffEvent
from app.domain.tariff import Tariff


def convert_entity_to_message(entity: Tariff) -> dict:
    return {
        'oid': entity.oid,
        'date': str(entity.date),
        'rate': entity.rate,
        'cargo_type': entity.cargo_type
    }


def convert_update_tariff_event_to_message(event: UpdateTariffEvent) -> dict:
    return {
        'oid': event.oid,
        'created_at': str(event.created_at),
        'type': 'UpdateTariffEvent',
        'entity': convert_entity_to_message(event.entity),
        'new_entity': convert_entity_to_message(event.new_entity)
    }


def convert_delete_tariff_event_to_message(event: UpdateTariffEvent) -> dict:
    return {
        'oid': event.oid,
        'created_at': str(event.created_at),
        'type': 'DeleteTariffEvent',
        'entity': convert_entity_to_message(event.entity)
    }
