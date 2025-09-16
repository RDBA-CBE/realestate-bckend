from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group

def setup_groups(sender, **kwargs):
    groups = ['Buyer', 'Seller', 'Agent', 'Developer', 'Admin']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
