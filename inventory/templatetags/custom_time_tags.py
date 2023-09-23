from django.utils import timezone as tz
from django import template
import dateutil.parser
import pytz

register = template.Library()


@register.simple_tag
def get_local_now():
    return tz.localtime(tz.now(), pytz.timezone("America/New_York"))


@register.simple_tag
def get_local_now_format(formatt: str):
    # print(
    #     tz.localtime(tz.now(), pytz.timezone("America/New_York")).strftime(
    #         "%Y-%m-%dT%H:%M:%S "
    #     )
    # )
    return tz.localtime(tz.now(), pytz.timezone("America/New_York")).strftime(formatt)


@register.simple_tag
def get_today():
    return tz.localtime(tz.now(), pytz.timezone("America/New_York")).date()
