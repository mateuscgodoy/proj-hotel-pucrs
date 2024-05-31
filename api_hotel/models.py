from django.db import models

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=50, blank=True, null=True
    )  # Para distinguir entre Customer e Employee

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name[0]}."


class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_capacity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class RoomInstance(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.CharField(
        max_length=100, help_text="The code representing each individual room."
    )
    is_occupied = models.BooleanField(default=False)
    allow_pets = models.BooleanField(default=False)

    class Meta:
        ordering = ["room"]

    def __str__(self):
        return f"{self.room} - {'Occupied' if self.is_occupied else 'Free' }"


class Reservation(models.Model):
    guest = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reservations"
    )
    room = models.ForeignKey(RoomInstance, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    date_in = models.DateField()
    date_out = models.DateField()

    def __str__(self):
        return f"Room: {self.room} from {self.date_in} to ${self.date_out}. Guest: {self.guest}"


class Payment(models.Model):
    guest = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"${self.amount} from {self.guest} on {self.payment_date}"


class Transaction(models.Model):
    guest = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment} for {self.reservation}"
