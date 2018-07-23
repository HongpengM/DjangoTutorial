# Django Hello World

##最简单的Hello World Python程序

最简单的Hello World 程序 hello.py

```python
from django.http import HttpResponse
def index(request):
    return HttpResponse('Hello world')


from django.conf.urls import url
urlpatterns = (url(r'^$', index),)


import sys
from django.conf import settings
settings.configure(
    DEBUG=True, SECRET_KEY='thisisthesecretkey',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=('django.middleware.common.CommonMiddleware',
                        'django.middleware.csrf.CsrfViewMiddleware',
                        'django.middleware.clickjacking.XFrameOptionsMiddleware'))
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

```

运行python hello.py runserver运行

## 构建WSGI接口

```python
pip install gunicorn 
```

gunicorn 是一个Python编写的WSGI UNIX服务器，适用于Linux系平台

```shell
hostname@ubuntu:~$ gunicorn hello_wsgi --log-file=-
[2018-07-22 22:14:56 -0700] [14270] [INFO] Starting gunicorn 19.9.0
[2018-07-22 22:14:56 -0700] [14270] [INFO] Listening at: http://127.0.0.1:8000 (14270)
[2018-07-22 22:14:56 -0700] [14270] [INFO] Using worker: sync
[2018-07-22 22:14:56 -0700] [14273] [INFO] Booting worker with pid: 14273
...
```



## 12 Factor App: 将配置变量移至环境

```python
'''
=========================================================
# Move configure to environment variables
'''
DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))
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
```



## 可复用模板

```python
hello_template/
	hello_template.py
    
'''
...
=========================================================
# secret_key project_name project_directory docs_version
Will be passed as CONTEXT using template

'''
DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', {{secret_key}})
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
...
'''
```



使用startproject的template参数会生成一个以某项目文件夹一致的文件

```shell
python -m django startproject foo --template=hello_template
```

如果文件夹及文件分别为project_name， project_name.py，该文件则会自动继承命令行中新project的文件



