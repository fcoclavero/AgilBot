from django.core.urlresolvers import reverse
from django.test import TestCase


class IndexTests(TestCase):
    def test_index_view_status_code(self):
        url = reverse('app:index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
