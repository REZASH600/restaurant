import pytest
from django.db.models.signals import post_save
from apps.accounts.models import Profile
from faker import Faker

faker = Faker()

@pytest.mark.django_db
class TestProfile:

    def test_profile_created_with_user(self, fake_profile):
        assert fake_profile.user is not None
        assert fake_profile.reviews_count == 0
        assert fake_profile.orders_count == 0
        assert Profile.objects.filter(user=fake_profile.user).exists()

    def test_signal_does_not_duplicate_profile(self, fake_profile):
        initial_count = Profile.objects.count()
        post_save.send(sender=type(fake_profile.user), instance=fake_profile.user, created=False)
        assert Profile.objects.count() == initial_count

    def test_str_output(self, fake_profile):
        fake_profile.first_name = "Ali"
        fake_profile.last_name = "Karimi"
        fake_profile.save()
        expected = f"Ali Karimi ({fake_profile.user.phone})"
        assert str(fake_profile) == expected

    def test_field_assignment(self, fake_profile):
        email = faker.email()
        fake_profile.first_name = "Leila"
        fake_profile.last_name = "Kazemi"
        fake_profile.reviews_count = 3
        fake_profile.orders_count = 6
        fake_profile.temporary_email = email
        fake_profile.save()
        obj = Profile.objects.get(pk=fake_profile.pk)
        assert obj.first_name == "Leila"
        assert obj.last_name == "Kazemi"
        assert obj.reviews_count == 3
        assert obj.orders_count == 6
        assert obj.temporary_email == email

    def test_default_profile_picture(self, fake_profile):
        assert fake_profile.profile_picture.name == "user/profile/user.png"

    def test_count_update(self, fake_profile):
        fake_profile.reviews_count = 1
        fake_profile.orders_count = 2
        fake_profile.save()
        fake_profile.reviews_count += 4
        fake_profile.orders_count += 3
        fake_profile.save()
        refreshed = Profile.objects.get(pk=fake_profile.pk)
        assert refreshed.reviews_count == 5
        assert refreshed.orders_count == 5
