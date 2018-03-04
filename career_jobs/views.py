from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import  reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from .forms import CareerJobCreateForm
from .models import CareerJob


# CHORE: Apply this action to templates
class CareerJobActionMixin:

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(FlavorActionMixin, self).form_valid(form)

class CareerJobListView(ListView):
    model = CareerJob
    context_object_name = 'career_jobs'
    template_name = 'home.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        kwargs['total_count'] = CareerJob.objects.count()
        q = self.request.GET.get('q')

        # Handling search query
        if q:
            kwargs['has_search'] = True
            kwargs['search_param'] = q
        
        return super().get_context_data(**kwargs)


    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        
        # Handling search query
        if q:
            queryset = queryset.filter(
                Q(tag__icontains=q) | 
                Q(job_title__icontains=q) | 
                Q(job_location_country__icontains=q) | 
                Q(job_type__icontains=q) |
                Q(company_name__icontains=q)
            )

        return queryset.order_by('-updated_at')

class CareerJobCreateView(LoginRequiredMixin, CreateView):
    model = CareerJob
    form_class = CareerJobCreateForm
    template_name = 'career_job_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CareerJobUpdateView(LoginRequiredMixin, UpdateView):
    model = CareerJob
    context_object_name = 'career_job'
    template_name = 'career_job_update.html'
    fields = (
        'job_title', 
        'company_name', 
        'job_location_country', 
        'job_location_city', 
        'job_type', 
        'job_description',
        'job_status',
        'tag',
    )
    success_url = '/'

class CareerJobDetailView(DetailView):
    model = CareerJob
    context_object_name = 'career_job'
    template_name = 'career_job_detail.html'

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.kwargs['pk'])
        if not self.request.session.get(session_key, False):
            cj = CareerJob.objects.get(pk=self.kwargs['pk'])
            cj.views += 1
            cj.save()
            #self.request.session[session_key] = True
        return super().get_context_data(**kwargs)
