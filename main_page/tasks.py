from time import sleep
from celery import shared_task
from a_wall_site.celery import app


@shared_task
def some_task():
    sleep(10)
    return 'aboba'


@shared_task
def test_scheduled_task():
    return 'susibaka'


if __name__ == '__main__':
    app.worker_main()
