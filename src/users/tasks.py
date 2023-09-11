


from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone


from dateutil.relativedelta import relativedelta



logger = get_task_logger(__name__)


@shared_task
def check_subscriptions_task():
    print('-------------------!!!!!!!!!---------------------------')
    print('-------------------checking!---------------------------')
    print('-------------------!!!!!!!!!---------------------------')
    
    # from .models import Subscription

    # subscriptions = Subscription.objects.filter(\
    #                 subscription_last_date__lte = timezone.now().date(),\
    #                 is_active = True)
    # for subscription in subscriptions:
    #     if subscription.is_auto_renewal == False:
    #         subscription.is_active = False
    #         subscription.save()
    #     if subscription.is_auto_renewal == True:
    #         subscription.subscription_last_date = timezone.now().date() + relativedelta(months=1)
    #         subscription.save()

