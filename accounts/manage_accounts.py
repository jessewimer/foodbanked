#!/usr/bin/env python
"""
FoodBanked Account Management CLI
Simple menu-driven interface for managing foodbank accounts
"""

import os
import sys
import django
from django.db.models import Q

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodbanked.settings')
django.setup()

from accounts.models import Foodbank, FoodbankOrganization


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Print a nice header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_foodbank(foodbank):
    """Display foodbank information nicely"""
    tz_display = "PST" if foodbank.timezone == "America/Los_Angeles" else "MST" if foodbank.timezone == "America/Boise" else foodbank.timezone
    
    print(f"  ID: {foodbank.id}")
    print(f"  Name: {foodbank.name}")
    print(f"  Address: {foodbank.address or 'Not set'}")
    print(f"  City: {foodbank.city or 'Not set'}")
    print(f"  State: {foodbank.state or 'Not set'}")
    print(f"  Zip Code: {foodbank.zipcode or 'Not set'}")
    print(f"  Phone: {foodbank.phone or 'Not set'}")
    print(f"  Email: {foodbank.email or 'Not set'}")
    print(f"  Timezone: {tz_display}")
    print(f"  Food Truck Enabled: {'Yes' if foodbank.food_truck_enabled else 'No'}")
    print(f"  Created: {foodbank.created_date.strftime('%B %d, %Y')}")


def view_all_foodbanks():
    """Display all foodbanks"""
    clear_screen()
    print_header("All Food Banks")
    
    foodbanks = Foodbank.objects.all().order_by('name')
    
    if not foodbanks:
        print("  No food banks found.\n")
        input("Press Enter to continue...")
        return
    
    for fb in foodbanks:
        print(f"\n{'-' * 60}")
        print_foodbank(fb)
    
    print(f"\n{'-' * 60}")
    print(f"\nTotal: {foodbanks.count()} food bank(s)")
    input("\nPress Enter to continue...")


def edit_foodbank():
    """Edit a foodbank's information"""
    clear_screen()
    print_header("Edit Food Bank")
    
    # List all foodbanks
    foodbanks = Foodbank.objects.all().order_by('name')
    
    if not foodbanks:
        print("  No food banks found.\n")
        input("Press Enter to continue...")
        return
    
    print("Available food banks:\n")
    for i, fb in enumerate(foodbanks, 1):
        print(f"  {i}. {fb.name}")
    
    print("\n  0. Cancel")
    
    # Get selection
    try:
        choice = input("\nSelect a food bank (enter number): ").strip()
        if choice == '0':
            return
        
        idx = int(choice) - 1
        if idx < 0 or idx >= len(foodbanks):
            print("\nInvalid selection!")
            input("Press Enter to continue...")
            return
        
        foodbank = foodbanks[idx]
    except (ValueError, IndexError):
        print("\nInvalid selection!")
        input("Press Enter to continue...")
        return
    
    # Show current info
    clear_screen()
    print_header(f"Editing: {foodbank.name}")
    print("Current information:\n")
    print_foodbank(foodbank)
    
    print("\n" + "=" * 60)
    print("\nEnter new values (press Enter to keep current value):\n")
    
    # Collect new values
    pending_changes = {}
    
    # Name
    name = input(f"Name [{foodbank.name}]: ").strip()
    pending_changes['name'] = name if name else foodbank.name
    
    # Address
    address = input(f"Address [{foodbank.address or 'Not set'}]: ").strip()
    pending_changes['address'] = address if address else foodbank.address
    
    # City
    city = input(f"City [{foodbank.city or 'Not set'}]: ").strip()
    pending_changes['city'] = city if city else foodbank.city
    
    # State
    state = input(f"State [{foodbank.state or 'Not set'}]: ").strip()
    pending_changes['state'] = state if state else foodbank.state
    
    # Zip Code
    zipcode = input(f"Zip Code [{foodbank.zipcode or 'Not set'}]: ").strip()
    pending_changes['zipcode'] = zipcode if zipcode else foodbank.zipcode
    
    # Phone
    phone = input(f"Phone [{foodbank.phone or 'Not set'}]: ").strip()
    pending_changes['phone'] = phone if phone else foodbank.phone
    
    # Email
    email = input(f"Email [{foodbank.email or 'Not set'}]: ").strip()
    pending_changes['email'] = email if email else foodbank.email
    
    # Timezone
    current_tz = "P" if foodbank.timezone == "America/Los_Angeles" else "M" if foodbank.timezone == "America/Boise" else "?"
    tz_input = input(f"Timezone [P=PST, M=Mountain] (current: {current_tz}): ").strip().upper()
    
    if tz_input == 'P':
        pending_changes['timezone'] = 'America/Los_Angeles'
    elif tz_input == 'M':
        pending_changes['timezone'] = 'America/Boise'
    else:
        pending_changes['timezone'] = foodbank.timezone
    
    # Food Truck Enabled
    ft_current = 'Y' if foodbank.food_truck_enabled else 'N'
    ft_input = input(f"Food Truck Enabled [Y/N] (current: {ft_current}): ").strip().upper()
    
    if ft_input == 'Y':
        pending_changes['food_truck_enabled'] = True
    elif ft_input == 'N':
        pending_changes['food_truck_enabled'] = False
    else:
        pending_changes['food_truck_enabled'] = foodbank.food_truck_enabled
    
    # Show pending changes for confirmation
    clear_screen()
    print_header("Confirm Changes")
    
    tz_display = "PST" if pending_changes['timezone'] == "America/Los_Angeles" else "MST"
    
    print("Pending changes:\n")
    print(f"  Name: {pending_changes['name']}")
    print(f"  Address: {pending_changes['address'] or 'Not set'}")
    print(f"  City: {pending_changes['city'] or 'Not set'}")
    print(f"  State: {pending_changes['state'] or 'Not set'}")
    print(f"  Zip Code: {pending_changes['zipcode'] or 'Not set'}")
    print(f"  Phone: {pending_changes['phone'] or 'Not set'}")
    print(f"  Email: {pending_changes['email'] or 'Not set'}")
    print(f"  Timezone: {tz_display}")
    print(f"  Food Truck Enabled: {'Yes' if pending_changes['food_truck_enabled'] else 'No'}")
    
    confirm = input("\nSave these changes? [Y/N]: ").strip().upper()
    
    if confirm == 'Y':
        # Apply changes
        for key, value in pending_changes.items():
            setattr(foodbank, key, value)
        foodbank.save()
        
        print("\n✓ Changes saved successfully!")
    else:
        print("\n✗ Changes discarded.")
    
    input("\nPress Enter to continue...")



def add_foodbank_organization():
    """Add a new organization"""
    clear_screen()
    print_header("Add New Organization")
    
    print("Enter organization details:\n")
    
    # Collect organization info
    name = input("Organization Name: ").strip()
    if not name:
        print("\nError: Organization name is required!")
        input("Press Enter to continue...")
        return
    
    address = input("Address (optional): ").strip()
    city = input("City (optional): ").strip()
    state = input("State (optional): ").strip()
    zipcode = input("Zip Code (optional): ").strip()
    phone = input("Phone (optional): ").strip()
    email = input("Email (optional): ").strip()
    website = input("Website (optional): ").strip()
    
    # Show confirmation
    clear_screen()
    print_header("Confirm New Organization")
    
    print("Organization details:\n")
    print(f"  Name: {name}")
    print(f"  Address: {address or 'Not set'}")
    print(f"  City: {city or 'Not set'}")
    print(f"  State: {state or 'Not set'}")
    print(f"  Zip Code: {zipcode or 'Not set'}")
    print(f"  Phone: {phone or 'Not set'}")
    print(f"  Email: {email or 'Not set'}")
    print(f"  Website: {website or 'Not set'}")
    
    confirm = input("\nCreate this organization? [Y/N]: ").strip().upper()
    
    if confirm == 'Y':
        try:
            org = FoodbankOrganization.objects.create(
                name=name,
                address=address or None,
                city=city or None,
                state=state or None,
                zipcode=zipcode or None,
                phone=phone or None,
                email=email or None,
                website=website or None
            )
            print(f"\n✓ Organization '{org.name}' created successfully!")
        except Exception as e:
            print(f"\n✗ Error creating organization: {e}")
    else:
        print("\n✗ Organization creation cancelled.")
    
    input("\nPress Enter to continue...")


def assign_foodbank_to_organization():
    """Assign a foodbank to an organization"""
    clear_screen()
    print_header("Assign Food Bank to Organization")
    
    # Check if there are organizations
    organizations = FoodbankOrganization.objects.all().order_by('name')
    if not organizations:
        print("  No organizations found. Please create an organization first.\n")
        input("Press Enter to continue...")
        return
    
    # Check if there are foodbanks
    foodbanks = Foodbank.objects.all().order_by('name')
    if not foodbanks:
        print("  No food banks found.\n")
        input("Press Enter to continue...")
        return
    
    # Select organization
    print("Available organizations:\n")
    for i, org in enumerate(organizations, 1):
        fb_count = org.foodbanks.count()
        print(f"  {i}. {org.name} ({fb_count} food bank{'s' if fb_count != 1 else ''})")
    
    print("\n  0. Cancel")
    
    try:
        choice = input("\nSelect an organization (enter number): ").strip()
        if choice == '0':
            return
        
        idx = int(choice) - 1
        if idx < 0 or idx >= len(organizations):
            print("\nInvalid selection!")
            input("Press Enter to continue...")
            return
        
        organization = organizations[idx]
    except (ValueError, IndexError):
        print("\nInvalid selection!")
        input("Press Enter to continue...")
        return
    
    # Select foodbank
    clear_screen()
    print_header(f"Assign Food Bank to: {organization.name}")
    
    print("Available food banks:\n")
    for i, fb in enumerate(foodbanks, 1):
        org_name = fb.organization.name if fb.organization else "Not assigned"
        print(f"  {i}. {fb.name} (Currently: {org_name})")
    
    print("\n  0. Cancel")
    
    try:
        choice = input("\nSelect a food bank (enter number): ").strip()
        if choice == '0':
            return
        
        idx = int(choice) - 1
        if idx < 0 or idx >= len(foodbanks):
            print("\nInvalid selection!")
            input("Press Enter to continue...")
            return
        
        foodbank = foodbanks[idx]
    except (ValueError, IndexError):
        print("\nInvalid selection!")
        input("Press Enter to continue...")
        return
    
    # Show confirmation
    clear_screen()
    print_header("Confirm Assignment")
    
    current_org = foodbank.organization.name if foodbank.organization else "None"
    
    print(f"  Food Bank: {foodbank.name}")
    print(f"  Current Organization: {current_org}")
    print(f"  New Organization: {organization.name}")
    
    confirm = input("\nConfirm this assignment? [Y/N]: ").strip().upper()
    
    if confirm == 'Y':
        try:
            foodbank.organization = organization
            foodbank.save()
            print(f"\n✓ '{foodbank.name}' assigned to '{organization.name}' successfully!")
        except Exception as e:
            print(f"\n✗ Error assigning food bank: {e}")
    else:
        print("\n✗ Assignment cancelled.")
    
    input("\nPress Enter to continue...")



def geocode_all_locations():
    """Geocode all foodbanks and organizations missing coordinates"""
    clear_screen()
    print_header("Geocode Locations")
    
    print("This will automatically generate latitude/longitude coordinates")
    print("for all foodbanks and organizations based on their addresses.\n")
    
    confirm = input("Continue? [Y/N]: ").strip().upper()
    
    if confirm != 'Y':
        print("\nGeocoding cancelled.")
        input("\nPress Enter to continue...")
        return
    
    print("\n" + "=" * 60)
    print("Starting geocoding process...")
    print("=" * 60 + "\n")
    
    # Geocode foodbanks
    
    foodbanks = Foodbank.objects.filter(Q(latitude__isnull=True) | Q(longitude__isnull=True))
    print(f"Found {foodbanks.count()} foodbanks needing geocoding...\n")
    
    fb_success = 0
    fb_failed = 0
    
    for fb in foodbanks:
        print(f"Geocoding: {fb.name}...")
        fb.save()  # This triggers the geocode() method
        fb.refresh_from_db()  # <-- Add this line to reload from database
        
        if fb.latitude and fb.longitude:
            print(f"  ✓ Success: {fb.latitude}, {fb.longitude}")
            fb_success += 1
        else:
            print(f"  ✗ Failed: Could not geocode (check address)")
            fb_failed += 1
    
    # Geocode organizations
    print(f"\n{'-' * 60}\n")
    orgs = FoodbankOrganization.objects.filter(latitude__isnull=True)
    print(f"Found {orgs.count()} organizations needing geocoding...\n")
    
    org_success = 0
    org_failed = 0
    
    for org in orgs:
        print(f"Geocoding: {org.name}...")
        org.save()  # This triggers the geocode() method
        org.refresh_from_db()  # <-- Add this line to reload from database
        
        if org.latitude and org.longitude:
            print(f"  ✓ Success: {org.latitude}, {org.longitude}")
            org_success += 1
        else:
            print(f"  ✗ Failed: Could not geocode (check address)")
            org_failed += 1
    
    # Summary
    print(f"\n{'=' * 60}")
    print("Geocoding Complete!")
    print("=" * 60)
    print(f"\nFoodbanks:")
    print(f"  ✓ Successfully geocoded: {fb_success}")
    print(f"  ✗ Failed: {fb_failed}")
    print(f"\nOrganizations:")
    print(f"  ✓ Successfully geocoded: {org_success}")
    print(f"  ✗ Failed: {org_failed}")
    print(f"\nTotal: {fb_success + org_success} locations geocoded")
    
    input("\nPress Enter to continue...")


def set_all_locations_public():
    """Set all foodbanks and organizations to public"""
    clear_screen()
    print_header("Set All Locations to Public")
    
    foodbanks = Foodbank.objects.all()
    orgs = FoodbankOrganization.objects.all()
    
    print(f"This will set {foodbanks.count()} foodbanks and {orgs.count()} organizations to public.\n")
    print("Public locations will appear on the public locations map at /locations/\n")
    
    confirm = input("Continue? [Y/N]: ").strip().upper()
    
    if confirm != 'Y':
        print("\nCancelled.")
        input("\nPress Enter to continue...")
        return
    
    print("\n" + "=" * 60)
    
    # Update foodbanks
    fb_updated = 0
    for fb in foodbanks:
        fb.is_public = True
        fb.save()
        fb_updated += 1
        print(f"✓ {fb.name} set to public")
    
    # Update organizations
    org_updated = 0
    for org in orgs:
        org.is_public = True
        org.save()
        org_updated += 1
        print(f"✓ {org.name} set to public")
    
    print("=" * 60)
    print(f"\n✓ Updated {fb_updated} foodbanks and {org_updated} organizations to public")
    
    input("\nPress Enter to continue...")

def main_menu():
    """Display main menu and handle selection"""
    while True:
        clear_screen()
        print_header("FoodBanked Account Management")
        
        print("  1. View all food banks")
        print("  2. Edit food bank")
        print("  3. Add food bank organization")
        print("  4. Assign food bank to organization")
        print("  5. Geocode all locations")
        print("  6. Set all locations to public")
        print("\n  0. Exit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == '1':
            view_all_foodbanks()
        elif choice == '2':
            edit_foodbank()
        elif choice == '3':
            add_foodbank_organization()
        elif choice == '4':
            assign_foodbank_to_organization()
        elif choice == '5':
            geocode_all_locations()
        elif choice == '6':
            set_all_locations_public()
        elif choice == '0':
            clear_screen()
            print("\nGoodbye!\n")
            sys.exit(0)
        else:
            print("\nInvalid option!")
            input("Press Enter to continue...")


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\nExiting...\n")
        sys.exit(0)