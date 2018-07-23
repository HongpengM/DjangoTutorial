import os
import sys

from django.conf import settings
'''
=========================================================
# secret_key project_name project_directory docs_version
Will be passed as CONTEXT using template

'''
DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', wywrfe^4xb7(k66@tfl)@!&k@^8@=3t8@6yvv=2+1tj)*#z(0!)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=('django.middleware.common.CommonMiddleware',
                        'django.middleware.csrf.CsrfViewMiddleware',
                        'django.middleware.clickjacking.XFrameOptionsMiddleware'))
'''
=========================================================
'''

from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello world')


from django.conf.urls import url
urlpatterns = (url(r'^$', index),)


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
