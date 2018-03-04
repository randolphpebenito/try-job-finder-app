import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator

from markdown import markdown

class CareerJob(models.Model):
    COUNTRY_MALAYSIA = 'Malaysia'
    COUNTRY_SINGAPORE = 'Singapore'
    COUNTRY_PHILIPPINES = 'Philippines'
    COUNTRY_THAILAND = 'Thailand'

    COUNTRY_CHOICES = (
	(COUNTRY_MALAYSIA, 'Malaysia'),
	(COUNTRY_SINGAPORE, 'Singapore'),
	(COUNTRY_PHILIPPINES, 'Philippines'),
	(COUNTRY_THAILAND, 'Thailand'),
    )

    JOB_FULL_TIME = 'Full Time'
    JOB_PART_TIME = 'Part Time'

    JOB_TYPE_CHOICES = (
	(JOB_FULL_TIME, 'Full Time'),
	(JOB_PART_TIME, 'Part Time'),
    )

    JOB_STATUS_AVAILABLE = 'Open'
    JOB_STATUS_NOT_AVAILABLE = 'Closed'

    JOB_STATUS_CHOICES = (
	(JOB_STATUS_AVAILABLE, 'Open'),
	(JOB_STATUS_NOT_AVAILABLE, 'Closed'),
    )

    job_title = models.CharField(max_length=255, blank=False, help_text=u"Minimum characters 7")
    job_location_country = models.CharField(max_length=32, choices=COUNTRY_CHOICES, default=COUNTRY_CHOICES[0][1])
    job_location_city = models.CharField(max_length=64, verbose_name='City')
    job_type = models.CharField(max_length=32, choices=JOB_TYPE_CHOICES, default=JOB_TYPE_CHOICES[0][1])
    job_description = models.TextField(max_length=4000)
    tag = models.CharField(max_length=64, blank=False)
    job_status = models.CharField(max_length=32, choices=JOB_STATUS_CHOICES, default=JOB_STATUS_CHOICES[0][1])
    company_name = models.CharField(max_length=64, blank=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='user')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        return self.job_title

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def get_job_count(self):
        return CareerJob.objects.count()

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_job_description_as_markdown(self):
        return mark_safe(markdown(self.job_description, safe_mode='escape'))

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]
