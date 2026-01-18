# from django.utils import timezone
# from zoneinfo import ZoneInfo

# def get_foodbank_today(foodbank):
#     """Get today's date in the foodbank's timezone"""
#     fb_tz = ZoneInfo(foodbank.timezone)
#     now = timezone.now().astimezone(fb_tz)
#     return now.date()
from django.utils import timezone
from zoneinfo import ZoneInfo

def get_foodbank_today(foodbank):
    """Get today's date in the foodbank's timezone"""
    
    print("=" * 60)
    print("DEBUG: get_foodbank_today() called")
    print(f"Foodbank ID: {foodbank.id}")
    print(f"Foodbank Name: {foodbank.name}")
    print(f"Timezone from DB: {foodbank.timezone}")
    
    now_utc = timezone.now()
    print(f"Current UTC time: {now_utc}")
    
    fb_tz = ZoneInfo(foodbank.timezone)
    now_local = now_utc.astimezone(fb_tz)
    print(f"Converted to local time: {now_local}")
    
    result_date = now_local.date()
    print(f"Date being returned: {result_date}")
    print("=" * 60)
    
    return result_date