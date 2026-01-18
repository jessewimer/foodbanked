from django.utils import timezone
from zoneinfo import ZoneInfo

def get_foodbank_today(foodbank):
    """Get today's date in the foodbank's timezone"""

    now_utc = timezone.now()
    
    fb_tz = ZoneInfo(foodbank.timezone)
    now_local = now_utc.astimezone(fb_tz)
    
    result_date = now_local.date()
    
    return result_date