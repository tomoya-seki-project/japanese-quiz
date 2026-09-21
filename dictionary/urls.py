from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
    VocabHomeView,
    VocabCreateRequestView,
    VocabDetailView,
    VocabUpdateRequestView,
    VocabDeleteRequestView,
    VocabListFilterView,
    VocabListView,
    UserVocabListFilterView,
    UserVocabListView,
    UserVocabDetailView,
)

app_name = 'dictionary'

urlpatterns = [
    path('', VocabHomeView.as_view(), name='vocab_home'),
    path('vocab/create', VocabCreateRequestView.as_view(), name='vocab_create'),
    path('vocab/<int:pk>', VocabDetailView.as_view(), name='vocab_detail'),
    path('vocab/<int:vocab_id>/update/', VocabUpdateRequestView.as_view(), name='vocab_update'),
    path('vocab/<int:vocab_id>/delete/', VocabDeleteRequestView.as_view(), name='vocab_delete'),
    path('vocab/list_filter', VocabListFilterView.as_view(), name='vocab_list_filter'),
    path('vocab/list', VocabListView.as_view(), name='vocab_list'),
    path('user_vocab/list_filter', UserVocabListFilterView.as_view(), name='user_vocab_list_filter'),
    path('user_vocab/list', UserVocabListView.as_view(), name='user_vocab_list'),
    path('user_vocab/<int:pk>', UserVocabDetailView.as_view(), name='user_vocab_detail'),
]
