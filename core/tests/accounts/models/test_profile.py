import pytest
from django.db.models.signals import post_save
from apps.accounts.models import Profile
from faker import Faker

faker = Faker()

@pytest.mark.django_db
class TestProfile:

    def test_profile_created_with_user(self, normal_user_profile):
        assert normal_user_profile.user is not None
        assert normal_user_profile.reviews_count == 0
        assert normal_user_profile.orders_count == 0
        assert Profile.objects.filter(user=normal_user_profile.user).exists()

    def test_signal_does_not_duplicate_profile(self, normal_user_profile):
        initial_count = Profile.objects.count()
        post_save.send(sender=type(normal_user_profile.user), instance=normal_user_profile.user, created=False)
        assert Profile.objects.count() == initial_count

    def test_str_output(self, normal_user_profile):
        normal_user_profile.first_name = "Ali"
        normal_user_profile.last_name = "Karimi"
        normal_user_profile.save()
        expected = f"Ali Karimi ({normal_user_profile.user.phone})"
        assert str(normal_user_profile) == expected

    def test_field_assignment(self, normal_user_profile):
        email = faker.email()
        normal_user_profile.first_name = "Leila"
        normal_user_profile.last_name = "Kazemi"
        normal_user_profile.reviews_count = 3
        normal_user_profile.orders_count = 6
        normal_user_profile.temporary_email = email
        normal_user_profile.save()
        obj = Profile.objects.get(pk=normal_user_profile.pk)
        assert obj.first_name == "Leila"
        assert obj.last_name == "Kazemi"
        assert obj.reviews_count == 3
        assert obj.orders_count == 6
        assert obj.temporary_email == email

    def test_default_profile_picture(self, normal_user_profile):
        assert normal_user_profile.profile_picture.name == "user/profile/user.png"

    def test_count_update(self, normal_user_profile):
        normal_user_profile.reviews_count = 1
        normal_user_profile.orders_count = 2
        normal_user_profile.save()
        normal_user_profile.reviews_count += 4
        normal_user_profile.orders_count += 3
        normal_user_profile.save()
        refreshed = Profile.objects.get(pk=normal_user_profile.pk)
        assert refreshed.reviews_count == 5
        assert refreshed.orders_count == 5
