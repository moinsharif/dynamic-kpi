# Testing Guide for Slide Processing Script

## Quick Test

Run the script:
```bash
python3 process_slide.py
```

Expected output should show:
- ✅ ALL TASKS COMPLETED SUCCESSFULLY!
- All 4 tasks completed
- Merged folder removed
- Output file created: `basic_slide_updated.html`

## Detailed Testing Checklist

### 1. Script Execution
- [ ] Script runs without errors
- [ ] All 4 tasks complete successfully
- [ ] `basic_slide_updated.html` is created
- [ ] `merged` folder is automatically deleted after processing

### 2. File Structure
Check that these files exist:
- [ ] `basic_slide.html` (original, unchanged)
- [ ] `basic_slide_updated.html` (new, with all fixes)
- [ ] `process_slide.py` (updated with fixes)
- [ ] `November Achivment.txt` (input data)
- [ ] `December Plans.txt` (input data)
- [ ] `notCompletedKPIS.txt` (input data)
- [ ] `images/` folder with all images

### 3. HTML Validation

Open `basic_slide_updated.html` in a browser and test:

#### Navigation Tests
- [ ] Press Right Arrow → moves to next slide
- [ ] Press Left Arrow → moves to previous slide
- [ ] Scroll mouse wheel down → moves to next slide
- [ ] Scroll mouse wheel up → moves to previous slide
- [ ] Slide indicator shows correct count (e.g., "1 / 12")
- [ ] Can navigate through all slides without errors

#### Visual Tests
- [ ] Cover slide displays correctly with logo
- [ ] Team members slide shows 3 team members
- [ ] Achievement slides display all 25 achievements
- [ ] Plan slides display all 9 plans
- [ ] Not Completed KPIs slide shows 7 items
- [ ] Timeline slide displays correctly
- [ ] Thank you slide shows 3 team member images (not placeholders)

#### Image Tests
- [ ] Click on any achievement item → image overlay opens
- [ ] Image overlay shows the correct image
- [ ] Image counter shows correct count (e.g., "1 / 6")
- [ ] Press Right Arrow in overlay → shows next image
- [ ] Press Left Arrow in overlay → shows previous image
- [ ] Scroll mouse wheel in overlay → navigates images
- [ ] Click X button → closes overlay
- [ ] Click outside image → closes overlay
- [ ] Press Escape → closes overlay

#### Auto-play Tests
- [ ] Auto-play starts automatically when page loads
- [ ] "Auto Play: ON" indicator appears in top-right
- [ ] Slides advance automatically every 5 seconds
- [ ] Press F3 → toggles auto-play on/off
- [ ] Manual navigation stops auto-play
- [ ] Press F5 → restarts from first slide and resumes auto-play

### 4. Code Validation

Check the generated HTML:
```bash
# Verify init() is called after DOMContentLoaded
grep -A 2 "Initialize presentation AFTER" basic_slide_updated.html

# Verify no duplicate window.onload
grep "window.onload" basic_slide_updated.html
# Should return nothing

# Verify team member images are inserted
grep "teamMembersData" basic_slide_updated.html | head -5
# Should show base64 image data, not placeholder SVGs
```

### 5. Console Errors

Open browser developer console (F12) and check:
- [ ] No JavaScript errors
- [ ] No "Cannot read property" errors
- [ ] No "undefined" errors
- [ ] No image loading errors

### 6. Performance Tests

- [ ] Page loads in under 3 seconds
- [ ] Slide transitions are smooth
- [ ] Image overlay opens instantly
- [ ] No lag when navigating slides
- [ ] No memory leaks (check browser task manager)

## Common Issues and Solutions

### Issue: Navigation doesn't work
**Cause:** `init()` called before slides are generated  
**Solution:** Already fixed - `init()` now called at end of `DOMContentLoaded`

### Issue: Team member images are placeholders
**Cause:** Images not inserted or `setupImageOverlay()` ran too early  
**Solution:** Already fixed - initialization order corrected

### Issue: Achievement items not clickable
**Cause:** Event handlers not attached  
**Solution:** Already fixed - `setupImageOverlay()` now runs after slides are created

### Issue: Merged folder still exists
**Cause:** Cleanup code was commented out  
**Solution:** Already fixed - cleanup code enabled

## Regression Testing

After making any changes to the script, re-run all tests above to ensure:
1. No new bugs introduced
2. All existing functionality still works
3. Performance hasn't degraded

## Browser Compatibility

Test in multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (if on Mac)
- [ ] Edge

## Mobile Testing (Optional)

If needed, test on mobile devices:
- [ ] Touch swipe left/right for navigation
- [ ] Tap on achievement items to open overlay
- [ ] Pinch to zoom works correctly
- [ ] Responsive layout adapts to screen size

## Automated Testing Script

You can create a simple test script:
```bash
#!/bin/bash
echo "Running slide processing script..."
python3 process_slide.py

echo ""
echo "Checking output..."
if [ -f "basic_slide_updated.html" ]; then
    echo "✓ Output file created"
else
    echo "✗ Output file missing"
    exit 1
fi

if [ -d "merged" ]; then
    echo "✗ Merged folder not cleaned up"
    exit 1
else
    echo "✓ Merged folder cleaned up"
fi

echo ""
echo "Checking HTML structure..."
slide_count=$(grep -c 'id="slide-' basic_slide_updated.html)
echo "Found $slide_count static slide declarations"

init_check=$(grep -c "Initialize presentation AFTER" basic_slide_updated.html)
if [ $init_check -eq 1 ]; then
    echo "✓ Initialization fix applied"
else
    echo "✗ Initialization fix missing"
    exit 1
fi

echo ""
echo "✅ All automated checks passed!"
```

Save as `test_script.sh`, make executable with `chmod +x test_script.sh`, and run with `./test_script.sh`.
