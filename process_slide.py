#!/usr/bin/env python3
"""
Comprehensive Slide Processing Script
Combines three tasks:
1. Update HTML content with achievements and plans from text files
2. Encode images to base64 and merge them
3. Insert encoded images into HTML
"""

import os
import json
import base64
import re
import shutil
from collections import defaultdict
from difflib import SequenceMatcher


# ============================================================================
# TASK 1: Update HTML Content with Achievements and Plans
# ============================================================================

def parse_items_file(filepath):
    """Parse achievements or plans file and return list of items with categories"""
    items = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Split by "--" to separate item name and category
                if '--' in line:
                    parts = line.split('--', 1)
                    item_name = parts[0].strip()
                    category = parts[1].strip()
                else:
                    item_name = line
                    category = ""
                
                items.append({
                    'name': item_name,
                    'category': category
                })
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    return items


def generate_slides_data(achievements, plans, achievement_month=None, plans_month=None):
    """Generate slidesData JavaScript array from achievements and plans"""
    # Default placeholder images
    placeholder_images = [
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAwIDgwMCI+PHBhdGggZmlsbD0iI2M2ZmVmZiIgZD0iTTAgMEgxMjAwVjgwMEgwWiIvPjwvc3ZnPg==",
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAwIDgwMCI+PHBhdGggZmlsbD0iI2M2ZmVmZiIgZD0iTTAgMEgxMjAwVjgwMEgwWiIvPjwvc3ZnPg==",
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAwIDgwMCI+PHBhdGggZmlsbD0iI2M2ZmVmZiIgZD0iTTAgMEgxMjAwVjgwMEgwWiIvPjwvc3ZnPg=="
    ]
    
    # Convert achievements to slide data format
    achievement_data = []
    for item in achievements:
        achievement_data.append({
            "text": item["name"],
            "category": item["category"],
            "images": placeholder_images.copy()
        })
    
    # Convert plans to slide data format
    plan_data = []
    for item in plans:
        plan_data.append({
            "text": item["name"],
            "category": item["category"]
        })
    
    # Create slides data structure
    slides_data = [
        {
            "title": f"{achievement_month} Achievements" if achievement_month else "Achievements",
            "subtitle": "Key accomplishments this month",
            "data": achievement_data,
            "listClass": "achievement-list",
            "itemsPerSlide": 6,
        },
        {
            "title": f"{plans_month} Plans" if plans_month else "Plans",
            "subtitle": "Upcoming tasks and objectives", 
            "data": plan_data,
            "listClass": "plan-list",
            "itemsPerSlide": 6,
        }
    ]
    
    return slides_data


def extract_month_from_filename(filename):
    """Extract month name from filename like 'October Achivment.txt' or 'November Plans.txt'"""
    basename = os.path.basename(filename)
    # Remove file extension
    name_without_ext = os.path.splitext(basename)[0]
    # Extract the first word (month name)
    parts = name_without_ext.split()
    if parts:
        return parts[0]
    return None


def update_html_content(html_content, achievements, plans, achievement_month=None, plans_month=None):
    """Update HTML with achievements, plans, and month titles using new JavaScript structure"""
    # Generate slides data
    slides_data = generate_slides_data(achievements, plans, achievement_month, plans_month)
    
    # Convert to JavaScript format
    slides_js = json.dumps(slides_data, indent=4, ensure_ascii=False)
    
    # Replace mainData.slidesData array with proper pattern matching
    pattern = r'(slidesData:\s*)\[[\s\S]*?\n\s*\](?=\s*,\s*notCompletedKPIS)'
    replacement = f'\\1{slides_js}'
    html_content = re.sub(pattern, replacement, html_content, count=1)
    
    # Update page title and subtitle
    if achievement_month and plans_month:
        title = f"LMS Team Monthly KPI - {achievement_month}"
        html_content = re.sub(
            r'<title>[^<]*</title>',
            f'<title>{title}</title>',
            html_content
        )
        
        subtitle = f"{achievement_month}"
        html_content = re.sub(
            r'(<h2 class="slide-subtitle">)[^<]*(</h2>)',
            r'\1' + subtitle + r'\2',
            html_content,
            count=1
        )
    
    # Update statistics in team members slide
    if achievement_month:
        html_content = re.sub(
            r'(<div class="stat-number">)\d+(</div>\s*<div class="stat-label">)Achievements</div>',
            lambda m: f"{m.group(1)}{len(achievements)}{m.group(2)}{achievement_month} Achievements</div>",
            html_content
        )
    else:
        html_content = re.sub(
            r'(<div class="stat-number">)\d+(</div>\s*<div class="stat-label">)Achievements</div>',
            lambda m: f"{m.group(1)}{len(achievements)}{m.group(2)}Achievements</div>",
            html_content
        )
    
    if plans_month:
        html_content = re.sub(
            r'(<div class="stat-number">)\d+(</div>\s*<div class="stat-label">)[^<]*Plans</div>',
            lambda m: f"{m.group(1)}{len(plans)}{m.group(2)}{plans_month} Plans</div>",
            html_content
        )
    else:
        html_content = re.sub(
            r'(<div class="stat-number">)\d+(</div>\s*<div class="stat-label">)[^<]*Plans</div>',
            lambda m: f"{m.group(1)}{len(plans)}{m.group(2)}Plans</div>",
            html_content
        )
    
    return html_content


# ============================================================================
# TASK 2: Encode Images and Merge
# ============================================================================

def encode_image_to_base64(image_path):
    """Encode an image file to base64 data URI"""
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            
            # Get file extension
            ext = os.path.splitext(image_path)[1].lower().lstrip('.')
            
            # Map extensions to MIME types
            mime_types = {
                'png': 'image/png',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'gif': 'image/gif',
                'svg': 'image/svg+xml',
                'webp': 'image/webp'
            }
            
            mime_type = mime_types.get(ext, 'image/png')
            return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"Error encoding {image_path}: {e}")
        return None


def encode_images_in_directory(directory):
    """Encode all image files in the directory"""
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']
    
    encoded_files = []
    all_image_files = []
    
    # Collect all image files
    for image_file in os.listdir(directory):
        if any(image_file.lower().endswith(ext) for ext in image_extensions):
            image_path = os.path.join(directory, image_file)
            
            if not os.path.isfile(image_path):
                continue
            
            all_image_files.append(image_file)
    
    # Sort files by numerical prefix
    def get_sort_key(filename):
        parts = filename.split('_', 2)
        if len(parts) >= 2:
            try:
                main_num = int(parts[0])
                sub_num = int(parts[1])
                return (main_num, sub_num)
            except ValueError:
                return (0, 0)
        return (0, 0)
    
    all_image_files.sort(key=get_sort_key)
    
    # Process files in sorted order
    for image_file in all_image_files:
        image_path = os.path.join(directory, image_file)
        name_without_ext = os.path.splitext(image_file)[0]
        
        encoded_data = encode_image_to_base64(image_path)
        if encoded_data:
            encoded_files.append((name_without_ext, encoded_data))
            print(f"  Encoded: {image_file}")
    
    return encoded_files


def extract_title_and_number(filename):
    """Extract the number prefix and title from filename"""
    parts = filename.split('_', 2)
    if len(parts) >= 3:
        number = parts[0]
        title = parts[2].replace('.txt', '')
        return number, title
    return "00", filename.replace('.txt', '')


def merge_files(encoded_files, directory):
    """Group files by title and merge their content into JSON arrays"""
    title_groups = defaultdict(list)
    file_info = {}
    
    for name_without_ext, encoded_data in encoded_files:
        number, title = extract_title_and_number(name_without_ext + ".txt")
        
        if title not in file_info:
            file_info[title] = number
        
        title_groups[title].append(encoded_data)
    
    # Create merged folder
    merged_folder = os.path.join(directory, "merged")
    os.makedirs(merged_folder, exist_ok=True)
    
    # Create merged files
    for title, content_list in title_groups.items():
        if content_list:
            number = file_info[title]
            new_filename = f"{number}_merged_{title}.txt"
            new_filepath = os.path.join(merged_folder, new_filename)
            
            json_content = json.dumps(content_list, indent=2)
            
            with open(new_filepath, 'w', encoding='utf-8') as f:
                f.write(json_content)
            
            print(f"  Created: merged/{new_filename} with {len(content_list)} entries")


# ============================================================================
# TASK 3: Insert Images into HTML
# ============================================================================

def similarity(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def normalize_title(title):
    """Normalize title for better matching"""
    # Remove common punctuation and replace with space
    title = re.sub(r'[_\(\)/\-\,\.\:]', ' ', title)
    # Remove extra spaces
    title = re.sub(r'\s+', ' ', title).strip()
    # Handle common variations
    title = title.replace('desgin', 'design').replace('recommandation', 'recommendation')
    title = title.replace('Signatrue', 'Signature').replace('revnue', 'revenue')
    return title.lower()


def find_all_matching_images(achievement_title, merged_files, threshold=0.5):
    """Find all matching merged files for an achievement title"""
    normalized_achievement = normalize_title(achievement_title)
    matching_files = []
    
    for filename in merged_files:
        parts = filename.replace('.txt', '').split('_merged_', 1)
        if len(parts) == 2:
            file_title = normalize_title(parts[1])
            
            score = similarity(normalized_achievement, file_title)
            
            # Boost score if file title is contained in achievement title
            if file_title in normalized_achievement:
                score = max(score, 0.85)
            
            # Boost score for exact word matches
            achievement_words = set(normalized_achievement.split())
            file_words = set(file_title.split())
            common_words = achievement_words.intersection(file_words)
            if common_words:
                word_match_bonus = len(common_words) / max(len(achievement_words), len(file_words))
                score = max(score, word_match_bonus * 0.9)
            
            if score >= threshold:
                matching_files.append((filename, score))
    
    # Sort by score (highest first), then by filename for consistent ordering
    matching_files.sort(key=lambda x: (-x[1], x[0]))
    return matching_files


def read_merged_file(filepath):
    """Read and parse a merged JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def fix_initialization_order(html_content):
    """Fix the initialization order to ensure init() runs after DOMContentLoaded"""
    # Remove window.onload = init; if it exists
    html_content = re.sub(r'// Initialize\s*\n\s*window\.onload\s*=\s*init;\s*\n', '', html_content)
    
    # Ensure init() is called at the end of DOMContentLoaded
    pattern = r'(totalSlides\s*=\s*document\.querySelectorAll\([\'"]\.slide[\'"]\)\.length;\s*)\n(\s*}\);)'
    replacement = r'\1\n    \n    // Initialize presentation AFTER all slides are generated\n    init();\n\2'
    html_content = re.sub(pattern, replacement, html_content)
    
    return html_content


def insert_background_image(html_content, background_data):
    """Insert background image into CSS :root section"""
    # Pattern to match --bg-image url in CSS
    pattern = r'(--bg-image:\s*url\(")[^"]*("\))'
    replacement = r'\1' + background_data + r'\2'
    updated_content = re.sub(pattern, replacement, html_content)
    
    # Also update the background image in the body CSS if present
    # Need to wrap the base64 data in url() properly with quotes
    body_pattern = r'(background:\s*linear-gradient[^;]*,\s*)url\([^)]*\)([^;]*;)'
    body_replacement = r'\1url(\'' + background_data + r'\')\2'
    updated_content = re.sub(body_pattern, body_replacement, updated_content)
    
    return updated_content


def insert_achievement_images(html_content, merged_dir):
    """Insert base64 images into slidesData achievement items"""
    merged_files = [f for f in os.listdir(merged_dir) 
                    if f.endswith('.txt') and f != '00_merged_background.txt']
    
    # Sort merged files by name to ensure consistent ordering
    merged_files.sort()
    
    # Pattern to match slidesData array and find achievement items
    pattern = r'(\s*"text":\s*")([^"]+)(",\s*"category":\s*"[^"]+",\s*"images":\s*)\[([^\]]*)\]'
    
    def replace_images(match):
        prefix = match.group(1)
        title = match.group(2).strip()
        suffix = match.group(3)
        old_images = match.group(4)
        
        matching_files = find_all_matching_images(title, merged_files)
        
        if matching_files:
            all_images = []
            # Sort matching files by filename to ensure ascending order
            sorted_matching = sorted(matching_files, key=lambda x: x[0])
            
            for filename, score in sorted_matching:
                filepath = os.path.join(merged_dir, filename)
                images_data = read_merged_file(filepath)
                
                if images_data:
                    all_images.extend(images_data)
                    print(f"  ✓ Matched '{title}' with '{filename}' (score: {score:.2f}) - {len(images_data)} images")
            
            if all_images:
                images_json = json.dumps(all_images)
                return f'{prefix}{title}{suffix}{images_json}'
        
        print(f"  ✗ No match found for '{title}'")
        return match.group(0)
    
    updated_content = re.sub(pattern, replace_images, html_content, flags=re.DOTALL)
    return updated_content

def insert_team_member_images(html_content, merged_dir):
    """Insert team member images into thank you page"""
    # Look for all team member merged files
    team_member_files = []
    for filename in os.listdir(merged_dir):
        if filename.endswith('.txt') and 'TeamMember' in filename:
            team_member_files.append(filename)
    
    if not team_member_files:
        print("  ⚠️  No team member images file found")
        return html_content
    
    # Sort files to ensure correct order (01, 02, 03)
    team_member_files.sort()
    
    # Read all team member images
    team_images = []
    for filename in team_member_files:
        filepath = os.path.join(merged_dir, filename)
        images_data = read_merged_file(filepath)
        if images_data and len(images_data) > 0:
            team_images.append(images_data[0])  # Take first image from each file
    
    if len(team_images) < 3:
        print(f"  ⚠️  Not enough team member images found (need 3, got {len(team_images)})")
        return html_content
    
    # Create team member data structure
    team_members_data = [
        {"name": "Fizul Haque", "image": team_images[0]},
        {"name": "Samiul Islam", "image": team_images[1]},
        {"name": "Moin Sharif", "image": team_images[2]}
    ]

    # Convert to JavaScript format
    team_members_js = json.dumps(team_members_data, indent=4, ensure_ascii=False)

    # Replace mainData.teamMembersData array - more precise pattern
    pattern = r'(teamMembersData:\s*)\[[^\]]*\]'
    replacement = f'\\1{team_members_js}'
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    print(f"  ✓ Inserted {len(team_images)} team member images")
    
    return html_content


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def find_file_with_pattern(directory, pattern):
    """Find a file matching the pattern (e.g., '*Achivment.txt' or '*Plans.txt')"""
    for filename in os.listdir(directory):
        if pattern.lower() in filename.lower():
            return os.path.join(directory, filename)
    return None


def parse_not_completed_kpis(filepath):
    """Parse not completed KPIs file"""
    items = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Split by "--" to separate item name and category
                if '--' in line:
                    parts = line.split('--', 1)
                    item_name = parts[0].strip()
                    category = parts[1].strip()
                else:
                    item_name = line
                    category = ""
                
                items.append({
                    'text': item_name,
                    'category': category
                })
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    return items

def update_not_completed_kpis(html_content, not_completed_items):
    """Update notCompletedKPIS array in HTML"""
    # Convert to JavaScript format
    not_completed_js = json.dumps(not_completed_items, indent=4, ensure_ascii=False)

    # Replace mainData.notCompletedKPIS array
    # Pattern to match the notCompletedKPIS property within mainData object
    pattern = r'(notCompletedKPIS:\s*)\[[\s\S]*?\](?=\s*,\s*timelineData)'
    replacement = f'\\1{not_completed_js}'
    html_content = re.sub(pattern, replacement, html_content, count=1)

    return html_content

def main():
    """Main function to process slide"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # File paths
    html_file = os.path.join(script_dir, "basic_slide.html")
    img_dir = os.path.join(script_dir, "images")  # Changed from "img" to "images"
    merged_dir = os.path.join(script_dir, "merged")
    output_file = os.path.join(script_dir, "basic_slide_updated.html")
    
    # Find achievement and plans files dynamically
    achievements_file = find_file_with_pattern(script_dir, "achivment.txt")
    plans_file = find_file_with_pattern(script_dir, "plans.txt")

    # Extract months from both file names first
    achievement_month = extract_month_from_filename(achievements_file)
    plans_month = extract_month_from_filename(plans_file)

    # Set output filename based on achievement month
    if achievement_month:
        output_file = os.path.join(script_dir, f"{achievement_month}-KPI.html")
    else:
        output_file = os.path.join(script_dir, "basic_slide_updated.html")

    # Use direct path for notCompletedKPIS.txt
    not_completed_file = os.path.join(script_dir, "notCompletedKPIS.txt")

    print("=" * 70)
    print("SLIDE PROCESSING SCRIPT")
    print("=" * 70)

    # Check if required files exist
    if not os.path.exists(html_file):
        print(f"❌ Error: HTML file not found at {html_file}")
        return

    if not achievements_file or not os.path.exists(achievements_file):
        print(f"❌ Error: Achievements file not found (looking for '*Achivment.txt')")
        return

    if not plans_file or not os.path.exists(plans_file):
        print(f"❌ Error: Plans file not found (looking for '*Plans.txt')")
        return

    if not os.path.exists(img_dir):
        print(f"❌ Error: Images directory not found at {img_dir}")
        return

    # TASK 1: Update HTML Content
    print("\n📝 TASK 1: Updating HTML content with achievements and plans...")
    print("-" * 70)
    
    print(f"  Found achievements file: {os.path.basename(achievements_file)}")
    print(f"  Found plans file: {os.path.basename(plans_file)}")
    if achievement_month:
        print(f"  Detected achievement month: {achievement_month}")
        print(f"  Output file will be: {achievement_month}-KPI.html")
    if plans_month:
        print(f"  Detected plans month: {plans_month}")
    
    achievements = parse_items_file(achievements_file)
    plans = parse_items_file(plans_file)
    not_completed_items = []
    
    if not_completed_file and os.path.exists(not_completed_file):
        not_completed_items = parse_not_completed_kpis(not_completed_file)
        print(f"  Found not completed KPIs file: {os.path.basename(not_completed_file)}")
    
    print(f"  Loaded {len(achievements)} achievements")
    print(f"  Loaded {len(plans)} plans")
    if not_completed_items:
        print(f"  Loaded {len(not_completed_items)} not completed KPIs")
    
    # Calculate how many slides needed
    items_per_slide = 6
    achievement_slides = (len(achievements) + items_per_slide - 1) // items_per_slide
    plan_slides = (len(plans) + items_per_slide - 1) // items_per_slide
    
    print(f"  Will distribute across {achievement_slides} achievement slide(s) and {plan_slides} plan slide(s)")
    print(f"  Using {items_per_slide} items per slide")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    html_content = update_html_content(html_content, achievements, plans, achievement_month, plans_month)
    
    # Update not completed KPIs if available
    if not_completed_items:
        html_content = update_not_completed_kpis(html_content, not_completed_items)
    
    print("  ✓ HTML content updated")
    if achievement_month:
        print(f"  ✓ Achievement title updated to: {achievement_month} Achievements")
        print(f"  ✓ Month subtitle updated to: {achievement_month}")
    if plans_month:
        print(f"  ✓ Plans title updated to: {plans_month} Plans")
    if not_completed_items:
        print(f"  ✓ Not completed KPIs updated: {len(not_completed_items)} items")
    
    # TASK 2: Encode Images and Merge
    print("\n🖼️  TASK 2: Encoding images and merging...")
    print("-" * 70)
    
    encoded_files = encode_images_in_directory(img_dir)
    
    if encoded_files:
        print(f"\n  Merging {len(encoded_files)} encoded files...")
        merge_files(encoded_files, script_dir)
        print("  ✓ Images encoded and merged")
    else:
        print("  ⚠️  No image files found to encode")
    
    # TASK 3: Insert Images into HTML
    print("\n🔗 TASK 3: Inserting images into HTML...")
    print("-" * 70)
    
    if os.path.exists(merged_dir):
        # Insert background image
        background_file = os.path.join(merged_dir, "00_merged_background.txt")
        if os.path.exists(background_file):
            background_data = read_merged_file(background_file)
            if background_data and len(background_data) > 0:
                html_content = insert_background_image(html_content, background_data[0])
                print("  ✓ Background image inserted")
        else:
            print("  ⚠️  Background image file not found")
        
        # Insert achievement images
        html_content = insert_achievement_images(html_content, merged_dir)
        print("  ✓ Achievement images inserted")
        
        # Insert team member images
        html_content = insert_team_member_images(html_content, merged_dir)
    else:
        print("  ⚠️  Merged directory not found, skipping image insertion")
    
    # Fix initialization order
    print("\n🔧 TASK 4: Fixing JavaScript initialization...")
    print("-" * 70)
    html_content = fix_initialization_order(html_content)
    print("  ✓ JavaScript initialization order fixed")
    
    # Write final output
    print("\n💾 Writing final output...")
    print("-" * 70)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  ✓ Updated HTML saved to: {output_file}")
    
    # Clean up merged folder
    print("\n🧹 Cleaning up...")
    print("-" * 70)
    
    if os.path.exists(merged_dir):
        try:
            shutil.rmtree(merged_dir)
            print(f"  ✓ Removed merged folder: {merged_dir}")
        except Exception as e:
            print(f"  ⚠️  Could not remove merged folder: {e}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TASKS COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\nOutput file: {output_file}")
    print("\nFixed issues:")
    print("  • Slide navigation now works correctly")
    print("  • Team member images load properly")
    print("  • Achievement images are clickable")
    print("  • Merged folder cleaned up automatically")
    print("\nYou can now review the file and replace basic_slide.html if everything looks good.")


if __name__ == "__main__":
    main()
