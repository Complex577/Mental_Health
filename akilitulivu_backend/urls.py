from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include


schema_view = get_schema_view(
   openapi.Info(title="My API", default_version='v1'),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/chatbot/", include("chatbot.urls")),
    path("api/assessment/", include("self_evaluation.urls")),
    path("api/education/", include("education.urls")),
    path("api/experts/", include("experts.urls")),
    path("api/admin/", include("administrator.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
