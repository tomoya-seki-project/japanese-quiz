from django import template
from core.ui import EVENT_TYPES, VOCAB_LEVELS, VOCAB_TYPES

register = template.Library()


@register.filter
def event_label(value):
    return EVENT_TYPES.get(value, "お知らせ")


@register.filter
def vocab_type_label(value):
    return VOCAB_TYPES.get(value, "その他")


@register.filter
def vocab_level_label(value):
    return VOCAB_LEVELS.get(str(value), "未設定")


@register.filter
def kana_key_label(value):
    return {'"': '゛', '。': '゜'}.get(value, value)

