from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from . import validations


class MyUserManager(BaseUserManager):
    """
    Custom manager for the User model, providing methods to create regular users, personnel, and managers.
    """

    def create_user(self, phone, username, password, **extra_fields):
        """
        Creates and returns a regular user with the specified phone, username, and password.

        This method ensures that the phone number, username, and password are provided.
        It also validates the password and normalizes the email if included in extra fields.

        Args:
            phone (str): The user's phone number (required).
            username (str): The user's username (required).
            password (str): The user's password (required).
            extra_fields (dict): Additional fields to set on the user.

        Returns:
            User: The created user instance.

        Raises:
            ValueError: If any required field is missing or if the password is invalid.
        """
        if not phone:
            raise ValueError("The Phone field must be set.")

        if not username:
            raise ValueError("The Username field must be set.")

        if not password:
            raise ValueError("The password field must be set.")

        user = self.model(phone=phone, username=username, **extra_fields)

        if "email" in extra_fields:
            user.email = self.normalize_email(extra_fields["email"])

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_personnel(self, phone, username, password, **extra_fields):
        """
        Creates and returns a personnel user with the specified phone, username, and password.

        Personnel users have `is_superuser=True`, `is_active=True`, and `is_staff=False`.
        If these conditions are not met, an error is raised.

        Args:
            phone (str): The personnel's phone number.
            username (str): The personnel's username.
            password (str): The personnel's password.
            extra_fields (dict): Additional fields to set.

        Returns:
            User: The created personnel user instance.

        Raises:
            ValueError: If the required flags are not correctly set.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", False)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("personnel must have is_superuser=True."))

        if extra_fields.get("is_active") is not True:
            raise ValueError(_("personnel must have is_active=True."))

        if extra_fields.get("is_staff") is not False:
            raise ValueError(_("personnel must have is_staff=False."))

        return self.create_user(phone, username, password, **extra_fields)

    def create_superuser(self, phone, username, password, **extra_fields):
        """
        Creates and returns a manager user with the specified phone, username, and password.

        Manager users have `is_superuser=True`, `is_active=True`, and `is_staff=True`.
        If these conditions are not met, an error is raised.

        Args:
            phone (str): The manager's phone number.
            username (str): The manager's username.
            password (str): The manager's password.
            extra_fields (dict): Additional fields to set.

        Returns:
            User: The created manager user instance.

        Raises:
            ValueError: If the required flags are not correctly set.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("manager must have is_superuser=True."))

        if extra_fields.get("is_active") is not True:
            raise ValueError(_("manager must have is_active=True."))

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("manager must have is_staff=True."))

        return self.create_user(phone, username, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        verbose_name=_("phone"),
        max_length=11,
        unique=True,
        validators=[validations.validate_phone],
    )
    username = models.CharField(verbose_name=_("username"), max_length=255, unique=True)

    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(verbose_name=_("is active"), default=True)
    is_staff = models.BooleanField(verbose_name=_("is staff"), default=False)
    is_phone_verified = models.BooleanField(
        verbose_name=_("is phone verified"), default=False
    )

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
