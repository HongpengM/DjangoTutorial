# PNG 占位图片服务器



## 新的Url pattern



```python
def pngHolder(request, width, height):
    #TODO
    return HttpResponse('OK')

urlpatterns = (
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$',
        pngHolder, name='pngHolder'),
    url(r'^$', index, name='homepage'),
)
```



## 表单校验

引入django的表单来完成输入参数的校验

```python
from django import forms
from django.http import HttpResponseBadRequest
class ImageForms(forms.Form):
    """docstring for  ImageForms"""
    height = forms.IntegerField(min_value=1, max_value=4000)
    width = forms.IntegerField(min_value=1, max_value=4000)


def pngHolder(request, width, height):
    # TODO
    form = ImageForms({'height': height, 'width': width})
    if form.is_valid():
        height = form.cleaned_data['height']
        width = form.cleaned_data['width']

        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest('Invalid request')
```



## 图片缓存

### 服务器本地缓存

```python
from django.core.cache import cache
class ImageForms(forms.Form):
    """docstring for  ImageForms"""
    height = forms.IntegerField(min_value=1, max_value=4000)
    width = forms.IntegerField(min_value=1, max_value=4000)

    def generate(self, image_format='PNG'):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        # Set content key
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        if content == None:

            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{} x {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)

            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill=(255, 255, 0))

            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            # New content cached
            cache.set(key, content, 60 * 60)
        return content
```



### 客户端缓存

Etag修饰 304 Not Modified

```python
from django.views.decorators.http import etag
import hashlib
def generate_etag(request, width, height):
    content = 'pngHolder: {0} x {1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(generate_etag)
def pngHolder(request, width, height):
    # TODO
    form = ImageForms({'height': height, 'width': width})
    if form.is_valid():

        image = form.generate()

        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid request')
```



## Template

templates和static应放在靠近项目的地方

```python
PNGen/
	PNGen.py
    templates/
    	home.html
    static/
    	site.css    
```

并在setting中配置

```python
'''
=========================================================
# Set static file setting

'''

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get(
    'SECRET_KEY', '3@ri6j0y@!01vhg1nay1y ^ fkhq - gzazh@yp@r(yu) % owu_4bkz')
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 'localhost').split(',').append('127.0.0.1')
BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=('django.middleware.common.CommonMiddleware',
                        'django.middleware.csrf.CsrfViewMiddleware',
                        'django.middleware.clickjacking.XFrameOptionsMiddleware'),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
    ),
    TEMPLATES=(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': (
                os.path.join(BASE_DIR, 'templates'),
            )
        },
    ),
    STATICFILES_DIRS=(
        os.path.join(BASE_DIR, 'static'),
    ),
    STATIC_URL='/static/',
)

'''
=========================================================
'''
```



在templates中加入home.html

```html
{% load staticfiles %}
<!DOCTYPE html>
<html>
<head>
    <meta charser="utf-8">
    <title>Django PNGen Server</title>
    <link rel="stylesheet" href="{% static 'site.css' %}" type="text/css">
</head>
<body>
    <h1>Django PNG Generate Images</h1>
    <p>This server can be used for serving blank png </p>
    <p>To request a blank png image, simply GET:</p>
    <b>/image/&lt;width&gt;x&lt;height&gt;/</b>
    <p>such as: </p>
    <pre>
        &lt;img src="{{example}}" &gt;
    </pre>
    <h2> Examples</h2>
    <ul>
        <li><img src="{% url 'pngHolder' width=50 height=50%}"></li>
        <li><img src="{% url 'pngHolder' width=200 height=50%}"></li>
        <li><img src="{% url 'pngHolder' width=50 height=400%}"></li>
    </ul>
</body>
</html>
```

在static中加入site.css

```css	
body{
    text-align:center;
}
ul {
    list-type:None;
}
li{
    display: inline-block;
}
```

通过reverse 和 render重新用模板来渲染主页的视图



```python
from django.urls import reverse
from django.shortcuts import render

def index(request):
    example = reverse('pngHolder', kwargs={'width': 50, 'height': 50})
    context = {'example': request.build_absolute_uri(example)}
    return render(request, 'home.html', context)

```

