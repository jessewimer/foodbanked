from django.utils import timezone
from zoneinfo import ZoneInfo

def get_foodbank_today(foodbank):
    """Get today's date in the foodbank's timezone"""
    fb_tz = ZoneInfo(foodbank.timezone)
    now = timezone.now().astimezone(fb_tz)
    return now.date()