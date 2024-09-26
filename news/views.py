from .models import News
from .serializers import NewsSerializer

from django.db.models import F
from django.shortcuts import render

from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'news': reverse('news-list', request=request, format=format),
        'search': reverse('news-search', request=request, format=format),
    })


def list(request):
    count = int(request.GET.get('count', '25'))
    page = int(request.GET.get('page', '1')) - 1
    news_list = News.objects.order_by(F('created').desc())[count * page : count * page + count]
    return render(request, "news/index.html", {"news_list": news_list})


def search(request):
    query = request.GET.get('query', '')
    news_list = News.objects.filter(title__contains=query).order_by(F('created').desc())
    return render(request, "news/search.html", {"news_list": news_list})


class NewsList(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter()

    def perform_create(self, serializer):
        serializer.save()