import datetime
from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone
from storage.models import *
from users.models import *
from rest_framework.response import Response

from users.serializers import UserSerializer


@periodic_task(run_every=crontab(minute='*/1'))
def delete_old_orders():
    d = timezone.now() - datetime.timedelta(minutes=2)
    
    orders = Timeline.objects.filter(created_time__lt=d, confirmed=False)
    print (orders)
    orders.delete()

    return "Done"


@periodic_task(run_every=crontab(minute='*/1'))
def get_staff_pvs():
    users = User.objects.filter(is_active=True)
    serializer = UserSerializer(users, many=True)
    api_url = "https://pvs.com.vn/user-api/get-list-staff-profile"
    api_request = requests.get(api_url)
        
    url_file = api_request.json()['data']
        
    for i in url_file:
        print(i['user'])
        check = User.objects.filter(email=i['user']['email']).count()
        if check == 0:
            User.objects.create_user(
                id=i['user']['id'], email=i['user']['email'], 
                password='PVS@@123456', is_staff=True
                )
            users = User.objects.get(id=i['user']['id'])
            check = StaffProfile.objects.filter(user=users).count()
            if check == 0:
                for staff in str(users):
                    StaffProfile.objects.create(
                        user=users, name=i['name'], 
                        position=i['position'],
                    ) 
                    return Response(serializer.data)
            return "Done"        
                        