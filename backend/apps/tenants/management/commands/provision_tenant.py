from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from django_tenants.utils import tenant_context

from apps.tenants.models import Client, Domain


User = get_user_model()


class Command(BaseCommand):
    help = "Create a new tenant with domain and admin user"

    def add_arguments(self, parser):

        parser.add_argument("--schema", required=True)
        parser.add_argument("--domain", required=True)
        parser.add_argument("--name", required=True)

        parser.add_argument("--admin-username", required=True)
        parser.add_argument("--admin-email", required=True)

    def handle(self, *args, **options):

        schema = options["schema"]
        domain = options["domain"]
        name = options["name"]

        admin_username = options["admin_username"]
        admin_email = options["admin_email"]

        if Client.objects.filter(schema_name=schema).exists():
            self.stderr.write(f"Schema '{schema}' already exists")
            return

        if Domain.objects.filter(domain=domain).exists():
            self.stderr.write(f"Domain '{domain}' already exists")
            return

        self.stdout.write("Creating tenant...")

        with transaction.atomic():

            tenant = Client(
                schema_name=schema,
                name=name,
            )

            tenant.save()

            Domain.objects.create(
                domain=domain,
                tenant=tenant,
                is_primary=True,
            )

        self.stdout.write(self.style.SUCCESS("Tenant created"))

        password = input("Admin password: ")

        with tenant_context(tenant):

            if User.objects.filter(username=admin_username).exists():
                self.stderr.write("Admin username already exists")
                return

            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=password,
            )

        self.stdout.write(self.style.SUCCESS("Admin user created"))
        self.stdout.write(self.style.SUCCESS("Tenant provisioning complete"))
