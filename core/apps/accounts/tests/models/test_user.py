import pytest
from django.core.exceptions import ValidationError
from apps.accounts.models import MyUser


@pytest.mark.django_db
class TestMyUserModel:

    def test_create_normal_user(self, normal_user):
        assert normal_user.is_active is True
        assert normal_user.is_staff is False
        assert normal_user.is_superuser is False
        assert normal_user.phone.startswith("09")
        assert len(normal_user.phone) == 11

    def test_create_inactive_user(self, inactive_user):
        assert inactive_user.is_active is False
        assert inactive_user.is_staff is False

    def test_create_staff_user(self, staff_user):
        assert staff_user.is_staff is True
        assert staff_user.is_superuser is False

    def test_create_superuser(self, super_user):
        assert super_user.is_superuser is True
        assert super_user.is_staff is True
        assert super_user.is_active is True

    def test_password_is_hashed(self, normal_user):
        assert normal_user.password != "Reza.sh1382"
        assert normal_user.check_password("Reza.sh1382")

    def test_str_representation(self, normal_user):
        assert str(normal_user) == normal_user.phone

    def test_default_field_values(self, normal_user):
        assert normal_user.is_active is True
        assert normal_user.is_phone_verified is True

    def test_missing_username_raises_error(self):
        with pytest.raises(ValueError):
            MyUser.objects.create_user(
                phone="09123456789", username=None, password="Reza.sh1382"
            )

    def test_missing_phone_raises_error(self):
        with pytest.raises(ValueError):
            MyUser.objects.create_user(
                phone=None, username="reza", password="Reza.sh1382"
            )

    def test_missing_password_raises_error(self):
        with pytest.raises(ValueError):
            MyUser.objects.create_user(
                phone="09123456789", username="reza", password=None
            )

    def test_create_superuser_with_wrong_flags_raises(self):
        with pytest.raises(ValueError):
            MyUser.objects.create_superuser(
                phone="09123456789",
                username="admin",
                password="Reza.sh1382",
                is_staff=False,
            )

    def test_create_personnel_with_wrong_flags_raises(self):
        with pytest.raises(ValueError):
            MyUser.objects.create_personnel(
                phone="09123456789",
                username="personel",
                password="Reza.sh1382",
                is_staff=True,
            )

    def test_phone_validation_accepts_valid(self):
        user = MyUser(phone="09123456789", username="validuser", password="Reza.sh1382")
        user.full_clean()


    def test_phone_validation_rejects_invalid(self):
        user = MyUser(
            phone="08123456789", username="invaliduser", password="Reza.sh1382"
        )
        with pytest.raises(ValidationError):
            user.full_clean()


