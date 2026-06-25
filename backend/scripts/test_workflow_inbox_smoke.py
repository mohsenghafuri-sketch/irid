import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

import django
django.setup()

from django.urls import resolve, reverse
from django_tenants.utils import schema_context
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.requests.models import Request
from apps.tenants.models import Client, Domain


TENANT_SCHEMA = "irid"
HOST = "irid.localhost"
INBOX_PATH = "/api/workflow/inbox/"

WORKFLOW_USERS = [
    "manager@irid.ir",
    "finance@irid.ir",
    "emp@irid.ir",
    "ceo@irid.ir",
]


def ensure_domains():
    tenant = Client.objects.get(schema_name=TENANT_SCHEMA)

    for domain in [HOST, "irid.ir", "testserver", "192.168.10.85"]:
        obj, created = Domain.objects.get_or_create(
            domain=domain,
            defaults={
                "tenant": tenant,
                "is_primary": domain == HOST,
            },
        )

        changed = False
        if obj.tenant_id != tenant.id:
            obj.tenant = tenant
            changed = True

        if domain == HOST and not obj.is_primary:
            obj.is_primary = True
            changed = True

        if changed:
            obj.save()

    print(f"[OK] Tenant domains ensured for schema={TENANT_SCHEMA}")


def get_test_user():
    with schema_context(TENANT_SCHEMA):
        for email in WORKFLOW_USERS:
            user = User.objects.filter(email=email).first()
            if user:
                print(f"[OK] Using user: {user.email}")
                return user

        raise RuntimeError(
            "No workflow test user found. Expected one of: "
            + ", ".join(WORKFLOW_USERS)
        )


def main():
    print("========== Workflow Inbox Smoke Test ==========")

    ensure_domains()

    match = resolve(INBOX_PATH)
    print(f"[OK] resolve({INBOX_PATH}) -> {match.url_name}")

    reversed_path = reverse("workflow-inbox")
    print(f"[OK] reverse('workflow-inbox') -> {reversed_path}")

    with schema_context(TENANT_SCHEMA):
        request_count = Request.objects.count()
        print(f"[OK] Request count in schema '{TENANT_SCHEMA}': {request_count}")

    user = get_test_user()

    client = APIClient(HTTP_HOST=HOST)
    client.force_authenticate(user=user)

    response = client.get(INBOX_PATH, HTTP_HOST=HOST)

    print(f"[RESULT] GET {INBOX_PATH} with HOST={HOST}")
    print(f"[RESULT] Status: {response.status_code}")
    print(f"[RESULT] Content-Type: {response.get('Content-Type')}")

    try:
        payload = response.json()
        print("[RESULT] JSON:", payload)
    except Exception:
        print("[RESULT] Body:", response.content[:2000])

    if response.status_code != 200:
        raise RuntimeError(f"Inbox API failed with status={response.status_code}")

    print("[PASS] Workflow Inbox API is reachable and authenticated.")


if __name__ == "__main__":
    main()
