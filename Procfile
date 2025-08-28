django: uv run python -m debugpy --listen 5678 manage.py runserver $PORT
vite: pnpm exec vite
celery-worker: celery -A src.tasks worker -l INFO --without-gossip --without-mingle --without-heartbeat
celery-beat: celery -A src.tasks beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
