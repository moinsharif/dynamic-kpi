# Target: Dynamic Slide Content Update System

## Problem Statement

The `process_slide.py` script was not dynamically updating the HTML content from text files. The achievement-list and plan-list sections in `slide_17.html` were not being replaced with content from:
- `October Achivment.txt` (achievements)
- `November Plans.txt` (plans)

The script could not find and replace the content within the nested div structure of the HTML file.

## Requirements

1. **Dynamic Content Replacement**
   - Read achievement items from `*Achivment.txt` files
   - Read plan items from `*Plans.txt` files
   - Replace ALL `<div class="achievement-list">` sections with new content
   - Replace ALL `<div class="plan-list">` sections with new content

2. **Month Detection**
   - Extract month names from filenames (e.g., "October" from "October Achivment.txt")
   - Update slide titles dynamically (e.g., "October Achievements", "November Plans")
   - Update subtitle with achievement month

3. **Content Distribution**
   - Distribute items across multiple slides (6 items per slide)
   - Calculate required number of slides automatically
   - Maintain proper HTML structure and indentation

4. **Image Integration**
   - Encode images to base64
   - Match images to achievement/plan items
   - Insert image data into `data-images` attributes

## Solution Implemented

### Key Changes to `update_html_content()` Function

1. **Fixed Regex Pattern for Achievement Lists**
   ```python
   achievement_list_pattern = r'(<div class="achievement-list">)(.*?)(</div>)(\s*</div>\s*</div>)'
   ```
   - Captures opening tag
   - Captures content (with DOTALL flag for multi-line)
   - Captures closing `</div>` for achievement-list
   - Captures nested closing divs for content-section and slide

2. **Fixed Regex Pattern for Plan Lists**
   ```python
   plans_list_pattern = r'(<div class="plan-list">)(.*?)(</div>)(\s*</div>\s*</div>)'
   ```
   - Same structure as achievement pattern
   - Handles plan-list sections separately

3. **Content Replacement Logic**
   ```python
   def replace_achievement_list(match):
       nonlocal achievement_index
       start_idx = achievement_index
       end_idx = min(achievement_index + items_per_slide, len(achievements))
       achievement_index = end_idx
       
       slide_achievements = achievements[start_idx:end_idx]
       achievements_html = generate_achievement_html(slide_achievements, max_items=items_per_slide)
       
       return match.group(1) + '\n' + achievements_html + '\n                ' + match.group(3) + match.group(4)
   ```
   - Tracks current position in items list
   - Slices items for current slide (6 items max)
   - Generates HTML for items
   - Preserves proper closing tags

4. **Section Splitting**
   ```python
   parts = html_content.split('<!-- Future Plans -->', 1)
   achievements_section = parts[0]
   plans_section = parts[1]
   ```
   - Separates achievements from plans using HTML comment marker
   - Processes each section independently
   - Recombines after replacement

## HTML Structure Understanding

The script now correctly handles this nested structure:

```html
<div class="slide">
    <div class="slide-header">...</div>
    <div class="content-section">
        <div class="achievement-list">
            <!-- Items go here -->
        </div>  <!-- closes achievement-list -->
    </div>  <!-- closes content-section -->
</div>  <!-- closes slide -->
```

## Testing Results

✅ **Script Execution Successful**
- Loaded 10 achievements from "October Achivment.txt"
- Loaded 7 plans from "November Plans.txt"
- Total: 17 items to process
- Distributed across 2 achievement slides and 2 plan slides (6 items per slide)
- Updated titles: "October Achievements" and "November Plans"
- Encoded images from `img/` directory
- Matched images to items with 70%+ similarity threshold
- Successfully matched images for items found in the lists
- Generated `slide_17_updated.html` successfully

**Dynamic Behavior:**
- Script automatically detects month names from filenames
- Calculates required number of slides based on item count
- Only processes images that match items in the text files (≥70% similarity)
- Adapts to any number of achievements and plans

## Usage

1. **Update Content Files**
   - Edit `October Achivment.txt` or `November Plans.txt`
   - Format: `Item name -- Category`

2. **Add Images**
   - Place images in `img/` folder
   - Name format: `NN_MM_Item name.ext`
   - NN = item number, MM = sub-image number

3. **Run Script**
   ```bash
   python3 process_slide.py
   ```

4. **Review Output**
   - Check `slide_17_updated.html`
   - Verify content and images
   - Replace `slide_17.html` if satisfied

## File Structure

```
slide_final/
├── process_slide.py          # Main processing script
├── slide_17.html             # Original HTML template
├── slide_17_updated.html     # Generated output
├── October Achivment.txt     # Achievement items
├── November Plans.txt        # Plan items
└── img/                      # Image files
    ├── 00_01_background.svg
    ├── 01_01_Item name.png
    └── ...
```

## Benefits

1. **Fully Dynamic**: No manual HTML editing required
2. **Scalable**: Automatically handles any number of items
3. **Maintainable**: Simple text file format for content
4. **Automated**: Image matching and encoding handled automatically
5. **Flexible**: Month names extracted from filenames
6. **Smart Matching**: Only encodes and matches images for items in your lists (70%+ similarity)
7. **Adaptive**: Changes to text files automatically update slide count and content

## Future Enhancements

- Support for custom items per slide (not fixed at 6)
- Validation of text file format
- Error handling for missing images
- Preview mode before overwriting original file
- Support for additional slide types
