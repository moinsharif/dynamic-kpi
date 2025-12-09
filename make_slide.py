#!/usr/bin/env python3
"""
Comprehensive Slide Processing Script
Combines three tasks:
1. Update HTML content with achievements and plans from text files
2. Encode images to base64 and merge them
3. Insert encoded images into HTML
4. Apply custom configuration (theme colors, team members, etc.)
"""

import os
import json
import base64
import re
import shutil
from collections import defaultdict
from difflib import SequenceMatcher


# ============================================================================
# CONFIGURATION PARSER
# ============================================================================

# Predefined theme colors
THEMES = {
    1: {
        'name': 'Pink/Rose (Default)',
        'PRIMARY_COLOR': '#d5114a',
        'PRIMARY_LIGHT': '#ff6b8b',
        'PRIMARY_DARK': '#a00d38'
    },
    2: {
        'name': 'Blue Ocean',
        'PRIMARY_COLOR': '#1e40af',
        'PRIMARY_LIGHT': '#3b82f6',
        'PRIMARY_DARK': '#1e3a8a'
    },
    3: {
        'name': 'Green Forest',
        'PRIMARY_COLOR': '#15803d',
        'PRIMARY_LIGHT': '#22c55e',
        'PRIMARY_DARK': '#14532d'
    },
    4: {
        'name': 'Purple Dream',
        'PRIMARY_COLOR': '#7c3aed',
        'PRIMARY_LIGHT': '#a78bfa',
        'PRIMARY_DARK': '#5b21b6'
    },
    5: {
        'name': 'Orange Sunset',
        'PRIMARY_COLOR': '#ea580c',
        'PRIMARY_LIGHT': '#fb923c',
        'PRIMARY_DARK': '#c2410c'
    },
    6: {
        'name': 'Red Passion',
        'PRIMARY_COLOR': '#dc2626',
        'PRIMARY_LIGHT': '#ef4444',
        'PRIMARY_DARK': '#991b1b'
    },
    7: {
        'name': 'Teal Wave',
        'PRIMARY_COLOR': '#0d9488',
        'PRIMARY_LIGHT': '#14b8a6',
        'PRIMARY_DARK': '#115e59'
    },
    8: {
        'name': 'Indigo Night',
        'PRIMARY_COLOR': '#4f46e5',
        'PRIMARY_LIGHT': '#6366f1',
        'PRIMARY_DARK': '#3730a3'
    },
    9: {
        'name': 'Amber Gold',
        'PRIMARY_COLOR': '#d97706',
        'PRIMARY_LIGHT': '#f59e0b',
        'PRIMARY_DARK': '#92400e'
    },
    10: {
        'name': 'Emerald Luxury',
        'PRIMARY_COLOR': '#059669',
        'PRIMARY_LIGHT': '#10b981',
        'PRIMARY_DARK': '#065f46'
    }
}


def parse_config_file(filepath):
    """Parse configuration file and return config dictionary"""
    config = {
        'THEME': 1,
        'PRIMARY_COLOR': '#d5114a',
        'PRIMARY_LIGHT': '#ff6b8b',
        'PRIMARY_DARK': '#a00d38',
        'TEAM_NAME': 'LMS Team',
        'TEAM_FULL_NAME': 'LMS Development Team',
        'TEAM_MEMBERS': ['Fizul Haque', 'Samiul Islam', 'Moin Sharif'],
        'CONTACT_EMAIL': 'info@orbittechinc.com'
    }
    
    if not os.path.exists(filepath):
        print(f"  ⚠️  Config file not found: {filepath}")
        print(f"  ℹ️  Using default configuration")
        return config
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse key=value pairs
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Handle team members (comma-separated)
                    if key == 'TEAM_MEMBERS':
                        config[key] = [member.strip() for member in value.split(',')]
                    # Handle theme number
                    elif key == 'THEME':
                        try:
                            theme_num = int(value)
                            if 1 <= theme_num <= 10:
                                config['THEME'] = theme_num
                                # Apply theme colors
                                theme = THEMES[theme_num]
                                config['PRIMARY_COLOR'] = theme['PRIMARY_COLOR']
                                config['PRIMARY_LIGHT'] = theme['PRIMARY_LIGHT']
                                config['PRIMARY_DARK'] = theme['PRIMARY_DARK']
                                config['THEME_NAME'] = theme['name']
                            else:
                                print(f"  ⚠️  Invalid theme number: {theme_num}. Using default theme.")
                        except ValueError:
                            print(f"  ⚠️  Invalid theme value: {value}. Using default theme.")
                    else:
                        config[key] = value
        
        # If custom colors are specified, they override theme colors
        # This allows advanced users to use custom colors
        
        print(f"  ✓ Configuration loaded from {filepath}")
        if 'THEME_NAME' in config:
            print(f"  ✓ Theme: {config['THEME']} - {config['THEME_NAME']}")
        return config
    except Exception as e:
        print(f"  ⚠️  Error reading config file: {e}")
        print(f"  ℹ️  Using default configuration")
        # Apply default theme
        theme = THEMES[1]
        config['PRIMARY_COLOR'] = theme['PRIMARY_COLOR']
        config['PRIMARY_LIGHT'] = theme['PRIMARY_LIGHT']
        config['PRIMARY_DARK'] = theme['PRIMARY_DARK']
        config['THEME_NAME'] = theme['name']
        return config


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
    
    # Sort files alphabetically (natural sorting)
    all_image_files.sort()
    
    # Process files in sorted order
    for image_file in all_image_files:
        image_path = os.path.join(directory, image_file)
        name_without_ext = os.path.splitext(image_file)[0]
        
        encoded_data = encode_image_to_base64(image_path)
        if encoded_data:
            encoded_files.append((name_without_ext, encoded_data))
            print(f"  Encoded: {image_file}")
    
    return encoded_files


def extract_title_from_filename(filename):
    """Extract the title from filename (remove -01, -02 etc. suffix and extension)"""
    # Remove extension first
    name_without_ext = filename.replace('.txt', '')
    # Remove the -01, -02 etc. suffix
    parts = name_without_ext.rsplit('-', 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]
    return name_without_ext


def merge_files(encoded_files, directory):
    """Group files by title and merge their content into JSON arrays"""
    title_groups = defaultdict(list)
    
    for name_without_ext, encoded_data in encoded_files:
        title = extract_title_from_filename(name_without_ext + ".txt")
        title_groups[title].append(encoded_data)
    
    # Create merged folder
    merged_folder = os.path.join(directory, "merged")
    os.makedirs(merged_folder, exist_ok=True)
    
    # Create merged files
    for title, content_list in title_groups.items():
        if content_list:
            new_filename = f"{title}.txt"
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


def normalize_for_matching(text):
    """Normalize text for matching by converting special characters to underscores"""
    # Convert to lowercase
    text = text.lower()
    # Replace special characters that are not allowed in filenames with underscores
    # Windows/Linux disallowed: < > : " / \ | ? *
    # We'll also handle other punctuation
    text = text.replace('/', '_')
    text = text.replace('\\', '_')
    text = text.replace(':', '_')
    text = text.replace('*', '_')
    text = text.replace('?', '_')
    text = text.replace('"', '_')
    text = text.replace('<', '_')
    text = text.replace('>', '_')
    text = text.replace('|', '_')
    text = text.replace('(', '_')
    text = text.replace(')', '_')
    text = text.replace('[', '_')
    text = text.replace(']', '_')
    text = text.replace(',', '_')
    text = text.replace('.', '_')
    text = text.replace(';', '_')
    text = text.replace('!', '_')
    text = text.replace('@', '_')
    text = text.replace('#', '_')
    text = text.replace('$', '_')
    text = text.replace('%', '_')
    text = text.replace('^', '_')
    text = text.replace('&', '_')
    text = text.replace('+', '_')
    text = text.replace('=', '_')
    text = text.replace('{', '_')
    text = text.replace('}', '_')
    text = text.replace('`', '_')
    text = text.replace('~', '_')
    
    # Replace multiple underscores with single underscore
    text = re.sub(r'_+', '_', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing spaces and underscores
    text = text.strip(' _')
    
    return text


def suggest_filename(task_name):
    """Suggest correct filename for a task"""
    # Keep original case for display
    suggested = task_name
    # Replace special characters
    suggested = suggested.replace('/', '_')
    suggested = suggested.replace('\\', '_')
    suggested = suggested.replace(':', '_')
    suggested = suggested.replace('*', '_')
    suggested = suggested.replace('?', '_')
    suggested = suggested.replace('"', '_')
    suggested = suggested.replace('<', '_')
    suggested = suggested.replace('>', '_')
    suggested = suggested.replace('|', '_')
    suggested = suggested.replace(',', '_')
    
    # Clean up multiple underscores
    suggested = re.sub(r'_+', '_', suggested)
    suggested = suggested.strip(' _')
    
    return f"{suggested}-01.png"


def find_all_matching_images(achievement_title, merged_files, threshold=0.85):
    """Find all matching merged files for an achievement title"""
    # Normalize achievement title
    normalized_achievement = normalize_for_matching(achievement_title)
    matching_files = []

    for filename in merged_files:
        # Remove .txt extension
        file_title = filename.replace('.txt', '')
        
        # Normalize file title the same way
        normalized_file_title = normalize_for_matching(file_title)

        # Check for exact match
        if normalized_achievement == normalized_file_title:
            matching_files.append((filename, 1.0))
            continue

        # Check if file title starts with the achievement title
        if normalized_file_title.startswith(normalized_achievement):
            matching_files.append((filename, 0.95))
            continue

        # Check if achievement title starts with the file title
        if normalized_achievement.startswith(normalized_file_title):
            matching_files.append((filename, 0.95))
            continue

        # For close matches using similarity ratio
        score = similarity(normalized_achievement, normalized_file_title)
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
    body_pattern = r'(background:\s*linear-gradient[^;]*,\s*)url\([^)]*\)([^;]*;)'
    body_replacement = r'\1url(\'' + background_data + r'\')\2'
    updated_content = re.sub(body_pattern, body_replacement, updated_content)
    
    return updated_content


def apply_theme_colors(html_content, config):
    """Apply theme colors from config to HTML - comprehensive color replacement"""
    primary = config['PRIMARY_COLOR']
    light = config['PRIMARY_LIGHT']
    dark = config['PRIMARY_DARK']
    
    # 1. Replace CSS :root variables
    html_content = re.sub(
        r'(--primary-color:\s*)#[0-9a-fA-F]{6}',
        r'\1' + primary,
        html_content
    )
    html_content = re.sub(
        r'(--primary-light:\s*)#[0-9a-fA-F]{6}',
        r'\1' + light,
        html_content
    )
    html_content = re.sub(
        r'(--primary-dark:\s*)#[0-9a-fA-F]{6}',
        r'\1' + dark,
        html_content
    )
    
    # 2. Replace gradient definitions (--primary-gradient)
    html_content = re.sub(
        r'(--primary-gradient:\s*linear-gradient\(135deg,\s*)#[0-9a-fA-F]{6}(\s*0%,\s*)#[0-9a-fA-F]{6}(\s*100%\))',
        r'\1' + primary + r'\2' + light + r'\3',
        html_content
    )
    
    # 3. Replace secondary gradient
    html_content = re.sub(
        r'(--secondary-gradient:\s*linear-gradient\(135deg,\s*)#[0-9a-fA-F]{6}(\s*0%,\s*)#[0-9a-fA-F]{6}(\s*100%\))',
        r'\1' + light + r'\2' + primary + r'\3',
        html_content
    )
    
    # 4. Replace body background gradient (main background)
    # Pattern: linear-gradient(135deg, #d5114a 0%, #ff6b8b 50%, #ffb3c6 100%)
    html_content = re.sub(
        r'(background:\s*linear-gradient\(135deg,\s*)#[0-9a-fA-F]{6}(\s*0%,\s*)#[0-9a-fA-F]{6}(\s*50%,\s*)#[0-9a-fA-F]{6}(\s*100%\))',
        r'\1' + primary + r'\2' + light + r'\3' + light + r'\4',
        html_content
    )
    
    # 5. Replace inline gradient colors in body tag
    # This handles the main page background
    body_gradient_pattern = r'(body\s*{[^}]*background:\s*linear-gradient\([^)]+\))'
    def replace_body_gradient(match):
        text = match.group(0)
        # Replace all hex colors in this gradient
        text = re.sub(r'#d5114a', primary, text)
        text = re.sub(r'#ff6b8b', light, text)
        text = re.sub(r'#ffb3c6', light, text)
        text = re.sub(r'#a00d38', dark, text)
        return text
    html_content = re.sub(body_gradient_pattern, replace_body_gradient, html_content, flags=re.DOTALL)
    
    # 6. Replace rgba colors (for shadows and overlays)
    # Convert hex to RGB for rgba replacements
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    primary_rgb = hex_to_rgb(primary)
    
    # Replace rgba(213, 17, 74, ...) with new primary color
    html_content = re.sub(
        r'rgba\(213,\s*17,\s*74,',
        f'rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]},',
        html_content
    )
    
    # 7. Replace --primary-lighter variable (lighter shade)
    # Calculate a lighter shade (mix light with white)
    html_content = re.sub(
        r'(--primary-lighter:\s*)#[0-9a-fA-F]{6}',
        r'\1' + light,  # Use light color for lighter variant
        html_content
    )
    
    # 8. Replace accent gradient
    html_content = re.sub(
        r'(--accent-gradient:\s*linear-gradient\(135deg,\s*)#[0-9a-fA-F]{6}(\s*0%,\s*)#[0-9a-fA-F]{6}(\s*100%\))',
        r'\1' + light + r'\2' + light + r'\3',
        html_content
    )
    
    # 9. Replace thank-you-subtitle color
    html_content = re.sub(
        r'(\.thank-you-subtitle\s*{\s*color:\s*)#[0-9a-fA-F]{6}',
        r'\1' + primary,
        html_content
    )
    
    # 10. Replace thank-you-text gradient
    html_content = re.sub(
        r'(background-image:\s*linear-gradient\(135deg,\s*)#d5114a(\s*0%,\s*)#ff7ba5(\s*100%\))',
        r'\1' + primary + r'\2' + light + r'\3',
        html_content
    )
    
    # 11. Replace hover gradient for thank-you-text
    html_content = re.sub(
        r'(\.thank-you-text:hover[^}]*background-image:\s*linear-gradient\(135deg,\s*)#ff7ba5(\s*0%,\s*)#d5114a(\s*100%\))',
        r'\1' + light + r'\2' + primary + r'\3',
        html_content
    )
    
    # 12. Replace logo color in JavaScript
    html_content = re.sub(
        r"(const logoColor = slideIndex === totalSlides -1 \? ')#d5114a(' : 'white')",
        r"\1" + primary + r"\2",
        html_content
    )
    
    # 13. Replace all remaining hardcoded color references
    # This is a comprehensive replacement for any missed instances
    html_content = re.sub(r'#d5114a', primary, html_content)
    html_content = re.sub(r'#ff6b8b', light, html_content)
    html_content = re.sub(r'#a00d38', dark, html_content)
    html_content = re.sub(r'#ffb3c6', light, html_content)  # lighter variant
    html_content = re.sub(r'#ff7ba5', light, html_content)  # another light variant
    
    # 14. Replace rgba colors with different opacities
    # rgba(213, 17, 74, X) -> rgba(primary_rgb, X)
    html_content = re.sub(
        r'rgba\(213,\s*17,\s*74,\s*([0-9.]+)\)',
        f'rgba({primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]}, \\1)',
        html_content
    )
    
    # rgba(255, 107, 139, X) -> rgba(light_rgb, X)
    light_rgb = hex_to_rgb(light)
    html_content = re.sub(
        r'rgba\(255,\s*107,\s*139,\s*([0-9.]+)\)',
        f'rgba({light_rgb[0]}, {light_rgb[1]}, {light_rgb[2]}, \\1)',
        html_content
    )
    
    return html_content


def apply_team_info(html_content, config):
    """Apply team information from config to HTML"""
    team_members = config['TEAM_MEMBERS']
    
    # Create team members data structure for JavaScript
    team_members_data = [
        {"name": member, "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAwIDgwMCI+PHBhdGggZmlsbD0iI2M2ZmVmZiIgZD0iTTAgMEgxMjAwVjgwMEgwWiIvPjwvc3ZnPg=="}
        for member in team_members
    ]
    
    # Replace team name in title
    html_content = re.sub(
        r'(<title>)[^<]*(Monthly KPI[^<]*</title>)',
        r'\1' + config['TEAM_NAME'] + r' \2',
        html_content
    )
    
    # Replace team name in cover slide
    html_content = re.sub(
        r'(<h3 class="section-title">For the )[^<]*(</h3>)',
        r'\1' + config['TEAM_NAME'] + r'\2',
        html_content
    )
    
    # Replace contact email
    html_content = re.sub(
        r'(Questions\? Contact us at )[^\s<]+',
        r'\1' + config['CONTACT_EMAIL'],
        html_content
    )
    
    # Replace team full name in contact section
    html_content = re.sub(
        r'(<p>)[^<]*(Team</p>)',
        r'\1' + config['TEAM_FULL_NAME'] + r'\2',
        html_content
    )
    
    return html_content


def insert_achievement_images(html_content, merged_dir):
    """Insert base64 images into slidesData achievement items"""
    merged_files = [f for f in os.listdir(merged_dir) 
                    if f.endswith('.txt') and f != 'background.txt']
    
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
        
        suggested = suggest_filename(title)
        print(f"  ✗ No match found for '{title}'")
        print(f"     Suggested filename: {suggested}")
        return match.group(0)
    
    updated_content = re.sub(pattern, replace_images, html_content, flags=re.DOTALL)
    return updated_content

def insert_team_member_images(html_content, merged_dir, config):
    """Insert team member images into thank you page"""
    team_members = config['TEAM_MEMBERS']
    
    # Look for team member merged files (TeamMember_01, TeamMember_02, TeamMember_03)
    team_member_files = []
    for filename in os.listdir(merged_dir):
        if filename.endswith('.txt') and 'teammember' in filename.lower():
            team_member_files.append(filename)
    
    # Sort files to ensure correct order
    team_member_files.sort()
    
    # Read all team member images
    team_images = []
    for filename in team_member_files:
        filepath = os.path.join(merged_dir, filename)
        images_data = read_merged_file(filepath)
        if images_data and len(images_data) > 0:
            team_images.append(images_data[0])  # Take first image from each file
    
    # Create team member data structure
    team_members_data = []
    for i, member_name in enumerate(team_members):
        if i < len(team_images):
            # Use actual image if available
            team_members_data.append({"name": member_name, "image": team_images[i]})
        else:
            # Use placeholder if no image available
            placeholder = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAwIDgwMCI+PHBhdGggZmlsbD0iI2M2ZmVmZiIgZD0iTTAgMEgxMjAwVjgwMEgwWiIvPjwvc3ZnPg=="
            team_members_data.append({"name": member_name, "image": placeholder})
    
    if not team_members_data:
        print("  ⚠️  No team members configured")
        return html_content

    # Convert to JavaScript format
    team_members_js = json.dumps(team_members_data, indent=4, ensure_ascii=False)

    # Replace mainData.teamMembersData array
    pattern = r'(teamMembersData:\s*)\[[^\]]*\]'
    replacement = f'\\1{team_members_js}'
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    print(f"  ✓ Inserted {len(team_members_data)} team member(s): {', '.join(team_members)}")
    
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
    img_dir = os.path.join(script_dir, "images")
    merged_dir = os.path.join(script_dir, "merged")
    config_file = os.path.join(script_dir, "config.txt")
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
    
    # Load configuration
    print("\n📋 LOADING CONFIGURATION...")
    print("-" * 70)
    config = parse_config_file(config_file)
    print(f"  Theme Color: {config['PRIMARY_COLOR']}")
    print(f"  Team Name: {config['TEAM_NAME']}")
    print(f"  Team Members: {', '.join(config['TEAM_MEMBERS'])}")
    print(f"  Contact Email: {config['CONTACT_EMAIL']}")

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
    
    # Apply configuration
    print("\n🎨 APPLYING CONFIGURATION...")
    print("-" * 70)
    html_content = apply_theme_colors(html_content, config)
    print(f"  ✓ Theme colors applied to:")
    print(f"    • CSS variables (:root)")
    print(f"    • Background gradients")
    print(f"    • Button and card colors")
    print(f"    • Shadows and overlays")
    print(f"    • Logo colors")
    print(f"    • All UI elements")
    
    html_content = apply_team_info(html_content, config)
    print(f"  ✓ Team information applied")
    
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
        background_file = os.path.join(merged_dir, "background.txt")
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
        html_content = insert_team_member_images(html_content, merged_dir, config)
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
    print("\n" + "=" * 70)
    print("📝 IMPORTANT: Image File Naming Rules")
    print("=" * 70)
    print("\nImage files MUST match task names exactly!")
    print("\nExample:")
    print("  Task: 'Survey feedback'")
    print("  File: 'Survey feedback-01.png' ✅")
    print("\nSpecial characters must be replaced with underscore (_):")
    print("  Task: 'Learner/Trainer location'")
    print("  File: 'Learner_Trainer location-01.png' ✅")
    print("\nCommon replacements:")
    print("  / → _  (slash)")
    print("  , → _  (comma)")
    print("  : → _  (colon)")
    print("  * → _  (asterisk)")
    print("  ? → _  (question mark)")
    print("\nCheck console output above for '✗ No match found' messages.")
    print("\nYou can now review the file and replace basic_slide.html if everything looks good.")


if __name__ == "__main__":
    main()
