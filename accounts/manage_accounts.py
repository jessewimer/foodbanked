#!/usr/bin/env python
"""
FoodBanked Account Management CLI
Simple menu-driven interface for managing foodbank accounts
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodbanked.settings')
django.setup()

from accounts.models import Foodbank


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


def main_menu():
    """Display main menu and handle selection"""
    while True:
        clear_screen()
        print_header("FoodBanked Account Management")
        
        print("  1. View all food banks")
        print("  2. Edit food bank")
        print("\n  0. Exit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == '1':
            view_all_foodbanks()
        elif choice == '2':
            edit_foodbank()
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