# PVS-EStorage
echo "# PVS-EStorage" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/HoangPham24/PVS-EStorage.git
git push -u origin main

# remove origin
git remote remove origin

# Celery
pip install celery==4.4.2
pip install django-celery-beat
pip install django-celery-results
pip install redis

# Celery settings

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'

CELERY_RESULT_BACKEND = 'django-db'
# Celery django_celery_beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'