# foodbanked/geocoding.py
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

def geocode_address(address, city, state, zipcode):
    """
    Convert address to latitude/longitude coordinates.
    Returns (latitude, longitude) tuple or (None, None) if geocoding fails.
    """
    # Build full address string
    address_parts = []
    if address:
        address_parts.append(str(address).strip())
    if city:
        address_parts.append(str(city).strip())
    if state:
        address_parts.append(str(state).strip())
    if zipcode:
        address_parts.append(str(zipcode).strip())
    
    full_address = ', '.join(address_parts)
    
    if not full_address:
        return None, None
    
    try:
        # Use Nominatim (OpenStreetMap's free geocoding service)
        geolocator = Nominatim(user_agent="foodbanked_app")
        
        # Add small delay to respect rate limits (1 req/sec)
        time.sleep(1)
        
        location = geolocator.geocode(full_address)
        
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Could not geocode: {full_address}")
            return None, None
            
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error for {full_address}: {e}")
        return None, None