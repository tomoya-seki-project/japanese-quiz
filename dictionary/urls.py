from django.urls import path
from django.views.generic.base import TemplateView

from .views import vocab
from .views.vocab import (
    VocabHomeView,
    VocabCreateRequestView,
    VocabDetailView,
    VocabUpdateRequestView,
    VocabDeleteRequestView,
    VocabListView,    
)

app_name = 'dictionary'

urlpatterns = [
    path('home/', VocabHomeView.as_view(), name='vocab_home'),
    path('vocab/create', VocabCreateRequestView.as_view(), name='vocab_create'),
    path('vocab/<int:vocab_id>', VocabDetailView.as_view(), name='vocab_detail'),
    path('vocab/<int:vocab_id>/update/', VocabUpdateRequestView.as_view(), name='vocab_update'),
    path('vocab/<int:vocab_id>/delete/', VocabDeleteRequestView.as_view(), name='vocab_delete'),
    path('vocab/list', VocabListView.as_view(), name='vocab_list'),
]
