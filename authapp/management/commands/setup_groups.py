from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Create default user groups for the real estate platform'

    def handle(self, *args, **options):
        """Create default groups with appropriate permissions"""
        
        groups_data = [
            {
                'name': 'Buyers',
                'description': 'Property buyers with basic access',
                'permissions': [
                    'view_property',
                    'add_propertyinquiry',
                    'view_propertyinquiry',
                    'add_propertyfavorite',
                    'view_propertyfavorite',
                    'delete_propertyfavorite',
                    'add_propertyreview',
                    'view_propertyreview',
                ]
            },
            {
                'name': 'Sellers',
                'description': 'Property sellers with listing capabilities',
                'permissions': [
                    'view_property',
                    'add_property',
                    'change_property',
                    'delete_property',
                    'view_propertyinquiry',
                    'add_propertyimage',
                    'change_propertyimage',
                    'delete_propertyimage',
                    'add_propertyvideo',
                    'change_propertyvideo',
                    'delete_propertyvideo',
                    'add_virtualtour',
                    'change_virtualtour',
                    'delete_virtualtour',
                ]
            },
            {
                'name': 'Agents',
                'description': 'Real estate agents with full property management',
                'permissions': [
                    'view_property',
                    'add_property',
                    'change_property',
                    'delete_property',
                    'view_propertyinquiry',
                    'change_propertyinquiry',
                    'add_propertyimage',
                    'change_propertyimage',
                    'delete_propertyimage',
                    'add_propertyvideo',
                    'change_propertyvideo',
                    'delete_propertyvideo',
                    'add_virtualtour',
                    'change_virtualtour',
                    'delete_virtualtour',
                    'view_customuser',
                ]
            },
            {
                'name': 'Developers',
                'description': 'Property developers with project management',
                'permissions': [
                    'view_property',
                    'add_property',
                    'change_property',
                    'delete_property',
                    'view_project',
                    'add_project',
                    'change_project',
                    'delete_project',
                    'view_projectphase',
                    'add_projectphase',
                    'change_projectphase',
                    'delete_projectphase',
                    'view_projectdocument',
                    'add_projectdocument',
                    'change_projectdocument',
                    'delete_projectdocument',
                    'add_propertyimage',
                    'change_propertyimage',
                    'delete_propertyimage',
                    'add_propertyvideo',
                    'change_propertyvideo',
                    'delete_propertyvideo',
                    'add_virtualtour',
                    'change_virtualtour',
                    'delete_virtualtour',
                ]
            },
            {
                'name': 'Admins',
                'description': 'Platform administrators with full access',
                'permissions': []  # Will get all permissions
            }
        ]

        for group_data in groups_data:
            group, created = Group.objects.get_or_create(name=group_data['name'])
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Group already exists: {group.name}')
                )

            # Clear existing permissions
            group.permissions.clear()

            # Add permissions for Admins (all permissions)
            if group.name == 'Admins':
                all_permissions = Permission.objects.all()
                group.permissions.set(all_permissions)
                self.stdout.write(
                    self.style.SUCCESS(f'Added all permissions to {group.name}')
                )
            else:
                # Add specific permissions for other groups
                permissions_to_add = []
                for perm_codename in group_data['permissions']:
                    try:
                        permission = Permission.objects.get(codename=perm_codename)
                        permissions_to_add.append(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Permission {perm_codename} not found for group {group.name}'
                            )
                        )

                if permissions_to_add:
                    group.permissions.set(permissions_to_add)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Added {len(permissions_to_add)} permissions to {group.name}'
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully set up default user groups!')
        )