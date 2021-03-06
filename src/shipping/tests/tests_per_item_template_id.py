import pytest
from django.core.exceptions import ImproperlyConfigured

from shipping.shipments import RecordShipment

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def record(mixer):
    return lambda template_id: mixer.blend('courses.Record', template_id=template_id)


@pytest.fixture
def shipment(user):
    return lambda stuff: RecordShipment(user, stuff=stuff)


@pytest.mark.parametrize('template_id, expected', [
    [None, 'purchased-record'],  # the default one
    [100500, '100500'],
])
def test(record, shipment, template_id, expected):
    record = record(template_id=template_id)

    shipment = shipment(record)

    assert shipment.get_template_id() == expected


def test_zero_template_id(record, shipment):
    shipment = shipment(record)

    shipment.template_id = None

    with pytest.raises(ImproperlyConfigured):
        shipment.get_template_id()
