from django.urls import path
from rest_framework.routers import DefaultRouter
from webhooks.views import github_webhook

"""
# =================================================================================================== #
# URLS ============================================================================================== #
# =================================================================================================== #
"""

# Create a router and register our view sets with it
router = DefaultRouter()

# urls for 'misc' routes
urlpatterns = [
    # WEBHOOK LISTENERS ======================================================== #
    # we attach a random string to each url to add a level
    # of security to the webhook listener, since presumably
    # only the webhook sender will have this exact URL
    path(r"github/pAXESnQTVN0l3Cjv", github_webhook),
] + router.urls
