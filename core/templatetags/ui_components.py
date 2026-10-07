"""Presentation helpers shared by the Tailwind templates."""
import re
from django import forms, template
from django.utils.html import format_html, format_html_join
from django.utils import timezone

register = template.Library()

@register.filter
def ui_control(field):
    attrs = {}
    if field.errors:
        attrs.update({"aria-invalid": "true", "aria-describedby": f"{field.id_for_label}_errors"})
    if isinstance(field.field.widget, forms.Textarea):
        attrs["rows"] = 6 if field.name == "context" else 3
    if field.name == "meaning":
        return field.as_widget(forms.Textarea(), attrs={**attrs, "rows": 3})
    return field.as_widget(attrs=attrs)

@register.simple_tag
def selection_options(field):
    value = field.value()
    selected = {str(v) for v in value} if isinstance(value, (list, tuple)) else {str(value)}
    multiple = isinstance(field.field, (forms.MultipleChoiceField, forms.ModelMultipleChoiceField))
    return [{"value": str(v), "label": label, "selected": str(v) in selected,
             "type": "checkbox" if multiple else "radio"} for v, label in field.field.choices if str(v) != ""]

@register.simple_tag
def pagination_data(page, request):
    def url(number):
        query = request.GET.copy()
        query["page"] = str(number)
        return "?" + query.urlencode()
    start = max(1, min(page.number - 2, page.paginator.num_pages - 4))
    return {"first": url(1), "previous": url(max(1, page.number - 1)),
            "next": url(min(page.paginator.num_pages, page.number + 1)), "last": url(page.paginator.num_pages),
            "numbers": [{"number": n, "url": url(n)} for n in range(start, min(page.paginator.num_pages + 1, start + 5))]}

@register.filter
def event_short_label(value):
    return {"vocab_request_result": "申請結果", "vocab": "単語",
            "weight_update_by_system": "優先度更新", "feedback_reply": "フィードバック返信",
            "new_vocab_request": "新規申請"}.get(value, "お知らせ")

@register.filter
def absolute(value):
    return abs(value or 0)

@register.filter
def weight_width(value):
    return max(0.5, min(100, (value or 1) / 2))

@register.filter
def weight_color(value):
    for ceiling, color in [(50,"#BFE8F7"),(100,"#8BC9E6"),(150,"#E6B85C"),(200,"#D9854B"),(300,"#AD4B55"),(500,"#73528D")]:
        if value < ceiling:
            return color
    return "#3F344A"

@register.filter
def example_answer(question, answer):
    parts = re.split(r"_+", question or "")
    return format_html_join(format_html('<strong class="text-icon">{}</strong>', answer), "{}", ((part,) for part in parts))

@register.filter
def relative_quiz_time(value):
    if not value:
        return "いつですかね？"
    seconds = max(0, (timezone.now() - value).total_seconds())
    if seconds < 3600:
        return f"{int(seconds // 60)}分前"
    if seconds < 86400:
        return f"{int(seconds // 3600)}時間前"
    return f"{int(seconds // 86400)}日前"

@register.filter
def actual_quiz_time(value):
    if not value:
        return "早くクイズしろ"
    local = timezone.localtime(value)
    if (timezone.now() - value).total_seconds() < 86400:
        return local.strftime("%Y年%m月%d日 %H:%M")
    minute = local.hour * 60 + local.minute
    period = "朝" if 360 < minute <= 720 else "昼" if 720 < minute <= 1080 else "明け方" if 120 < minute <= 360 else "夜"
    return local.strftime("%Y年%m月%d日 ") + period
