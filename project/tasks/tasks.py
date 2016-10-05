from celery import Celery

app = Celery('hello', broker='amqp://test:test@localhost//',
                      backend='redis://localhost')


@app.task
def hello():
    return 'hello world'