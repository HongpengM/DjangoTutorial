from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from PIL import Image
from io import BytesIO
import binascii


class TestPNGServer(TestCase):
    def test_get_index_response(self):
        response = self.client.get('')
        assert response.status_code == 200

    def test_get_image_response(self):
        response = self.client.get('/image/30x60/')
        assert response.status_code == 200

    def test_get_image_outlier(self):
        response = self.client.get('/image/30x4001/')
        assert response.status_code == 400
        response = self.client.get('/png/30x300/')
        assert response.status_code == 404

    def test_get_index_content(self):
        response = self.client.get('')
        assert response.content == b'\n<!DOCTYPE html>\n<html>\n<head>\n    <meta charser="utf-8">\n    <title>Django PNGen Server</title>\n    <link rel="stylesheet" href="/static/site.css" type="text/css">\n</head>\n<body>\n    <h1>Django PNG Generate Images</h1>\n    <p>This server can be used for serving blank png </p>\n    <p>To request a blank png image, simply GET:</p>\n    <b>/image/&lt;width&gt;x&lt;height&gt;/</b>\n    <p>such as: </p>\n    <pre>\n        &lt;img src="http://testserver/image/50x50/" &gt;\n    </pre>\n    <h2> Examples</h2>\n    <ul>\n        <li><img src="/image/50x50/"></li>\n        <li><img src="/image/200x50/"></li>\n        <li><img src="/image/50x400/"></li>\n    </ul>\n</body>\n</html>'

    def test_get_image_content(self):
        response = self.client.get('/image/40x80/')
        stream = BytesIO(response.content)
        img = Image.open(stream)
        assert img.size == (40, 80)
