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


def generate_achievement_html(items, max_items=6):
    """Generate HTML for achievement items"""
    html_parts = []
    
    for item in items[:max_items]:
        category_html = f'<span class="item-category">{item["category"]}</span>' if item['category'] else ''
        
        html = f'''                    <div class="achievement-item" data-images='[]'>
                        <p>{item["name"]}</p>
                        {category_html}
                    </div>'''
        html_parts.append(html)
    
    return '\n'.join(html_parts)


def generate_plan_html(items, max_items=6):
    """Generate HTML for plan items"""
    html_parts = []
    
    for item in items[:max_items]:
        category_html = f'<span class="item-category">{item["category"]}</span>' if item['category'] else ''
        
        html = f'''                    <div class="plan-item">
                        <p>{item["name"]}</p>
                        {category_html}
                    </div>'''
        html_parts.append(html)
    
    return '\n'.join(html_parts)


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
    """Update HTML with achievements, plans, and month titles"""
    # Update month subtitle (first occurrence - under Monthly KPI)
    if achievement_month:
        subtitle_pattern = r'(<h2 class="slide-subtitle">)[^<]*(</h2>)'
        subtitle_replacement = r'\1' + achievement_month + r'\2'
        html_content = re.sub(subtitle_pattern, subtitle_replacement, html_content, count=1)
    
    # Update ALL achievement titles (skip Monthly KPI, update all "Achievements" titles)
    if achievement_month:
        def replace_achievement_title(match):
            full_match = match.group(0)
            title_content = match.group(2)
            
            if "Monthly KPI" in title_content or "Team Members" in title_content or "Project Timeline" in title_content:
                return full_match
            
            if "Achievements" in title_content:
                return match.group(1) + achievement_month + ' Achievements' + match.group(3)
            
            return full_match
        
        achievement_title_pattern = r'(<h1 class="slide-title">)([^<]*)(</h1>)'
        html_content = re.sub(achievement_title_pattern, replace_achievement_title, html_content)
    
    # Update ALL plans titles
    if plans_month:
        def replace_plans_title(match):
            full_match = match.group(0)
            title_content = match.group(2)
            
            if "Plans" in title_content and "Project Timeline" not in title_content:
                return match.group(1) + plans_month + ' Plans' + match.group(3)
            
            return full_match
        
        plans_title_pattern = r'(<h1 class="slide-title">)([^<]*)(</h1>)'
        html_content = re.sub(plans_title_pattern, replace_plans_title, html_content)
    
    # Calculate how many slides we need
    items_per_slide = 6
    achievement_slides_needed = (len(achievements) + items_per_slide - 1) // items_per_slide
    plan_slides_needed = (len(plans) + items_per_slide - 1) // items_per_slide
    
    # Pattern to match a complete slide block (comment + div)
    # Matches from <!-- Slide X: --> to the closing </div> before next comment
    slide_block_pattern = r'(\s*<!-- Slide \d+: [^>]+ -->\s*<div class="slide"[^>]*>.*?</div>)\s*(?=\n\s*(?:<!-- Slide \d+:|</div>\s*</body>))'
    
    # Find all slide blocks
    slide_blocks = []
    for match in re.finditer(slide_block_pattern, html_content, flags=re.DOTALL):
        slide_text = match.group(1)
        slide_blocks.append({
            'text': slide_text,
            'start': match.start(),
            'end': match.end(),
            'is_achievement': 'Achievements' in slide_text and 'achievement-list' in slide_text,
            'is_plan': 'Plans' in slide_text and 'plan-list' in slide_text
        })
    
    # Update content and mark slides to keep/remove
    achievement_index = 0
    plan_index = 0
    achievement_count = 0
    plan_count = 0
    
    slides_to_remove = []
    
    for i, slide in enumerate(slide_blocks):
        if slide['is_achievement']:
            if achievement_count < achievement_slides_needed:
                # Update this achievement slide
                start_idx = achievement_index
                end_idx = min(achievement_index + items_per_slide, len(achievements))
                achievement_index = end_idx
                
                slide_achievements = achievements[start_idx:end_idx]
                achievements_html = generate_achievement_html(slide_achievements, max_items=items_per_slide)
                
                # Replace the achievement-list content
                updated_text = re.sub(
                    r'(<div class="achievement-list">)(.*?)(</div>)(\s*</div>\s*</div>)',
                    r'\1\n' + achievements_html + r'\n                \3\4',
                    slide['text'],
                    flags=re.DOTALL
                )
                slide['text'] = updated_text
                achievement_count += 1
            else:
                # Mark for removal
                slides_to_remove.append(i)
        
        elif slide['is_plan']:
            if plan_count < plan_slides_needed:
                # Update this plan slide
                start_idx = plan_index
                end_idx = min(plan_index + items_per_slide, len(plans))
                plan_index = end_idx
                
                slide_plans = plans[start_idx:end_idx]
                plans_html = generate_plan_html(slide_plans, max_items=items_per_slide)
                
                # Replace the plan-list content
                updated_text = re.sub(
                    r'(<div class="plan-list">)(.*?)(</div>)(\s*</div>\s*</div>)',
                    r'\1\n' + plans_html + r'\n                \3\4',
                    slide['text'],
                    flags=re.DOTALL
                )
                slide['text'] = updated_text
                plan_count += 1
            else:
                # Mark for removal
                slides_to_remove.append(i)
    
    # Rebuild HTML by replacing slides in reverse order (to maintain positions)
    for i in reversed(range(len(slide_blocks))):
        slide = slide_blocks[i]
        if i in slides_to_remove:
            # Remove this slide
            html_content = html_content[:slide['start']] + html_content[slide['end']:]
        else:
            # Replace with updated content
            html_content = html_content[:slide['start']] + slide['text'] + html_content[slide['end']:]
    
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
    title = re.sub(r'[_\(\)/]', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title.lower()


def find_best_match(achievement_title, merged_files, threshold=0.7):
    """Find the best matching merged file for an achievement title"""
    normalized_achievement = normalize_title(achievement_title)
    
    best_match = None
    best_score = 0
    
    for filename in merged_files:
        parts = filename.replace('.txt', '').split('_merged_', 1)
        if len(parts) == 2:
            file_title = normalize_title(parts[1])
            
            score = similarity(normalized_achievement, file_title)
            
            if file_title in normalized_achievement:
                score = max(score, 0.85)
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = filename
    
    return best_match, best_score


def read_merged_file(filepath):
    """Read and parse a merged JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def insert_background_image(html_content, background_data):
    """Insert background image into CSS :root section"""
    pattern = r'(--bg-image:\s*url\(")[^"]*("\))'
    replacement = r'\1' + background_data + r'\2'
    updated_content = re.sub(pattern, replacement, html_content)
    return updated_content


def insert_achievement_images(html_content, merged_dir):
    """Insert base64 images into achievement items"""
    merged_files = [f for f in os.listdir(merged_dir) 
                    if f.endswith('.txt') and f != '00_merged_background.txt']
    
    pattern = r'(<div class="achievement-item" data-images=\')([^\']*)(\'>)\s*<p>([^<]+)</p>'
    
    def replace_images(match):
        prefix = match.group(1)
        old_images = match.group(2)
        suffix = match.group(3)
        title = match.group(4).strip()
        
        best_match, score = find_best_match(title, merged_files)
        
        if best_match:
            filepath = os.path.join(merged_dir, best_match)
            images_data = read_merged_file(filepath)
            
            if images_data:
                images_json = json.dumps(images_data)
                print(f"  ✓ Matched '{title}' with '{best_match}' (score: {score:.2f}) - {len(images_data)} images")
                return f"{prefix}{images_json}{suffix}\n                        <p>{title}</p>"
        
        print(f"  ✗ No match found for '{title}'")
        return match.group(0)
    
    updated_content = re.sub(pattern, replace_images, html_content, flags=re.DOTALL)
    return updated_content


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def find_file_with_pattern(directory, pattern):
    """Find a file matching the pattern (e.g., '*Achivment.txt' or '*Plans.txt')"""
    for filename in os.listdir(directory):
        if pattern.lower() in filename.lower():
            return os.path.join(directory, filename)
    return None


def main():
    """Main function to process slide"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # File paths
    html_file = os.path.join(script_dir, "basic_slide.html")
    img_dir = os.path.join(script_dir, "img")
    merged_dir = os.path.join(script_dir, "merged")
    output_file = os.path.join(script_dir, "basic_slide_updated.html")
    
    # Find achievement and plans files dynamically
    achievements_file = find_file_with_pattern(script_dir, "achivment.txt")
    plans_file = find_file_with_pattern(script_dir, "plans.txt")
    
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
    
    # Extract months from both file names
    achievement_month = extract_month_from_filename(achievements_file)
    plans_month = extract_month_from_filename(plans_file)
    
    print(f"  Found achievements file: {os.path.basename(achievements_file)}")
    print(f"  Found plans file: {os.path.basename(plans_file)}")
    if achievement_month:
        print(f"  Detected achievement month: {achievement_month}")
    if plans_month:
        print(f"  Detected plans month: {plans_month}")
    
    achievements = parse_items_file(achievements_file)
    plans = parse_items_file(plans_file)
    
    print(f"  Loaded {len(achievements)} achievements")
    print(f"  Loaded {len(plans)} plans")
    
    # Calculate how many slides needed
    items_per_slide = 6
    achievement_slides = (len(achievements) + items_per_slide - 1) // items_per_slide
    plan_slides = (len(plans) + items_per_slide - 1) // items_per_slide
    
    print(f"  Will distribute across {achievement_slides} achievement slide(s) and {plan_slides} plan slide(s)")
    print(f"  Using {items_per_slide} items per slide")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    html_content = update_html_content(html_content, achievements, plans, achievement_month, plans_month)
    print("  ✓ HTML content updated")
    if achievement_month:
        print(f"  ✓ Achievement title updated to: {achievement_month} Achievements")
        print(f"  ✓ Month subtitle updated to: {achievement_month}")
    if plans_month:
        print(f"  ✓ Plans title updated to: {plans_month} Plans")
    
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
    else:
        print("  ⚠️  Merged directory not found, skipping image insertion")
    
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
    print("You can now review the file and replace basic_slide.html if everything looks good.")


if __name__ == "__main__":
    main()
