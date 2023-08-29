import pytest
from users.models import CustomUser, Subscription
from django.utils import timezone
from dateutil.relativedelta import relativedelta

@pytest.mark.django_db
def test_simple_user_update_subscription_path(create_user_with_subscription_fixture):
    user = CustomUser.objects.get(email="test123_email@mail.com")
    url = f'/users/simple_user_update_subscription/{user.id}/'
    payload = {
        'is_prolonging': True
    }
    response = create_user_with_subscription_fixture.patch(url, payload, format='json')
    assert response.status_code == 200
    assert user.subscription.subscription_last_date == timezone.now().date() + relativedelta(months=1)