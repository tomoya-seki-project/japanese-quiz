from django.shortcuts import render
from django.conf import settings
from django.utils import timezone


def current_time_by_ymd_hms():
    return timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")