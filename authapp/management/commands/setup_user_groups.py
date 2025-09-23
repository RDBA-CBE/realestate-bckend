from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class Command(BaseCommand):
    help = 'Create user groups and assign permissions for real estate platform'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up user groups and permissions...'))
        
        # Create groups
        self.create_groups()
        
        # Assign permissions to groups
        self.assign_permissions()
        
        self.stdout.write(self.style.SUCCESS('Successfully set up user groups and permissions!'))

    def create_groups(self):
        """Create the five main user groups"""
        groups = [
            ('Buyers', 'Property buyers and renters'),
            ('Sellers', 'Property sellers and owners'),
            ('Agents', 'Real estate agents'),
            ('Developers', 'Property developers'),
            ('Admins', 'System administrators'),
        ]
        
        for group_name, description in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Created group: {group_name}')
            else:
                self.stdout.write(f'Group already exists: {group_name}')

    def assign_permissions(self):
        """Assign permissions to each group based on role requirements"""
        
        # Get groups
        buyers_group = Group.objects.get(name='Buyers')
        sellers_group = Group.objects.get(name='Sellers')
        agents_group = Group.objects.get(name='Agents')
        developers_group = Group.objects.get(name='Developers')
        admins_group = Group.objects.get(name='Admins')
        
        # Define permissions for each model
        permissions_config = {
            # Property permissions
            'property': {
                'buyers': ['view'],
                'sellers': ['view', 'add', 'change', 'delete'],  # Only their own
                'agents': ['view', 'add', 'change', 'delete'],   # Client properties
                'developers': ['view', 'add', 'change', 'delete'], # Project properties
                'admins': ['view', 'add', 'change', 'delete'],   # All properties
            },
            
            # Property Image permissions
            'propertyimage': {
                'buyers': ['view'],
                'sellers': ['view', 'add', 'change', 'delete'],
                'agents': ['view', 'add', 'change', 'delete'],
                'developers': ['view', 'add', 'change', 'delete'],
                'admins': ['view', 'add', 'change', 'delete'],
            },
            
            # Property Inquiry permissions
            'propertyinquiry': {
                'buyers': ['view', 'add'], # Can create and view their own
                'sellers': ['view'],       # Can view inquiries for their properties
                'agents': ['view', 'add', 'change'], # Can manage inquiries
                'developers': ['view'],    # Can view inquiries for their properties
                'admins': ['view', 'add', 'change', 'delete'],
            },
            
            # Property Favorite permissions
            'propertyfavorite': {
                'buyers': ['view', 'add', 'delete'], # Manage their favorites
                'sellers': ['view', 'add', 'delete'],
                'agents': ['view', 'add', 'delete'],
                'developers': ['view', 'add', 'delete'],
                'admins': ['view', 'add', 'change', 'delete'],
            },
            
            # Property Review permissions
            'propertyreview': {
                'buyers': ['view', 'add'],    # Can add reviews
                'sellers': ['view'],          # Can view reviews of their properties
                'agents': ['view'],           # Can view reviews
                'developers': ['view'],       # Can view reviews
                'admins': ['view', 'add', 'change', 'delete'],
            },
            
            # User management permissions
            'customuser': {
                'buyers': [],
                'sellers': [],
                'agents': ['view'],  # Can view basic user info for clients
                'developers': ['view'],
                'admins': ['view', 'add', 'change', 'delete'],
            },
            
            # Profile permissions
            'buyerprofile': {
                'buyers': ['view', 'change'],
                'sellers': [],
                'agents': ['view'], # Can view client profiles
                'developers': [],
                'admins': ['view', 'add', 'change', 'delete'],
            },
            
            'sellerprofile': {
                'buyers': [],
                'sellers': ['view', 'change'],
                'agents': ['view'],
                'developers': [],
                'admins': ['view', 'add', 'change', 'delete'],
            },
            
            'agentprofile': {
                'buyers': [],
                'sellers': [],
                'agents': ['view', 'change'],
                'developers': [],
                'admins': ['view', 'add', 'change', 'delete'],
            },
        }
        
        # Apply permissions
        for model_name, group_permissions in permissions_config.items():
            self.assign_model_permissions(model_name, group_permissions)

    def assign_model_permissions(self, model_name, group_permissions):
        """Assign permissions for a specific model to groups"""
        try:
            # Get the model
            if model_name in ['customuser']:
                app_label = 'authapp'
            else:
                app_label = 'authapp'  # Assuming all models are in authapp
            
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
            
            # Map group names to groups
            group_mapping = {
                'buyers': Group.objects.get(name='Buyers'),
                'sellers': Group.objects.get(name='Sellers'),
                'agents': Group.objects.get(name='Agents'),
                'developers': Group.objects.get(name='Developers'),
                'admins': Group.objects.get(name='Admins'),
            }
            
            # Assign permissions to each group
            for group_key, permission_types in group_permissions.items():
                group = group_mapping[group_key]
                
                for perm_type in permission_types:
                    permission_codename = f'{perm_type}_{model_name}'
                    
                    try:
                        permission = Permission.objects.get(
                            content_type=content_type,
                            codename=permission_codename
                        )
                        group.permissions.add(permission)
                        self.stdout.write(
                            f'Assigned {permission_codename} to {group.name}'
                        )
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Permission {permission_codename} does not exist'
                            )
                        )
                        
        except ContentType.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f'ContentType for {model_name} does not exist')
            )

    def add_arguments(self, parser):
        parser.add_argument(
            '--recreate',
            action='store_true',
            help='Delete existing groups and recreate them',
        )