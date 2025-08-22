vite: pnpm exec vite
django: python manage.py runserver
celery-worker: celery -A src.tasks worker -l INFO --without-gossip --without-mingle --without-heartbeat
celery-beat: celery -A src.tasks beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
