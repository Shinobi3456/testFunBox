from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = {
    path('visited_links', visited_links, name="visited_links"),
    path('visited_domains', visited_domains, name="visited_domains"),
}