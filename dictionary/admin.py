from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import (
    VocabType,
    VocabCategory,
    VocabLevel,
    VocabRequestStatus,
    VocabRequestType,
)
from .models import (
    Vocab,
    UserVocab,
    VocabDetail,
    KatakanaDetail,
    VocabRequest,
)
@admin.register(Vocab)
class VocabAdmin(admin.ModelAdmin):
    pass

@admin.register(UserVocab)
class UserVocabAdmin(admin.ModelAdmin):
    pass

@admin.register(VocabRequest)
class VocabRequestAdmin(admin.ModelAdmin):
    pass

