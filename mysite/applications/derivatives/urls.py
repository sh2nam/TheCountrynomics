from django.urls import path
from . import views

#TEMPLATE TAGGING
app_name = "derivatives"

urlpatterns = [
    path("g20_dashboard/", views.derivatives, name = "derivatives"),
    path("custom_data/", views.custom_data, name = "custom_data"),
    path("custom_data/compare_contrast/", views.compare_contrast, name = "compare_contrast"),
    path("custom_data/gdp_per_cap_report/", views.gdp_per_cap_report, name = "gdp_per_cap_report"),
]
