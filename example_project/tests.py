from django.test import TestCase
from migdal.models import Entry


class MigdalTests(TestCase):
    def test_x(self):
        Entry.objects.create(
                type='info', author='An author',
                published_pl=True, title_pl='An info entry', slug_pl='test1',
                body_pl='**Test text**',
            )
        Entry.objects.create(
                type='blog', author='An author',
                published_pl=True, title_pl='A blog entry', slug_pl='test2',
                body_pl='**Test blog text**',
            )


        response = self.client.get('/')
        self.assertContains(response, 'A blog entry')
        self.assertNotContains(response, 'An info entry')



        response = self.client.get('/info/')
        self.assertContains(response, 'An info entry')

        response = self.client.get('/info/test1/')
        self.assertContains(response, '<b>Test text</b>')
