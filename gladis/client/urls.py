from django.urls import re_path
from client.views import index

"""
# ============================================================ #
# URLS ======================================================= #
# ============================================================ #
"""

# urls for 'misc' routes
urlpatterns = [
    re_path(r"^$", index, name="home"),
]
