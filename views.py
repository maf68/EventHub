from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(city__icontains=query) |
                Q(location__icontains=query) |
                Q(promoter__username__icontains=query) |
                Q(event_type__icontains=query)
            )
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = Event.objects.order_by().values_list('city', flat=True).distinct()
        context['event_types'] = self.model.objects.order_by().values_list('event_type', flat=True).distinct()
        context['locations'] = Event.objects.values_list('city', flat=True).distinct()
        return context

class EventSearchView(ListView):
    model = Event
    template_name = 'events/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query and query.strip():
            object_list = Event.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(city__icontains=query) |
                Q(location__icontains=query) |
                Q(event_type__icontains=query) |
                Q(date__icontains=query) |
                Q(duration__icontains=query)
            )
            return object_list
        else:
            return Event.objects.none()

class SearchView(TemplateView):
    template_name = 'events/search_results.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            object_list = Event.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(city__icontains=query) |
                Q(location__icontains=query) |
                Q(event_type__icontains=query)
            )
        else:
            object_list = Event.objects.none()

        return self.render_to_response({'object_list': object_list, 'query': query})


class EventFilterView(ListView):
    model = Event
    template_name = 'events/event_filter.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.GET.get('location')
        date = self.request.GET.get('date')
        duration = self.request.GET.get('duration')
        event_type = self.request.GET.get('event_type')

        if location:
            queryset = queryset.filter(city=location)
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                queryset = queryset.filter(date__gte=date_obj)
            except ValueError:
                pass
        if duration:
            try:
                duration_obj = timedelta(hours=int(duration))
                queryset = queryset.filter(duration__lte=duration_obj)
            except ValueError:
                pass
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = Event.objects.order_by().values_list('city', flat=True).distinct()
        context['event_types'] = self.model.objects.order_by().values_list('event_type', flat=True).distinct()
        return context
