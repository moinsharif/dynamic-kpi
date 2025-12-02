# Slide Processing Script

This comprehensive Python script combines three tasks into one streamlined process:

1. **Update HTML Content** - Reads achievements and plans from text files and updates the HTML
2. **Encode Images** - Converts all images in the `img/` folder to base64 format
3. **Insert Images** - Matches and inserts encoded images into the HTML

## Requirements

- Python 3.x
- No external dependencies required (uses only standard library)

## File Structure

```
.
├── process_slide.py          # Main script
├── slide_17.html             # Source HTML file
├── achivment.txt             # Achievements list
├── plans.txt                 # Future plans list
├── img/                      # Images folder
│   ├── 00_01_background.svg
│   ├── 01_01_Separate LMS branches.png
│   ├── 01_02_Separate LMS branches.png
│   └── ... (more images)
└── merged/                   # Generated folder with encoded images
```

## Input File Format

### achivment.txt and plans.txt

Each line should follow this format:
```
Item name --Category
```

**Examples:**
```
Separate LMS branches --LMS-Market
Add Courses landing page --LMS-Market
Dashboard portal batch recommandation --LM
Survey feedback --LMS
Daily Issue fixes
```

**Notes:**
- Text before `--` is the item name
- Text after `--` is the category badge (optional)
- If no `--` is present, the item will have no category badge
- Maximum 6 items will be displayed for each section (achievements and plans)

### Image Files

Images should be named with the following pattern:
```
XX_YY_Title.ext
```

**Examples:**
```
01_01_Separate LMS branches.png
01_02_Separate LMS branches.png
03_01_Research semailer lms.jpg
```

**Notes:**
- `XX` = Main number (groups related images)
- `YY` = Sub number (sequence within group)
- `Title` = Descriptive title (should match achievement/plan text)
- Supported formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`

## Usage

Simply run the script:

```bash
python3 process_slide.py
```

The script will:
1. ✅ Load achievements and plans from text files
2. ✅ Update HTML content with first 6 items from each file
3. ✅ Encode all images in the `img/` folder
4. ✅ Create merged JSON files in `merged/` folder
5. ✅ Match images to achievements/plans by title similarity
6. ✅ Insert encoded images into HTML
7. ✅ Generate `slide_17_updated.html`

## Output

The script creates:
- **slide_17_updated.html** - Final HTML file with updated content and embedded images
- **merged/** folder - Contains JSON files with base64-encoded images

## Script Output Example

```
======================================================================
SLIDE PROCESSING SCRIPT
======================================================================

📝 TASK 1: Updating HTML content with achievements and plans...
----------------------------------------------------------------------
  Loaded 22 achievements
  Loaded 15 plans
  Using max 6 items for each section
  ✓ HTML content updated

🖼️  TASK 2: Encoding images and merging...
----------------------------------------------------------------------
  Encoded: 01_01_Separate LMS branches.png
  Encoded: 01_02_Separate LMS branches.png
  ...
  Created: merged/01_merged_Separate LMS branches.txt with 4 entries
  ✓ Images encoded and merged

🔗 TASK 3: Inserting images into HTML...
----------------------------------------------------------------------
  ✓ Background image inserted
  ✓ Matched 'Separate LMS branches' with '01_merged_Separate LMS branches.txt' (score: 1.00) - 4 images
  ...
  ✓ Achievement images inserted

💾 Writing final output...
----------------------------------------------------------------------
  ✓ Updated HTML saved to: slide_17_updated.html

======================================================================
✅ ALL TASKS COMPLETED SUCCESSFULLY!
======================================================================
```

## Features

### Smart Image Matching
- Uses fuzzy string matching to pair achievements with images
- Handles variations in naming (spaces, underscores, special characters)
- Reports matching confidence score

### Automatic Grouping
- Groups multiple images by their main number prefix
- Maintains proper sequence with sub-numbers
- Creates JSON arrays for easy JavaScript consumption

### Category Badges
- Automatically adds category badges from text files
- Supports custom styling with `.item-category` class
- Optional - items without categories work fine

## Troubleshooting

**No images matched:**
- Check that image filenames contain similar text to achievement/plan names
- Ensure images are in the `img/` folder
- Verify image file extensions are supported

**Missing categories:**
- Ensure text files use `--` separator
- Check for extra spaces around the separator

**HTML not updated:**
- Verify `slide_17.html` exists in the same folder
- Check that achievements/plans sections exist in HTML

## Previous Scripts (Now Deprecated)

This script replaces:
- `encode_and_merge.py` - Image encoding
- `insert_images_to_html.py` - Image insertion
- Manual HTML editing for content updates

All three tasks are now handled by `process_slide.py`!
