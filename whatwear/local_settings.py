import os
import environ

#環境変数のため追記
env = environ.Env()
env.read_env('.env')

#settings.pyからそのままコピー
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY=env('SECRET_KEY')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresl',
        'NAME': os.path.join(BASE_DIR, 'db.postgresl'),
    }
}

DEBUG = True 