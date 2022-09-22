from django.urls import path, include
from rest_framework.routers import DefaultRouter

"""
# =================================================================================================== #
# URLS ============================================================================================== #
# =================================================================================================== #
"""

# Create a router and register our view sets with it
router = DefaultRouter()

# urls for 'misc' routes
urlpatterns = [
    # EMAIL ======================================================== #
    # path(r"emails/", EmailViewSet.as_view()),
] + router.urls