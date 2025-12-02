#!/usr/bin/env python3

import re
import json

def parse_file_to_items(filename, delimiter='--'):
    """Parse a text file into list of items with text and category"""
    items = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and delimiter in line:
                    parts = line.rsplit(delimiter, 1)
                    text = parts[0].strip()
                    category = parts[1].strip()
                    items.append({
                        "text": text,
                        "category": category
                    })
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
    return items

def generate_timeline_from_files(november_achievements, december_plans):
    """Generate timeline data from November achievements and December plans"""
    timeline_items = []

    # Create a more realistic timeline based on the actual work
    # Group items by subcategory or time period if possible
    if november_achievements:
        # Add a general entry for November achievements
        timeline_items.append({
            "date": "Nov 1-15",
            "content": f"Early Nov: Started work on LMS improvements ({len([a for a in november_achievements if 'LMS' in a['category']])} tasks)"
        })
        timeline_items.append({
            "date": "Nov 16-30",
            "content": f"Late Nov: Completed {len(november_achievements)} achievements"
        })

    if december_plans:
        # Add a general entry for December plans
        timeline_items.append({
            "date": "Dec 1-15",
            "content": f"Early Dec: Planning phase for {len(december_plans)} tasks"
        })
        timeline_items.append({
            "date": "Dec 16-31",
            "content": f"Late Dec: Implementation of critical features"
        })

    # Also add a couple of specific important items if available
    if november_achievements:
        # Add first achievement as a specific milestone
        first_achievement = november_achievements[0]
        timeline_items.append({
            "date": "Nov",
            "content": f"Completed: {first_achievement['text'][:40]}{'...' if len(first_achievement['text']) > 40 else ''}"
        })

    if december_plans:
        # Add first plan as a future milestone
        first_plan = december_plans[0]
        timeline_items.append({
            "date": "Dec",
            "content": f"Planning: {first_plan['text'][:40]}{'...' if len(first_plan['text']) > 40 else ''}"
        })

    return timeline_items

def parse_timeline_file(filename):
    """Parse timeline file into list of timeline items with date and content"""
    items = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '--' in line:
                    parts = line.split('--', 1)
                    date = parts[0].strip()
                    content = parts[1].strip()
                    items.append({
                        "date": date,
                        "content": content
                    })
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
        # If timelineData.txt is not found, auto-generate from achievements and plans
        return []
    return items

def update_timeline_data(content, timeline_data):
    """Update timelineData in HTML"""
    if not timeline_data:
        return content

    # Convert to JavaScript format
    timeline_js = json.dumps(timeline_data, indent=4, ensure_ascii=False)

    # Replace mainData.timelineData
    timeline_pattern = r'(\s*timelineData:\s*\[).*?(\]\s*\],)'
    new_timeline = f'\\1{timeline_js}\\2'
    content = re.sub(timeline_pattern, new_timeline, content, flags=re.DOTALL)

    return content

def parse_team_member_file(filename):
    """Parse team member file into list of members with name and image"""
    items = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '--' in line:
                    parts = line.split('--', 1)
                    name = parts[0].strip()
                    image = parts[1].strip()
                    items.append({
                        "name": name,
                        "image": image  # This should be a base64 encoded string
                    })
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
    return items

def update_team_member_data(content, team_members_data):
    """Update teamMembersData in HTML"""
    if not team_members_data:
        return content

    # Convert to JavaScript format
    team_members_js = json.dumps(team_members_data, indent=4, ensure_ascii=False)

    # Replace mainData.teamMembersData
    team_members_pattern = r'(\s*teamMembersData:\s*\[).*?(\]\s*\]\s*\}\s*;)'
    new_team_members = f'\\1{team_members_js}\\2'
    content = re.sub(team_members_pattern, new_team_members, content, flags=re.DOTALL)

    return content

def create_slides_data(november_achievements, december_plans):
    """Create slidesData structure from parsed items with achievement images"""

    # Default placeholder images
    placeholder_images = [
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAwIDgwMCI+PHBhdGggZmlsbD0iI2M2ZmVmZiIgZD0iTTAgMEgxMjAwVjgwMEgwWiIvPjwvc3ZnPg==",
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAwIDgwMCI+PHBhdGggZmlsbD0iI2M2ZmVmZiIgZD0iTTAgMEgxMjAwVjgwMEgwWiIvPjwvc3ZnPg==",
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAwIDgwMCI+PHBhdGggZmlsbD0iI2M2ZmVmZiIgZD0iTTAgMEgxMjAwVjgwMEgwWiIvPjwvc3ZnPg=="
    ]

    # Add images to achievement items
    for item in november_achievements:
        item["images"] = placeholder_images.copy()

    # Create the slides data structure
    slides_data = [
        {
            "title": "November Achievements",
            "subtitle": "Key accomplishments this month",
            "data": november_achievements,
            "listClass": "achievement-list",
            "itemsPerSlide": 6,
        },
        {
            "title": "December Plans",
            "subtitle": "Upcoming tasks and objectives",
            "data": december_plans,
            "listClass": "plan-list",
            "itemsPerSlide": 6,
        }
    ]

    return slides_data

def update_html_file(html_file, slides_data, not_completed_kpis, timeline_data, team_member_data, achievement_month="November"):
    """Update the HTML file with new slidesData, notCompletedKPIS, timelineData, and teamMemberData"""

    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert data to JavaScript format
    slides_js = json.dumps(slides_data, indent=2, ensure_ascii=False)  # Use indent=2 for more compact format
    not_completed_js = json.dumps(not_completed_kpis, indent=2, ensure_ascii=False)
    timeline_js = json.dumps(timeline_data, indent=2, ensure_ascii=False)

    # Debug: Print the generated JSON to ensure it's correct
    print(f"Generated slides data JSON length: {len(slides_js)}")
    print(f"Generated not completed JSON length: {len(not_completed_js)}")
    print(f"Generated timeline JSON length: {len(timeline_js)}")

    # Replace mainData.slidesData - use a more specific pattern that captures the full structure
    # Find the slidesData section and replace it
    start_marker = 'slidesData: ['
    # Find the beginning of slidesData
    start_pos = content.find(start_marker)
    if start_pos != -1:
        # Find the start of notCompletedKPIS to determine the end of slidesData
        not_completed_start = content.find('notCompletedKPIS: [', start_pos)
        if not_completed_start != -1:
            # Find the opening bracket for slidesData content (the one after the colon)
            bracket_start = start_pos + len('slidesData: ')
            # Find the matching closing bracket for slidesData by counting brackets
            bracket_count = 0
            pos = bracket_start
            while pos < len(content) and pos < not_completed_start:  # Don't go beyond notCompletedKPIS
                if content[pos] == '[':
                    bracket_count += 1
                elif content[pos] == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        break
                pos += 1

            if bracket_count == 0:  # Make sure we found the right closing bracket
                # Replace content between the opening bracket at bracket_start and the closing bracket at pos
                old_content = content[bracket_start:pos+1]
                new_content = slides_js  # Don't add brackets, the JSON has them already
                content = content[:bracket_start] + new_content + content[pos+1:]

    # Replace mainData.notCompletedKPIS
    start_marker_n = 'notCompletedKPIS: ['

    start_pos_n = content.find(start_marker_n)
    if start_pos_n != -1:
        # Find the start of timelineData to determine the end of notCompletedKPIS
        timeline_start = content.find('timelineData: [', start_pos_n)
        if timeline_start != -1:
            bracket_start_n = start_pos_n + len('notCompletedKPIS: ')
            bracket_count_n = 0
            pos_n = bracket_start_n
            while pos_n < len(content) and pos_n < timeline_start:  # Don't go beyond timelineData
                if content[pos_n] == '[':
                    bracket_count_n += 1
                elif content[pos_n] == ']':
                    bracket_count_n -= 1
                    if bracket_count_n == 0:
                        break
                pos_n += 1

            if bracket_count_n == 0:
                old_content_n = content[bracket_start_n:pos_n+1]
                new_content_n = not_completed_js  # Don't add brackets, the JSON has them already
                content = content[:bracket_start_n] + new_content_n + content[pos_n+1:]

    # Replace mainData.timelineData
    start_marker_t = 'timelineData: ['

    start_pos_t = content.find(start_marker_t)
    if start_pos_t != -1:
        # Find the start of teamMembersData to determine the end of timelineData
        team_start = content.find('teamMembersData: [', start_pos_t)
        if team_start != -1:
            bracket_start_t = start_pos_t + len('timelineData: ')
            bracket_count_t = 0
            pos_t = bracket_start_t
            while pos_t < len(content) and pos_t < team_start:  # Don't go beyond teamMembersData
                if content[pos_t] == '[':
                    bracket_count_t += 1
                elif content[pos_t] == ']':
                    bracket_count_t -= 1
                    if bracket_count_t == 0:
                        break
                pos_t += 1

            if bracket_count_t == 0:
                old_content_t = content[bracket_start_t:pos_t+1]
                new_content_t = timeline_js  # Don't add brackets, the JSON has them already
                content = content[:bracket_start_t] + new_content_t + content[pos_t+1:]

    # Update teamMembersData if provided (using existing function)
    content = update_team_member_data(content, team_member_data)

    # Update title and subtitle dynamically based on achievement month
    kpi_title = f'LMS Team Monthly KPI - {achievement_month}'
    content = re.sub(r'LMS Team Monthly KPI - [A-Za-z]+(/[A-Za-z]+)?', kpi_title, content)
    content = re.sub(r'<title>LMS Team Monthly KPI - [A-Za-z]+(/[A-Za-z]+)?</title>', f'<title>{kpi_title}</title>', content)
    content = re.sub(r'<h2 class="slide-subtitle">[^<]*</h2>', f'<h2 class="slide-subtitle">{achievement_month}/December</h2>', content)
    
    # Also update the main title in the cover slide - more specific pattern
    content = re.sub(r'<h1 class="slide-title">[^<]*Monthly KPI</h1>', f'<h1 class="slide-title">{achievement_month} Monthly KPI</h1>', content)
    
    # Also update the subtitle in the cover slide (line 905) - more specific pattern
    content = re.sub(r'<h2 class="slide-subtitle">[^<]*</h2>', f'<h2 class="slide-subtitle">{achievement_month}</h2>', content)

    # Update stats in team members slide dynamically
    # First achievement stat
    content = re.sub(r'<div class="stat-number">22</div>', f'<div class="stat-number">{len(slides_data[0]["data"])}</div>', content)
    content = re.sub(r'<div class="stat-label">[^<]*Achievements</div>', f'<div class="stat-label">{achievement_month} Achievements</div>', content)
    # Second plans stat
    content = re.sub(r'<div class="stat-number">15</div>', f'<div class="stat-number">{len(slides_data[1]["data"])}</div>', content)
    content = re.sub(r'<div class="stat-label">[^<]*Plans</div>', '<div class="stat-label">December Plans</div>', content)

    # Write the updated content back to the file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {html_file} successfully!")

def extract_month_from_filename(filename):
    """Extract month name from achievement filename"""
    import os
    basename = os.path.basename(filename)
    # Remove extension and extract month (assuming format like "November Achivment.txt")
    parts = basename.replace('.txt', '').split()
    for part in parts:
        # Check if part is a month name
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                 'July', 'August', 'September', 'October', 'November', 'December']
        if part in months:
            return part
    return "November"  # default

def main():
    # Parse input files
    achievement_filename = 'November Achivment.txt'
    november_achievements = parse_file_to_items(achievement_filename)
    december_plans = parse_file_to_items('December Plans.txt')
    not_completed_kpis = parse_file_to_items('notCompletedKPIS.txt')
    
    # Extract month name from achievement file
    achievement_month = extract_month_from_filename(achievement_filename)

    # Try to parse timelineData.txt, but auto-generate if not found
    timeline_data = parse_timeline_file('timelineData.txt')

    # If no timeline data was found in the file, auto-generate from achievements and plans
    if not timeline_data:
        timeline_data = generate_timeline_from_files(november_achievements, december_plans)
        print(f"Auto-generated {len(timeline_data)} timeline entries from achievements and plans")
    else:
        print(f"Loaded {len(timeline_data)} timeline entries from timelineData.txt")

    team_member_data = parse_team_member_file('teamMembers.txt')  # Optional team member file

    print(f"Parsed {len(november_achievements)} November achievements")
    print(f"Parsed {len(december_plans)} December plans")
    print(f"Parsed {len(not_completed_kpis)} not completed KPIs")
    print(f"Total timeline entries: {len(timeline_data)}")
    print(f"Parsed {len(team_member_data)} team members")

    # Create slides data
    slides_data = create_slides_data(november_achievements, december_plans)

    # Update HTML file
    update_html_file('basic_slide.html', slides_data, not_completed_kpis, timeline_data, team_member_data, achievement_month)

    print("HTML file updated successfully!")

if __name__ == "__main__":
    main()