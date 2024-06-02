import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from api_hotel.models import (
    CustomUser,
    Room,
    RoomInstance,
    Reservation,
    Payment,
    Transaction,
)


@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        return CustomUser.objects.create_user(**kwargs)

    return create_user


@pytest.fixture
def room_factory(db):
    def create_room(**kwargs):
        defaults = {
            "name": "Quarto Test",
            "description": "Um quarto de teste do nosso hotel.",
            "price": 100.00,
            "max_capacity": 2,
        }
        defaults.update(kwargs)
        return Room.objects.create(**defaults)

    return create_room


@pytest.fixture
def room_instance_factory(db, room_factory):
    def create_room_instance(**kwargs):
        room_args = kwargs.pop("room", None)
        print(room_args)
        if room_args:
            room = room_factory(**room_args)
        else:
            room = room_factory()

        defaults = {
            "number": "404",
            "is_occupied": False,
            "allow_pets": False,
        }
        defaults.update(kwargs)
        return RoomInstance.objects.create(room=room, **defaults)

    return create_room_instance


@pytest.fixture
def reservation_factory(db, user_factory, room_instance_factory):
    def create_reservation(guest=None, **kwargs):
        if isinstance(guest, dict):
            guest = user_factory(**guest)
        room_instance = room_instance_factory(**kwargs.pop("room", {}))
        # room_instance = kwargs.pop("room_instance", room_instance_factory())
        return Reservation.objects.create(guest=guest, room=room_instance, **kwargs)

    return create_reservation


@pytest.fixture
def payment_factory(db, user_factory):
    def create_payment(guest=None, **kwargs):
        if isinstance(guest, dict):
            guest = user_factory(**guest)
        return Payment.objects.create(guest=guest, **kwargs)

    return create_payment


@pytest.fixture
def transaction_factory(db, user_factory, payment_factory, reservation_factory):
    def create_transaction(guest=None, **kwargs):
        if isinstance(guest, dict):
            guest = user_factory(**guest)
        payment = payment_factory(guest=guest, **kwargs.pop("payment", {}))
        reservation = reservation_factory(guest=guest, **kwargs.pop("reservation", {}))
        return Transaction.objects.create(
            guest=guest, payment=payment, reservation=reservation, **kwargs
        )

    return create_transaction


@pytest.mark.django_db
def test_create_custom_user(user_factory):
    user = user_factory(
        username="testuser", password="password123", address="Rua Test, 123"
    )
    assert CustomUser.objects.count() == 1
    assert user.address == "Rua Test, 123"


@pytest.mark.django_db
def test_create_room(room_factory):
    room = room_factory(
        name="Suite", description="Uma suite luxuosa", price=250.00, max_capacity=4
    )
    assert Room.objects.count() == 1
    assert room.name == "Suite"


@pytest.mark.django_db
def test_create_room_instance(room_instance_factory):
    room_instance = room_instance_factory(
        room={
            "name": "Suite",
            "description": "Uma suite luxuosa",
            "price": 250.00,
            "max_capacity": 4,
        },
        number="101",
        is_occupied=False,
        allow_pets=True,
    )
    assert RoomInstance.objects.count() == 1
    assert room_instance.number == "101"


@pytest.mark.django_db
def test_create_reservation(reservation_factory):
    reservation = reservation_factory(
        guest={"username": "testguest", "password": "password123"},
        room={
            "room": {
                "name": "Suite",
                "description": "Uma suite luxuosa",
                "price": 250.00,
                "max_capacity": 4,
            },
            "number": "101",
        },
        date_in="2024-06-01",
        date_out="2024-06-05",
    )
    assert Reservation.objects.count() == 1
    assert reservation.date_in == "2024-06-01"


@pytest.mark.django_db
def test_create_payment(payment_factory):
    payment = payment_factory(
        guest={"username": "testguest", "password": "password123"},
        payment_date="2024-06-01T12:00:00Z",
        amount=250.00,
    )
    assert Payment.objects.count() == 1
    assert payment.amount == 250.00


@pytest.mark.django_db
def test_create_transaction(transaction_factory):
    transaction = transaction_factory(
        guest={"username": "testguest", "password": "password123"},
        payment={"amount": 250.00, "payment_date": "2024-06-01T12:00:00Z"},
        reservation={"date_in": "2024-06-01", "date_out": "2024-06-05"},
    )
    assert Transaction.objects.count() == 1
    assert transaction.payment.amount == 250.00
    assert transaction.guest.username == "testguest"
