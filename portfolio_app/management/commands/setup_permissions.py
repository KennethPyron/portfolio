from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from portfolio_app.models import Portfolio, Project, Student


class Command(BaseCommand):
    help = 'Sets up user groups and permissions for the portfolio application'

    def handle(self, *args, **kwargs):
        # Create or get the 'student' group
        student_group, created = Group.objects.get_or_create(name='student')

        if created:
            self.stdout.write(self.style.SUCCESS('Created "student" group'))
        else:
            self.stdout.write(self.style.WARNING('Group "student" already exists'))

        # Get content types for our models
        portfolio_ct = ContentType.objects.get_for_model(Portfolio)
        project_ct = ContentType.objects.get_for_model(Project)
        student_ct = ContentType.objects.get_for_model(Student)

        # Define permissions for the student group
        # Students can add, change, and delete portfolios and projects
        permissions = [
            # Portfolio permissions
            Permission.objects.get(codename='add_portfolio', content_type=portfolio_ct),
            Permission.objects.get(codename='change_portfolio', content_type=portfolio_ct),
            Permission.objects.get(codename='delete_portfolio', content_type=portfolio_ct),
            Permission.objects.get(codename='view_portfolio', content_type=portfolio_ct),

            # Project permissions
            Permission.objects.get(codename='add_project', content_type=project_ct),
            Permission.objects.get(codename='change_project', content_type=project_ct),
            Permission.objects.get(codename='delete_project', content_type=project_ct),
            Permission.objects.get(codename='view_project', content_type=project_ct),

            # Student permissions (view and change only, not delete or add)
            Permission.objects.get(codename='view_student', content_type=student_ct),
            Permission.objects.get(codename='change_student', content_type=student_ct),
        ]

        # Add permissions to the group
        student_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully configured {len(permissions)} permissions for "student" group'
        ))

        # Display the permissions
        self.stdout.write('\nAssigned permissions:')
        for perm in permissions:
            self.stdout.write(f'  - {perm.content_type.app_label}.{perm.codename}')
