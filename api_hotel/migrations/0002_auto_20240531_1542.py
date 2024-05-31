# Generated by Django 5.0.6 on 2024-05-31 18:42

from django.db import migrations


def create_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    # Define the permissions for each group
    guest_permissions = [
        "add_reservation",
        "change_reservation",
        "delete_reservation",
        "view_reservation",
    ]
    staff_permissions = [
        "add_room",
        "change_room",
        "delete_room",
        "view_room",
        "add_customer",
        "change_user",
        "delete_user",
        "view_user",
        "add_reservation",
        "change_reservation",
        "delete_reservation",
        "view_reservation",
    ]

    # Create the Guest group and assign permissions
    guest_group, created = Group.objects.get_or_create(name="Guests")
    for perm in guest_permissions:
        permission = Permission.objects.get(codename=perm)
        guest_group.permissions.add(permission)

    # Create the Staff group and assign permissions
    staff_group, created = Group.objects.get_or_create(name="Staff")
    for perm in staff_permissions:
        permission = Permission.objects.get(codename=perm)
        staff_group.permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("api_hotel", "0001_initial"),
    ]

    operations = []