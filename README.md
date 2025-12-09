# LMS Team Monthly KPI Presentation

## Language / ভাষা

- 🇬🇧 **English**: You are reading it
- 🇧🇩 **বাংলা**: [README-bn.md](README-bn.md)

---

## About This Project

This is an interactive presentation system that displays the LMS Team's monthly KPI (Key Performance Indicators). Built with HTML, CSS, and JavaScript, it features a Python script for automatic content updates.

### ⚡ Quick Start

```bash
# 1. Edit config.txt (theme colors, team name, members)
# 2. Write your tasks in text files
# 3. Place images in images/ folder (matching task names)
# 4. Run the Python script
python make_slide.py

# 5. Open the generated HTML file
# Open [Month]-KPI.html in your browser
```

### 🎯 Key Point

**MOST IMPORTANT:** Image filenames MUST match task names 100%!

- Task: `Survey feedback` → File: `Survey feedback-01.png` ✅
- Task: `Learner/Trainer location` → File: `Learner_Trainer location-01.png` ✅
- Special characters (`/`, `,`, `:`, etc.) → Replace with underscore `_`

## Features

### 🎯 Core Features
- **Dynamic Slide Generation**: Automatically creates slides from text files
- **Image Gallery**: Clickable image gallery for each achievement
- **Auto-Play Mode**: Automatically advances slides (every 5 seconds)
- **Keyboard Navigation**: Navigate slides using arrow keys
- **Mouse Wheel Support**: Scroll to change slides
- **Responsive Design**: Looks great on all devices
- **3D Logo Animation**: Rotating 3D LMS logo

### 📊 Slide Types
1. **Cover Slide**: Project title and team members
2. **Team Members Slide**: Team members and statistics
3. **Achievements Slide**: Monthly completed tasks (with images)
4. **Not Completed KPIs Slide**: Tasks that are still pending
5. **Plans Slide**: Next month's planned tasks
6. **Timeline Slide**: Project timeline
7. **Thank You Slide**: Team member photos

## How It Works

### Process Flow

```
📝 Text Files            🖼️ Image Files
    ↓                        ↓
[Task List]            [Task Name-01.png]
    ↓                        ↓
    └────────┬───────────────┘
             ↓
      🐍 Python Script
      (make_slide.py)
             ↓
      ┌──────┴──────┐
      ↓             ↓
  Parse Data    Encode Images
      ↓             ↓
      └──────┬──────┘
             ↓
      Match & Merge
             ↓
      📄 HTML Output
      ([Month]-KPI.html)
             ↓
      🌐 Browser
      (Interactive Presentation)
```

### 1. Data Input
The project reads data from three text files:

- **`[Month] Achivment.txt`**: Monthly achievements list
  ```
  Survey feedback --LMS
  Dashboard portal batch recommandation --LM
  ```

- **`[Month] Plans.txt`**: Next month's plans
  ```
  Daily DB backup functionality --LMS-Market
  Application backup --LMS-Market
  ```

- **`notCompletedKPIS.txt`**: Incomplete tasks list
  ```
  Daily DB backup functionality --LMS-Market
  Order revnue report --LMS-Market
  ```

### 2. Image Processing
Image files in the `images/` folder must match task names 100%:
```
[Task Name]-[ImageNumber].[ext]
```
Example: `Survey feedback-01.png`

**Important:** Replace special characters that are not allowed in filenames with underscores (_).

### 3. Python Script (`make_slide.py`)
This script performs three tasks:
1. Reads data from text files and updates HTML
2. Encodes images to Base64
3. Inserts encoded images into HTML

### 4. HTML Presentation
The `basic_slide.html` file is a complete interactive presentation that:
- Dynamically generates slides using JavaScript
- Displays image gallery overlay
- Handles keyboard and mouse input

## How to Use

### Requirements
- Python 3.x
- A modern web browser (Chrome, Firefox, Edge)

### Step 1: Configure Your Presentation
Edit `config.txt` to customize your presentation:

```txt
# Theme Colors (Hex color codes)
PRIMARY_COLOR=#d5114a
PRIMARY_LIGHT=#ff6b8b
PRIMARY_DARK=#a00d38

# Team Information
TEAM_NAME=LMS Team
TEAM_FULL_NAME=LMS Development Team

# Team Members (separate with comma)
TEAM_MEMBERS=Fizul Haque,Samiul Islam,Moin Sharif

# Contact Information
CONTACT_EMAIL=info@orbittechinc.com
```

### Step 2: Prepare Data
1. Write your achievements list in `[Month] Achivment.txt`
2. Write plans in `[Month] Plans.txt`
3. Write incomplete tasks in `notCompletedKPIS.txt`

**Format:**
```
Task name --Category
```

### Step 3: Add Images
Place your images in the `images/` folder. Name files like this:

**Format:**
```
[Task Name]-[ImageNumber].[ext]
```

**Examples:**
```
Survey feedback-01.png
Survey feedback-02.png
Dashboard portal batch recommandation-01.png
Dashboard portal batch recommandation-02.png
```

**Special Note:** Replace special characters that cannot be used in filenames with underscores (_).

### Step 4: Run Python Script
```bash
python make_slide.py
```

This will:
- Read text files
- Encode images
- Create `[Month]-KPI.html` file

### Step 5: Run Presentation
1. Open the generated HTML file in your browser
2. The presentation will start

## Slide Navigation

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `→` (Right Arrow) | Next slide |
| `←` (Left Arrow) | Previous slide |
| `Space` | Next slide |
| `F5` | Return to first slide |
| `F3` | Toggle auto-play on/off |
| `Esc` | Close image gallery |

### Mouse Controls
- **Mouse Wheel**: Scroll up/down to change slides
- **Click**: Click on achievement items to open image gallery

### Auto-Play
- Automatically starts when presentation loads
- Changes slides every 5 seconds
- Stops when you use keyboard or mouse
- Press `F3` to restart

## Image Gallery

### How to Use
1. Click on any achievement item
2. Full-screen image gallery opens
3. Use arrow keys or mouse wheel to navigate images
4. Press `Esc` or click `X` button to close

### Features
- Full-screen view
- Image counter (e.g., 1 / 5)
- Keyboard navigation
- Mouse wheel support
- Click background to close

## File Naming Rules (VERY IMPORTANT)

### Task List and Image File Matching

Image filenames MUST match task list names 100%. Follow these rules:

#### ✅ Correct Examples

**Task List (November Achivment.txt):**
```
Survey feedback --LMS
Dashboard portal batch recommandation --LM
Learner/Trainer location tracking with filter, report generate --LMS
```

**Image Filenames:**
```
Survey feedback-01.png
Survey feedback-02.png
Dashboard portal batch recommandation-01.png
Dashboard portal batch recommandation-02.png
Learner_Trainer location tracking with filter_ report generate-01.png
Learner_Trainer location tracking with filter_ report generate-02.png
```

#### 🔄 Special Character Replacement Table

Replace special characters that cannot be used in Windows/Linux filenames with underscores (_):

| In Task List | In Filename | Example |
|-------------|-------------|---------|
| `/` (slash) | `_` | `Learner/Trainer` → `Learner_Trainer` |
| `\` (backslash) | `_` | `Path\Name` → `Path_Name` |
| `:` (colon) | `_` | `Time: 5pm` → `Time_ 5pm` |
| `*` (asterisk) | `_` | `Note*` → `Note_` |
| `?` (question mark) | `_` | `What?` → `What_` |
| `"` (double quote) | `_` | `"Quote"` → `_Quote_` |
| `<` (less than) | `_` | `<Tag>` → `_Tag_` |
| `>` (greater than) | `_` | `<Tag>` → `_Tag_` |
| `\|` (pipe) | `_` | `A\|B` → `A_B` |
| `,` (comma) | `_` | `A, B` → `A_ B` |
| `.` (dot - in middle) | `_` | `V2.0` → `V2_0` |

#### 📝 Special Character Examples

**Task:** `Learner/Trainer location tracking with filter, report generate`
**Filename:** `Learner_Trainer location tracking with filter_ report generate-01.png`

**Task:** `Student ID Card, Mail template and UI desgin/update`
**Filename:** `Student ID Card_ Mail template and UI desgin_update-01.png`

**Task:** `Order revnue report`
**Filename:** `Order revnue report-01.png`

#### 🎯 Team Member Images

Special naming for team member photos:
```
TeamMember_01-01.jpg    # Fizul Haque
TeamMember_02-01.jpg    # Samiul Islam
TeamMember_03-01.jpg    # Moin Sharif
```

#### 🖼️ Background Image

For background image:
```
background-01.svg
```

## Project Structure

```
project/
│
├── basic_slide.html          # Main presentation file
├── make_slide.py             # Python script
├── config.txt                # Configuration file (NEW!)
├── [Month] Achivment.txt     # Achievements list
├── [Month] Plans.txt         # Plans list
├── notCompletedKPIS.txt      # Incomplete tasks list
├── [Month]-KPI.html          # Generated file (output)
├── README.md                 # English documentation
├── README-bn.md              # Bengali documentation
│
└── images/                   # Images folder
    ├── Survey feedback-01.png
    ├── Survey feedback-02.png
    ├── Dashboard portal batch recommandation-01.png
    ├── Learner_Trainer location tracking with filter_ report generate-01.png
    ├── TeamMember_01-01.jpg
    ├── TeamMember_02-01.jpg
    ├── TeamMember_03-01.jpg
    └── background-01.svg
```

## Customization

### 🎨 Easy Customization via config.txt

The easiest way to customize your presentation is by editing `config.txt`:

#### Change Theme Colors
```txt
PRIMARY_COLOR=#d5114a      # Main theme color
PRIMARY_LIGHT=#ff6b8b      # Light variant
PRIMARY_DARK=#a00d38       # Dark variant
```

**Popular Color Schemes:**
- **Blue Theme**: `#1e40af`, `#3b82f6`, `#1e3a8a`
- **Green Theme**: `#15803d`, `#22c55e`, `#14532d`
- **Purple Theme**: `#7c3aed`, `#a78bfa`, `#5b21b6`
- **Orange Theme**: `#ea580c`, `#fb923c`, `#c2410c`

#### Change Team Information
```txt
TEAM_NAME=Your Team Name
TEAM_FULL_NAME=Your Full Team Name
TEAM_MEMBERS=Member 1,Member 2,Member 3,Member 4
CONTACT_EMAIL=your.email@example.com
```

**Notes:**
- You can add as many team members as you want (separate with commas)
- Team member images should be named: `TeamMember_01-01.jpg`, `TeamMember_02-01.jpg`, etc.
- If you have more members than images, placeholders will be used

### Advanced Customization

#### Items Per Slide
Change `itemsPerSlide` in `make_slide.py`:
```python
"itemsPerSlide": 6,  # 6 items per slide
```

#### Auto-Play Duration
In the JavaScript section of `basic_slide.html`:
```javascript
autoPlayInterval = setInterval(() => {
    nextSlide();
}, 5000);  // 5000 milliseconds = 5 seconds
```

## Troubleshooting

### Problem: Images not showing
**Solution:**
- Check if image filenames match task list names 100%
- Verify special characters are replaced with underscores (_)
- Ensure images exist in `images/` folder
- Run Python script again and check console messages
- Look for "✓ Matched" messages in console

### Problem: Slides not generating
**Solution:**
- Check text file format is correct
- Verify filenames are correct (e.g., `November Achivment.txt`)
- Ensure Python 3.x is installed

### Problem: Navigation not working
**Solution:**
- Refresh browser (Ctrl+F5)
- Check JavaScript console (F12)
- Use a modern browser

## Quick Reference Guide

### File Naming Checklist ✅

1. **Copy name from task list**
2. **Check for special characters:**
   - Has `/`? → Replace with `_`
   - Has `,`? → Replace with `_`
   - Has `:`? → Replace with `_`
   - Other special characters? → Replace with `_`
3. **Add `-01`, `-02`, etc. at the end**
4. **Add extension** (`.png`, `.jpg`)

### Quick Examples

| Task List | Filename |
|-----------|----------|
| `Survey feedback` | `Survey feedback-01.png` |
| `Learner/Trainer location` | `Learner_Trainer location-01.png` |
| `ID Card, Mail template` | `ID Card_ Mail template-01.png` |
| `UI desgin/update` | `UI desgin_update-01.png` |

## Tips and Tricks

### 1. Quick Presentation Creation
```bash
# Do everything in one command
python make_slide.py && start [Month]-KPI.html
```

### 2. Image Optimization
- Keep image size small (< 500KB)
- Use PNG or JPG format
- Resolution should not exceed 1920x1080

### 3. Sharing Presentations
- Generated HTML file can be shared directly
- All images are embedded (Base64)
- Works without internet

### 4. Verify Filenames
After running the Python script, check the console:
```
✓ Matched 'Survey feedback' with 'Survey feedback.txt' (score: 1.00) - 3 images
✗ No match found for 'Dashboard portal'
     Suggested filename: Dashboard portal-01.png
```
If you see `✗ No match found`, fix the filename.

## Frequently Asked Questions (FAQ)

### ❓ How do I change the theme color?

**Answer:** Edit `config.txt` and change the `PRIMARY_COLOR`, `PRIMARY_LIGHT`, and `PRIMARY_DARK` values.

```txt
PRIMARY_COLOR=#1e40af    # Change to your preferred color
PRIMARY_LIGHT=#3b82f6
PRIMARY_DARK=#1e3a8a
```

### ❓ How do I add or remove team members?

**Answer:** Edit `config.txt` and modify the `TEAM_MEMBERS` line. Separate names with commas.

```txt
TEAM_MEMBERS=Alice,Bob,Charlie,David
```

### ❓ How do I change the team name?

**Answer:** Edit `config.txt` and change `TEAM_NAME` and `TEAM_FULL_NAME`.

```txt
TEAM_NAME=Marketing Team
TEAM_FULL_NAME=Marketing Department
```

### ❓ How do I fix image filenames?

**Answer:** Copy the name from task list and replace special characters with underscores.

```
Task: Learner/Trainer location tracking with filter, report generate
File: Learner_Trainer location tracking with filter_ report generate-01.png
```

### ❓ How do I add multiple images for one task?

**Answer:** Create files with the same name using `-01`, `-02`, `-03`, etc.

```
Survey feedback-01.png
Survey feedback-02.png
Survey feedback-03.png
```

### ❓ Why does console show "No match found"?

**Answer:** Image filename doesn't match task list. Check the name and fix special characters.

### ❓ How do I change the background image?

**Answer:** Place a file named `background-01.svg` in the `images/` folder.

### ❓ How do I add team member photos?

**Answer:** Create three files:
```
TeamMember_01-01.jpg
TeamMember_02-01.jpg
TeamMember_03-01.jpg
```

### ❓ How do I change items per slide?

**Answer:** Change the `itemsPerSlide` value in `make_slide.py` (default: 6).

### ❓ Will the presentation work offline?

**Answer:** Yes! All images are Base64 encoded, so it works without internet.

## Cheat Sheet 📋

### Special Character Replacements

| Character | Replace With | Example |
|-----------|-------------|---------|
| `/` | `_` | `A/B` → `A_B` |
| `\` | `_` | `A\B` → `A_B` |
| `:` | `_` | `A:B` → `A_B` |
| `*` | `_` | `A*B` → `A_B` |
| `?` | `_` | `A?B` → `A_B` |
| `"` | `_` | `"A"` → `_A_` |
| `<` | `_` | `<A>` → `_A_` |
| `>` | `_` | `<A>` → `_A_` |
| `\|` | `_` | `A\|B` → `A_B` |
| `,` | `_` | `A, B` → `A_ B` |

### Command Reference

```bash
# Create presentation
python make_slide.py

# Open directly on Windows
python make_slide.py && start November-KPI.html

# Open directly on Linux/Mac
python make_slide.py && xdg-open November-KPI.html
```

### Filename Templates

```
# Achievement images
[Task Name]-01.png
[Task Name]-02.png

# Team members
TeamMember_01-01.jpg
TeamMember_02-01.jpg
TeamMember_03-01.jpg

# Background
background-01.svg
```

### Quick Debugging

If images don't show:
1. Check console: `✗ No match found for 'Task Name'`
2. Check filename: Does it match task list?
3. Check special characters: Replaced with underscores?
4. Check file extension: `.png`, `.jpg`, `.jpeg`?

## License and Credits

This project was created for the LMS Team.

**Technologies Used:**
- HTML5
- CSS3 (Flexbox, Grid, Animations)
- JavaScript (ES6+)
- Python 3
- Font Awesome Icons
- Google Fonts (Inter, Space Grotesk)

## Contact

For questions or help, contact:
- Email: info@orbittechinc.com
- Team: LMS Development Team

---

**Last Updated:** December 2024

**IMPORTANT NOTE:** Image filenames MUST match task list names 100%. Replace special characters with underscores (_).

---

## Language / ভাষা

- 🇬🇧 **English**: You are reading it
- 🇧🇩 **বাংলা**: [README-bn.md](README-bn.md)
