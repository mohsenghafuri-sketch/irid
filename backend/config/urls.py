from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def tenant_debug(request):
    tenant = getattr(request, "tenant", None)

    if not tenant:
        return JsonResponse({"tenant": None})

    return JsonResponse(
        {
            "tenant_schema": tenant.schema_name,
            "tenant_name": tenant.name,
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.api.urls")),
    path("debug/tenant/", tenant_debug),
]

