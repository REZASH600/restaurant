import pytest

from apps.menus.api.v1.serializers import ReviewsAdminSerializer, ReviewSerializer


@pytest.mark.django_db
class TestReviewSerializers:

    def test_reviews_admin_serializer(self, review):
        serializer = ReviewsAdminSerializer(review)
        data = serializer.data

        assert data["id"] == review.id
        assert data["comment"] == review.comment
        assert float(data["rate"]) == float(review.rate)
        assert data["menu_item"] == review.menu_item.id

    def test_review_serializer_output(self, review, rf):
        request = rf.get("/")
        context = {"request": request}
        serializer = ReviewSerializer(review, context=context)
        data = serializer.data

        assert data["id"] == review.id
        assert data["comment"] == review.comment
        assert float(data["rate"]) == float(review.rate)
        assert "user_profile_data" in data
        assert data["user_profile_data"]["id"] == review.user_profile.id

    def test_review_create_auto_publish(self, normal_user_profile, menu_item_with_relations,rf):
        request = rf.post("/")
        request.user = normal_user_profile.user
        context = {"request": request}

        data = {
            "menu_item": menu_item_with_relations.id,
            "restaurant": menu_item_with_relations.restaurant.first().id,
            "comment": "Great food!",
            "rate": 5,
        }

        serializer = ReviewSerializer(data=data, context=context)
        assert serializer.is_valid(), serializer.errors
        review_instance = serializer.save()

        assert review_instance.comment == data["comment"]
        assert review_instance.is_published is True
        assert review_instance.user_profile == normal_user_profile
