"""
Standalone script to import food items from CSV into FoodItem model

USAGE:
1. Place this in: resources/manage_resources.py
2. Make sure food_items_export.csv is in the project root
3. Run from project root: python resources/manage_resources.py
4. This will import all items from the CSV into the FoodItem table

The script will:
- Clear existing FoodItem data (optional - see CLEAR_EXISTING flag)
- Import all items from CSV
- Show statistics about what was imported
"""

import os
import sys
import django
import csv

# Setup Django environment
# Go up one level from resources/ to project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodbanked.settings')
django.setup()

# Now import models after Django is set up
from resources.models import FoodItem


# Configuration
CSV_FILE = 'food_items_export.csv'  # Path relative to project root
CLEAR_EXISTING = True  # Set to False if you want to keep existing data


def import_food_items():
    """Import food items from CSV into database"""
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"✗ Error: {CSV_FILE} not found in project root")
        print(f"  Current directory: {os.getcwd()}")
        print(f"  Make sure the CSV file is in the same directory as manage.py")
        return
    
    print("\n" + "="*60)
    print("Importing Food Items from CSV")
    print("="*60)
    
    # Optionally clear existing data
    if CLEAR_EXISTING:
        existing_count = FoodItem.objects.count()
        if existing_count > 0:
            confirm = input(f"\n⚠ This will delete {existing_count} existing food items. Continue? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Import cancelled.")
                return
            FoodItem.objects.all().delete()
            print(f"✓ Cleared {existing_count} existing items")
    
    # Read and import CSV
    items_created = 0
    items_skipped = 0
    errors = []
    
    with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        print(f"\nImporting from {CSV_FILE}...")
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (accounting for header row)
            try:
                # Parse numeric fields (handle empty strings)
                min_days = int(row['shelf_life_min_days']) if row['shelf_life_min_days'] else None
                max_days = int(row['shelf_life_max_days']) if row['shelf_life_max_days'] else None
                
                # Create FoodItem
                FoodItem.objects.create(
                    name=row['name'],
                    category=row['category'],
                    subcategory=row['subcategory'],
                    shelf_life_display=row['shelf_life_display'],
                    shelf_life_min_days=min_days,
                    shelf_life_max_days=max_days,
                    notes=row['notes']
                )
                items_created += 1
                
                # Show progress every 50 items
                if items_created % 50 == 0:
                    print(f"  Imported {items_created} items...")
                    
            except Exception as e:
                items_skipped += 1
                errors.append(f"Row {row_num}: {row.get('name', 'Unknown')} - {str(e)}")
    
    # Show results
    print("\n" + "="*60)
    print("Import Complete!")
    print("="*60)
    print(f"✓ Successfully imported: {items_created} items")
    
    if items_skipped > 0:
        print(f"⚠ Skipped: {items_skipped} items")
        print("\nErrors:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  • {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    # Show statistics
    print("\nBreakdown by category:")
    for category, label in FoodItem.CATEGORY_CHOICES:
        count = FoodItem.objects.filter(category=category).count()
        print(f"  • {label}: {count} items")
    
    print("\nItems with numeric shelf life:", 
          FoodItem.objects.exclude(shelf_life_min_days__isnull=True).count())
    print("Items using package date:", 
          FoodItem.objects.filter(shelf_life_min_days__isnull=True).count())
    
    print("\n" + "="*60)
    print("Next steps:")
    print("1. Verify data in Django admin: python manage.py createsuperuser")
    print("2. Build the Shelf Life search page")
    print("3. Test the autocomplete functionality")
    print("="*60 + "\n")


def show_stats():
    """Show statistics about current food items in database"""
    
    total = FoodItem.objects.count()
    
    print("\n" + "="*60)
    print("Food Items Database Statistics")
    print("="*60)
    print(f"\nTotal items: {total}")
    
    if total == 0:
        print("No items in database. Run import to add items.")
        return
    
    print("\nBy category:")
    for category, label in FoodItem.CATEGORY_CHOICES:
        count = FoodItem.objects.filter(category=category).count()
        percentage = (count / total * 100) if total > 0 else 0
        print(f"  • {label}: {count} ({percentage:.1f}%)")
    
    print("\nShelf life types:")
    numeric = FoodItem.objects.exclude(shelf_life_min_days__isnull=True).count()
    package_date = FoodItem.objects.filter(shelf_life_min_days__isnull=True).count()
    print(f"  • With numeric shelf life: {numeric}")
    print(f"  • Use package expiration: {package_date}")
    
    print("\nSample items:")
    for item in FoodItem.objects.all()[:5]:
        print(f"  • {item.name} ({item.get_category_display()}): {item.shelf_life_display}")
    
    print("="*60 + "\n")


def clear_all():
    """Clear all food items from database"""
    
    count = FoodItem.objects.count()
    if count == 0:
        print("No items to delete.")
        return
    
    confirm = input(f"\n⚠ This will delete ALL {count} food items. Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        FoodItem.objects.all().delete()
        print(f"✓ Deleted {count} items")
    else:
        print("Cancelled.")


def edit_subcategory():
    """Edit/rename a subcategory across all matching items"""
    
    print("\n" + "="*60)
    print("Edit Subcategory")
    print("="*60)
    
    # Show existing subcategories
    subcategories = FoodItem.objects.exclude(
        subcategory__isnull=True
    ).exclude(
        subcategory=''
    ).values_list('subcategory', flat=True).distinct().order_by('subcategory')
    
    if not subcategories:
        print("No subcategories found in database.")
        return
    
    print("\nExisting subcategories:")
    for i, subcat in enumerate(subcategories, 1):
        count = FoodItem.objects.filter(subcategory=subcat).count()
        print(f"  {i}. {subcat} ({count} items)")
    
    # Get current subcategory
    current = input("\nEnter the current subcategory name (or press Enter to cancel): ").strip()
    if not current:
        print("Cancelled.")
        return
    
    # Check if it exists
    matching_count = FoodItem.objects.filter(subcategory=current).count()
    if matching_count == 0:
        print(f"✓ No items found with subcategory '{current}'")
        return
    
    print(f"\nFound {matching_count} items with subcategory '{current}'")
    
    # Get replacement subcategory
    replacement = input("Enter the new subcategory name: ").strip()
    if not replacement:
        print("Replacement cannot be empty. Cancelled.")
        return
    
    # Confirm
    print(f"\nThis will change '{current}' to '{replacement}' for {matching_count} items.")
    confirm = input("Continue? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return
    
    # Perform update
    updated = FoodItem.objects.filter(subcategory=current).update(subcategory=replacement)
    
    print(f"\n✓ Successfully updated {updated} items")
    print(f"   Changed '{current}' → '{replacement}'")
    print("="*60 + "\n")


def remove_subcategory_from_name():
    """Remove trailing parenthetical text from item names like 'Item Name (subcategory)'"""
    
    print("\n" + "="*60)
    print("Remove Subcategory from Name")
    print("="*60)
    
    # Find items with names ending in )
    items_with_parens = FoodItem.objects.filter(name__endswith=')')
    count = items_with_parens.count()
    
    if count == 0:
        print("No items found with names ending in parentheses.")
        return
    
    print(f"\nFound {count} items with names ending in parentheses")
    
    # Show examples
    print("\nExamples of what will be changed:")
    for item in items_with_parens[:10]:
        # Preview the change
        original = item.name
        # Remove everything from the last ( to the end
        if '(' in original:
            new_name = original.rsplit('(', 1)[0].strip()
            print(f"  '{original}' → '{new_name}'")
    
    if count > 10:
        print(f"  ... and {count - 10} more items")
    
    # Confirm
    confirm = input(f"\nRemove trailing parentheses from {count} items? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return
    
    # Perform update
    updated_count = 0
    for item in items_with_parens:
        if '(' in item.name:
            # Remove everything from the last ( to the end, then trim whitespace
            new_name = item.name.rsplit('(', 1)[0].strip()
            item.name = new_name
            item.save()
            updated_count += 1
    
    print(f"\n✓ Successfully updated {updated_count} items")
    print("   Removed trailing parenthetical text from names")
    print("="*60 + "\n")



def export_to_csv():
    """Export all food items to CSV file"""
    
    print("\n" + "="*60)
    print("Export Food Items to CSV")
    print("="*60)
    
    # Check if there are items to export
    total = FoodItem.objects.count()
    if total == 0:
        print("No items in database to export.")
        return
    
    print(f"\nFound {total} items to export")
    
    # Get filename
    default_filename = 'food_items_export.csv'
    filename = input(f"\nEnter filename (default: {default_filename}): ").strip()
    if not filename:
        filename = default_filename
    
    # Make sure it ends with .csv
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    # Check if file exists
    if os.path.exists(filename):
        overwrite = input(f"âš  {filename} already exists. Overwrite? (yes/no): ")
        if overwrite.lower() != 'yes':
            print("Cancelled.")
            return
    
    # Export to CSV
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'name', 
                'category', 
                'subcategory', 
                'shelf_life_display',
                'shelf_life_min_days',
                'shelf_life_max_days',
                'notes'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            exported_count = 0
            for item in FoodItem.objects.all().order_by('category', 'name'):
                writer.writerow({
                    'name': item.name,
                    'category': item.category,
                    'subcategory': item.subcategory or '',
                    'shelf_life_display': item.shelf_life_display,
                    'shelf_life_min_days': item.shelf_life_min_days or '',
                    'shelf_life_max_days': item.shelf_life_max_days or '',
                    'notes': item.notes or ''
                })
                exported_count += 1
                
                # Show progress every 100 items
                if exported_count % 100 == 0:
                    print(f"  Exported {exported_count} items...")
        
        print(f"\n✓ Successfully exported {exported_count} items to {filename}")
        print(f"   File location: {os.path.abspath(filename)}")
        
        # Show breakdown
        print("\nBreakdown by category:")
        for category, label in FoodItem.CATEGORY_CHOICES:
            count = FoodItem.objects.filter(category=category).count()
            print(f"  • {label}: {count} items")
        
        print("\nYou can now:")
        print(f"  1. Copy {filename} to your production environment")
        print("  2. Run this script and select option 1 to import")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error exporting to CSV: {str(e)}")
        print("="*60 + "\n")

if __name__ == '__main__':
    print("\nFood Items Management Script")
    print("="*60)
    print("Options:")
    print("  1. Import food items from CSV")
    print("  2. Show database statistics")
    print("  3. Clear all food items")
    print("  4. Edit subcategory")
    print("  5. Remove subcategory from item names")
    print("  6. Export food items to CSV")
    print("  0. Exit")
    print("="*60)
    
    choice = input("\nSelect an option (0-6): ").strip()
    
    if choice == '1':
        import_food_items()
    elif choice == '2':
        show_stats()
    elif choice == '3':
        clear_all()
    elif choice == '4':
        edit_subcategory()
    elif choice == '5':
        remove_subcategory_from_name()
    elif choice == '6':
        export_to_csv()
    elif choice == '0':
        print("Goodbye!")
    else:
        print("Invalid option. Please run again and select 0-6.")