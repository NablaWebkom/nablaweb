# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, DetailView
from content.views.mixins import AdminLinksMixin, ViewAddMixin, PublishedMixin, update_published_state
from utils.view_mixins import FlatPageMixin

from .models import Podcast, Season, get_season_count


class SeasonView(FlatPageMixin, TemplateView):
    model = Season
    template_name = "podcast/season.html"
    flatpages = [("info", "/skraattcast/")]

    def get_context_data(self, **kwargs):
        data = super(SeasonView, self).get_context_data(**kwargs)

        try:
            if 'number' in kwargs:
                number = kwargs['number']
                season = Season.objects.get(number=number)
            else:
                season = Season.objects.order_by('-number')[0]

            data['season'] = season
            data['season_name'] = season.name()

            update_published_state(Podcast)
            data['podcast_list'] = Podcast.objects.filter(season=season, published=True).order_by('-pub_date').exclude(
                is_clip=True)
            data['podcast_clips'] = Podcast.objects.filter(season=season, published=True).order_by('-pub_date').exclude(
                is_clip=False)

            data['next'] = season.get_next()
            data['season_count'] = get_season_count()
            data['previous'] = season.get_previous()
        except IndexError:
            pass

        return data


class PodcastDetailView(PublishedMixin, ViewAddMixin, AdminLinksMixin, DetailView):
    template_name = 'podcast/podcast_detail.html'
    model = Podcast
    context_object_name = "podcast"

    def get_context_data(self, **kwargs):
        context = super(PodcastDetailView, self).get_context_data(**kwargs)
        context['season'] = season = self.object.season
        context['season_name'] = season.name()
        context['podcast_clips'] = Podcast.objects.filter(season=season, published=False).order_by('-pub_date').exclude(
            is_clip=False)
        return context