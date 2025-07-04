from django.contrib import admin
from .models import SelfAssessment, ModelConfig, FeatureModelAssignment

admin.site.register(SelfAssessment)


@admin.register(ModelConfig)
class ModelConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "temperature", "active")
    list_filter = ("provider", "active")
    search_fields = ("name",)

@admin.register(FeatureModelAssignment)
class FeatureModelAssignmentAdmin(admin.ModelAdmin):
    list_display = ("feature_key", "model")
    list_filter = ("feature_key", "model__provider")
    search_fields = ("feature_key",)
