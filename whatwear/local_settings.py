import os
import environ
import psycopg2


#環境変数のため追記
env = environ.Env()
env.read_env('.env')

#settings.pyからそのままコピー
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY=env('SECRET_KEY')


DATABASES = {

    'default': env.db(),
}

ALLOWED_HOSTS = ['*']

DEBUG = True 