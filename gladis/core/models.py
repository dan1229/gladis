import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

"""
# ==================================================================================== #
# ABSTRACT BASE MODEL ================================================================ #
# ==================================================================================== #
"""


#
# ABSTRACT BASE MODEL =================================== #
#
class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "Abstract Base Model"


"""
# ==================================================================================== #
# USER =============================================================================== #
# ==================================================================================== #
"""


#
# USER MANAGER ================== #
#
class UserManager(BaseUserManager):
    """Custom User model manager, eliminating the 'username' field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        All emails are lowercase automatically.
        """
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a superuser with the given email and password."""
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self._create_user(email, password, **extra_fields)

    class Meta:
        ordering = ("id",)


#
# USER ========================= #
#
class User(AbstractUser, AbstractBaseModel):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField(unique=True)

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        app_label = "core"
        ordering = ["email"]


#
# USER SETTINGS ================= #
#
class UserSettings(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    slack_username = models.CharField(max_length=255, null=False, blank=False)
    github_username = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"User Settings ({self.user})"

    class Meta:
        app_label = "core"
        ordering = ["user"]
