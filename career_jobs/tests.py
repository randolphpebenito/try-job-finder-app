from django.contrib.auth.models import User
from django.forms import ModelForm
from django.test import TestCase
from django.urls import resolve, reverse

from .forms import CareerJobCreateForm
from .models import CareerJob
from .views import CareerJobListView, CareerJobCreateView, CareerJobDetailView, CareerJobUpdateView

class HomeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.career_job = CareerJob.objects.create(
            job_title='Django', 
            job_description='Django board.',
            tag='test',
            job_location_city='KL',
            created_by=self.user
        )
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, CareerJobListView)

    def test_home_view_contains_link_to_career_job_detail_page(self):
        career_job_detail_url = reverse('career_job_detail', kwargs={'pk': self.career_job.pk})
        self.assertContains(self.response, 'href="{0}"'.format(career_job_detail_url))


class LoginRequiredCreateCareerJobTests(TestCase):

    def setUp(self):
        self.url = reverse('career_job_create')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class CreateCareerJobTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.url = reverse('career_job_create')

    def test_create_career_job_view_success_status_code(self):
         self.client.login(username='john', password='johnpassword')
         response = self.client.get(self.url)
         self.assertEquals(response.status_code, 200)

    def test_create_career_job_view_redirect_to_login(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_create_career_job_url_resolves_create_career_job_view(self):
        view = resolve('/job/new/')
        self.assertEquals(view.func.view_class, CareerJobCreateView)

    def test_csrf(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(self.url)
        form = response.context.get('form')
        self.assertIsInstance(form, CareerJobCreateForm)

    def test_create_create_career_missing_required_fields(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_create_create_career_success(self):
        self.client.login(username='john', password='johnpassword')
        fields = {
            'job_title': 'Django', 
            'job_description': 'Django board.',
            'tag': 'test',
            'job_location_city': 'KL',
            'created_by': self.user
        }
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)



class DetailCareerJobTests(TestCase):

    def setUp(self):
        self.username = 'john'
        self.password = 'johnpassword'
        self.user = User.objects.create_user(self.username, 'lennon@thebeatles.com', self.password)
        self.career_job = CareerJob.objects.create(
            job_title='Django', 
            job_description='Django board.',
            tag='test',
            job_location_city='KL',
            created_by=self.user
        )
        self.login_url = reverse('login')
        self.url = reverse('career_job_detail', kwargs={ 'pk': self.career_job.pk })
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/job/1/')
        self.assertEquals(view.func.view_class, CareerJobDetailView)


class UpdateCareerJobTests(TestCase):

    def setUp(self):
        self.username = 'john'
        self.password = 'johnpassword'
        self.user = User.objects.create_user(self.username, 'lennon@thebeatles.com', self.password)
        self.client.login(username=self.username, password=self.password)
        self.career_job = CareerJob.objects.create(
            job_title='Django', 
            job_description='Django board.',
            tag='test',
            job_location_city='KL',
            created_by=self.user
        )
        self.login_url = reverse('login')
        self.url = reverse('career_job_update', kwargs={ 'pk': self.career_job.pk })
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_redirect_not_login_status_code(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_redirect_not_found(self):
        self.url = reverse('career_job_update', kwargs={ 'pk': '3' })
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 404)

    def test_view_class(self):
        view = resolve('/job/1/edit/')
        self.assertEquals(view.func.view_class, CareerJobUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_successful_update(self):
        updated_job_title = 'Django'
        self.response = self.client.post(self.url, {'job_title': updated_job_title})
        self.career_job.refresh_from_db()
        self.assertEquals(self.career_job.job_title, updated_job_title)



