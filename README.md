# Roblox Arcane Odyssey - Background Fishing Macro

A sophisticated fishing automation script for Roblox Arcane Odyssey that works even when the game window is in the background. Features automatic fishing, hunger management, Discord notifications with screenshots, and emergency stop capabilities.

---

## 🎯 CRITICAL: RESOLUTION-DEPENDENT DETECTION

### ⚠️ **IMAGE DETECTION ACCURACY DEPENDS HEAVILY ON YOUR MONITOR RESOLUTION**

**THIS IS THE #1 REASON WHY THE MACRO MAY NOT WORK FOR YOU!**

The provided detection images (`point.png`, `fish.png`, etc.) were taken at a **specific game resolution and graphics settings**. If your game runs at a **different resolution**, the template matching will have **poor accuracy** or **fail completely**.

**Why this matters:**
- Template matching compares pixel patterns
- Different resolutions = different pixel patterns
- Even small resolution differences can cause mismatches
- Graphics settings (quality, brightness) also affect matching

**SOLUTION:**
1. **TEST FIRST** with the provided images
2. **If detection fails**, you **MUST** retake screenshots at **YOUR** resolution
3. See the [Detection Images Setup](#detection-images-setup) section below

---

## 🤖 PROJECT NOTICE - AI GENERATED CODE

**⚠️ This entire project is 100% "vibe coded" using AI (GitHub Copilot).**

What this means:
- 🧑‍💻 **Human role:** Prompting and describing how the program should work
- 🤖 **AI role:** Writing 100% of the actual code implementation
- 📄 **Documentation:** Even this README.md is AI-generated through prompting
- 🎯 **Result:** Educational demonstration of AI-assisted development

**USE WITH CAUTION:** This is a pure AI coding experiment - all code, logic, implementation decisions, AND documentation were created by AI based on natural language descriptions. The AI may have made assumptions or errors. Always review and test before use.

---

## ⚠️ CRITICAL WARNING - BAN RISKS

### Roblox Terms of Service
**Using automation scripts in Roblox violates their Terms of Service and WILL result in account bans.** Use at your own risk.

### Arcane Odyssey In-Game Rules - Section 2.3 Macroing

**📖 Full Official Rulebook:** [Arcane Odyssey Rules Document](https://docs.google.com/document/d/1oh7TLdW6aN6mAyk55BDF_ga-eMl_nHNECo2Bmqa71XA/edit?usp=sharing)

According to the official Arcane Odyssey rulebook, macroing violations result in **2 STRIKES (caps at 5 strikes total)**:

#### 2.3.1 - Definition
> "Usage of programs that automate a process that would typically require a certain degree of attention in order to not fail the task. **If you are present at your computer and are able to respond to stimuli within the game then this is permitted.**"

**This means:**
- ✅ **ALLOWED:** Using macros while actively present and able to respond
- ❌ **BANNED:** Leaving macro running unattended/AFK where it requires no attention

#### 2.3.2 - Alternate Accounts
> "Alternate accounts blatantly used for macroing will be permanently banned."

**This means:**
- ❌ Alt accounts used ONLY for macroing = **PERMANENT BAN**

#### 2.3.3 - Alt Account Appeals
> "Alternate accounts that are not exclusively used for macroing can be appealed with an inventory wipe after the main account ban duration."

**This means:**
- ⚠️ Alt accounts with other activities can appeal but lose all items

#### 2.3.4 - AFK While Macroing
> "You are permitted to AFK while macroing for the sake of staying in the server by eating or doing similar actions, provided you are in an accessible location."

**This means:**
- ✅ **ALLOWED:** AFK auto-eating to stay in server (if in accessible location)
- ❌ **BANNED:** AFK fishing macro (requires attention to not fail)

#### 2.3.5 - Moderator Actions
> "Moderator tools may be used to roll back or completely wipe the inventories or fishing progress/journal statistics of any affected slot."

**This means:**
- ⚠️ Even if not banned, you may lose all fishing progress and items

### Penalty System

| Offense | Strikes | Ban Duration |
|---------|---------|--------------|
| First Macroing Offense | 2 | 3 days |
| Second Macroing Offense | 4 | 7 days |
| Third Macroing Offense | 5 (cap) | 14 days |
| Subsequent Offenses | 5 (cap) | 14 days |

**Note:** Strikes cap at 5. Each offense adds 2 strikes.

**📖 Source:** [Official Arcane Odyssey Rules - Section 2.3](https://docs.google.com/document/d/1oh7TLdW6aN6mAyk55BDF_ga-eMl_nHNECo2Bmqa71XA/edit?usp=sharing)

### How to Use This Macro Safely (Within Rules)

According to rule 2.3.1, you **MUST**:
1. ✅ Be present at your computer
2. ✅ Be able to respond to in-game stimuli/chat
3. ✅ Be in an accessible location (not hiding)
4. ✅ Monitor the macro actively

**DO NOT:**
- ❌ Leave the macro running while you sleep
- ❌ Leave the macro running while you're away
- ❌ Use on alt accounts exclusively for macroing
- ❌ Hide in inaccessible locations

**RECOMMENDATION:** This script is for **educational purposes only**. Understanding the risks:
- First offense: 3-day ban + 2 strikes
- Possible inventory/fishing progress wipe
- Alt accounts used only for macroing = permanent ban

---

## 🚀 Quick Start Guide

### Prerequisites

- **Windows 10/11** (Required - uses Windows-specific APIs)
- **Python 3.8 or higher** ([Download here](https://www.python.org/downloads/))
- **Roblox** with Arcane Odyssey installed
- **Administrator privileges** (for input blocking feature)

### Step 1: Installation

1. **Clone or download this repository** to a folder on your computer

2. **Open PowerShell in the project folder**
   - Right-click the folder → "Open in Terminal" or "Open PowerShell window here"

3. **Run the installation script:**
   ```powershell
   cd scripts
   .\install.bat
   ```

   Or install manually:
   ```powershell
   pip install -r requirements.txt
   ```

### Step 2: Configuration

**Option A: Quick Setup (Recommended)**
```powershell
python setup_wizard.py
```

The wizard will guide you through:
- Discord webhook setup (optional)
- Detection sensitivity configuration
- Eating schedule defaults
- Screenshot settings

**Option B: Manual Configuration**
1. Copy the example config:
   ```powershell
   copy config.example.py config.py
   ```

2. Edit `config.py` with your settings:
   - Discord webhook URL (if you want notifications)
   - Detection confidence thresholds
   - Timing and safety settings
   - Inventory slot keys

**⚠️ IMPORTANT:** Your `config.py` file contains your Discord webhook URL and will NOT be committed to git (it's in .gitignore).

### Step 3: Detection Images Setup

**⚠️ CRITICAL: Resolution-Dependent Detection**

The provided detection images may NOT work for your monitor resolution!

#### Test First:
1. Try running the macro with provided images
2. Watch if it detects fishing bites correctly
3. If it fails or has low accuracy, proceed to create your own

#### Create Your Own Detection Images:

**REQUIRED: Fishing Bite Indicator (`point.png`)**

1. Launch Roblox Arcane Odyssey at YOUR normal resolution
2. Start fishing and wait for a bite
3. When the bite indicator appears:
   - Press **Print Screen** (default Roblox screenshot button)
   - Roblox will save a screenshot to your Pictures folder
   - Open the screenshot in an image editor (Paint, Photoshop, etc.)
   - **Crop ONLY the bite indicator** from the screenshot
4. Save the cropped image as: `assets/images/detection/point.png`
5. **This is REQUIRED** - without it, the macro won't work

**OPTIONAL: Caught Indicators**

For better detection speed, capture these the same way:
1. Fish caught screen → crop and save as `fish_arcane_odyssey.png`
2. Treasure caught → crop and save as `treasure_arcane_odyssey.png`
3. Sunken item → crop and save as `sunken_arcane_odyssey.png`
4. Junk caught → crop and save as `junk_arcane_odyssey.png`

**Tips for best results:**
- Always use **Print Screen** in Roblox for consistent quality
- Use consistent resolution (don't change game window size)
- Use same graphics settings when playing
- Crop carefully - include ONLY the indicator, not extra background
- Make sure the cropped image is clear and not blurry
- Adjust confidence values in config.py if needed (0.55-0.75)

### Step 4: In-Game Setup

1. **Launch Roblox Arcane Odyssey**
2. **Equip your fishing rod** in slot **9** (or change `ROD_SLOT_KEY` in config.py)
3. **Put food items** in slot **0** (or change `FOOD_SLOT_KEY` in config.py)
4. **Stand at your fishing location**
5. **Cast your fishing rod** once to start
6. Keep the window title as **"Roblox"** (default, or change `WINDOW_NAME` in config.py)

### Step 5: Run the Macro

1. **Open PowerShell as Administrator** (right-click → "Run as administrator")
   - ⚠️ Administrator required for input blocking to work

2. **Navigate to project folder:**
   ```powershell
   cd c:\path\to\roblox-arcane-odyssey-macro-fishing
   ```

3. **Run the macro:**
   ```powershell
   python background_fishing_macro.py
   ```

4. **Follow the prompts:**
   - Enter duration in seconds (e.g., 3600 for 1 hour)
   - Enter eating interval (or press Enter for default from config)
   - Enter eating count (or press Enter for default from config)
   - Enable debug mode (y/n) - shows detailed information

5. **🚨 EMERGENCY STOP:** Press **Ctrl+Alt+M** anytime to stop immediately

---

## ✨ Features

### Core Features
- ✅ **Background Operation** - Captures window even when not in focus
- ✅ **Configurable Settings** - Easy config.py file for all settings
- ✅ **Smart Click Detection** - Detects fishing bite indicator and clicks automatically
- ✅ **High-Speed Clicking** - Configurable click speed (default: 1000 clicks/sec theoretical max)
- ✅ **Auto-Casting** - Recasts fishing rod after configured timeout (default: 60s)
- ✅ **Input Blocking** - Blocks your keyboard/mouse during fishing to prevent interference
- ✅ **Safety Timeouts** - Configurable safety unblock (default: 90s)
- ✅ **Emergency Stop** - Press Ctrl+Alt+M to stop immediately and unblock input
- ✅ **Mouse Position Restoration** - Returns mouse to original position after fishing

### Eating System
- ✅ **User-Configurable Schedule** - Set eating interval and count
- ✅ **Smart Eating Logic** - Doesn't eat while actively fishing
- ✅ **Auto Re-equip** - Automatically re-equips fishing rod after eating
- ✅ **Configurable Slots** - Change food/rod slots in config.py

### Discord Integration
- ✅ **Catch Notifications** - Get notified on Discord when fish are caught
- ✅ **Screenshot Attachments** - Sends actual game screenshot with notification
- ✅ **Catch Statistics** - Shows total catches, catch breakdown by type
- ✅ **Session Info** - Displays session duration, time since last meal, clicks
- ✅ **Auto-cleanup** - Optionally deletes screenshots after sending to save storage

### Safety Features
- ✅ **Configurable Safety Timeout** - Force-unblocks input after configured time (default: 90s)
- ✅ **Configurable Click Timeout** - Stops clicking after configured duration (default: 20s)
- ✅ **Input Unblocking** - Always unblocks input even if script crashes
- ✅ **Window Restoration** - Returns focus to your previous window after actions
- ✅ **Mouse Position Restore** - Returns cursor to original position
- ✅ **Emergency Stop** - Works even when input is blocked (requires admin)
- ✅ **Try-Finally Blocks** - Ensures cleanup always happens

### Advanced Features
- ✅ **Template Matching** - OpenCV-based image detection
- ✅ **Adjustable Confidence** - Configure detection sensitivity in config.py
- ✅ **Multiple Catch Types** - Detects fish, treasure, sunken items, junk separately
- ✅ **Parallel Detection** - Separate thread for detection while clicking
- ✅ **Resolution-Independent** - Works with custom screenshots at any resolution
- ✅ **Setup Wizard** - Interactive configuration tool for first-time setup

---

## ⚙️ Configuration

### Configuration File (`config.py`)

All settings are in `config.py`. Copy from `config.example.py` to get started.

#### Discord Settings
```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
ENABLE_DISCORD_NOTIFICATIONS = True
```

#### Detection Settings
```python
# ⚠️ Adjust these if detection is not working!
POINT_CONFIDENCE = 0.65  # Lower = more sensitive (0.55-0.75)
FISH_CONFIDENCE = 0.75   # Caught fish detection
```

#### Timing Settings
```python
MAX_CLICKING_DURATION = 20  # Stop after 20s of clicking
NO_DETECTION_TIMEOUT = 60   # Auto-cast after 60s
CLICK_DELAY = 0.001         # Click speed (1ms between clicks)
```

#### Eating Settings
```python
DEFAULT_EATING_INTERVAL = 300  # Default: eat every 5 minutes
DEFAULT_EATING_COUNT = 3       # Default: eat 3 times per session
FOOD_SLOT_KEY = 0x30          # Slot 0 for food
ROD_SLOT_KEY = 0x39           # Slot 9 for rod
```

#### Safety Settings
```python
CRITICAL_SAFETY_TIMEOUT = 90  # Force unblock after 90s
```

#### Screenshot Settings
```python
SAVE_DETECTION_SCREENSHOTS = True   # Save screenshots
DELETE_SCREENSHOTS_AFTER_DISCORD = True  # Delete after sending
```

### Adjusting Detection Sensitivity

If the macro is:
- **Missing fish bites** → Lower `POINT_CONFIDENCE` (try 0.55 or 0.60)
- **Too many false positives** → Raise `POINT_CONFIDENCE` (try 0.75 or 0.80)
- **Not detecting catches** → Lower `FISH_CONFIDENCE`, `TREASURE_CONFIDENCE`, etc.

**Most common issue:** Detection images don't match your resolution → Retake screenshots!

---

## 📊 How It Works

### Detection System

1. **Template Matching** - Uses OpenCV to compare game screenshots with your detection images
2. **Confidence Threshold** - Only triggers when similarity exceeds configured threshold
3. **Resolution Dependent** - Works best with screenshots taken at YOUR resolution using Roblox's Print Screen
4. **Multiple Detectors** - Supports different catch types (fish, treasure, sunken, junk, etc.)

### Why Resolution Matters

- Template matching compares pixel patterns
- Different resolutions = different pixel sizes and arrangements
- A 1920x1080 screenshot won't match well at 1280x720
- Even UI scaling affects detection accuracy

**Solution:** Always use Roblox's **Print Screen** feature to capture screenshots, then crop them to show only the indicators!

### Clicking System

1. Detects fishing bite indicator (`point.png`)
2. Starts separate detection thread
3. Clicks rapidly at center of screen (configurable speed)
4. Detection thread watches for caught visual in background (fish, treasure, sunken, junk)
5. Stops when caught detected or timeout reached

---

## 🔧 Troubleshooting

### "Window 'Roblox' not found"
- Make sure Roblox is running
- Check window title matches `WINDOW_NAME` in config.py
- Change `WINDOW_NAME` if your window has different title

### "Template image not found"
- Make sure `assets/images/detection/point.png` exists
- Run from project root directory
- Check file paths in `DETECTION_IMAGES` config

### Detection not working / Low accuracy
**This is the #1 issue!**

1. **Resolution mismatch** - Provided images don't match your resolution
   - Solution: Use Roblox's **Print Screen** to capture screenshots, then crop ONLY the indicators
   
2. **Wrong screenshot method** - Used Windows Snipping Tool instead of Roblox's Print Screen
   - Solution: Always use **Print Screen** in Roblox for consistent quality
   
3. **Graphics settings** - Different brightness/quality affects matching
   - Solution: Use consistent graphics settings
   
4. **Confidence too high** - Threshold set too strict
   - Solution: Lower `POINT_CONFIDENCE` to 0.55-0.60
   
5. **Screenshot quality** - Captured indicator is too small/blurry
   - Solution: Crop carefully - include ONLY the indicator, not extra background

### Input blocking doesn't work
- **Must run PowerShell as Administrator**
- Required for `BlockInput` API to work
- Right-click PowerShell → "Run as administrator"

### Fish escaping before caught
- Already optimized (20s max clicking by default)
- Increase `MAX_CLICKING_DURATION` in config.py if needed
- Check detection images are correct for your resolution

### Discord notifications not working
- Verify webhook URL is correct in config.py
- Check webhook hasn't been deleted in Discord
- Test webhook manually with curl or browser

### Emergency stop not responding
- Must run as Administrator for keyboard hook to work
- Hook bypasses `BlockInput` but needs admin privileges
- Alternative: Close PowerShell window (input will unblock)

---

## 📝 File Structure

```
roblox-arcane-odyssey-macro-fishing/
├── background_fishing_macro.py    # Main script
├── config.example.py              # Example configuration (INCLUDED IN GIT)
├── config.py                      # Your configuration (IGNORED BY GIT)
├── setup_wizard.py                # Interactive setup tool
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
├── assets/
│   ├── images/
│   │   └── detection/             # Detection templates
│   │       ├── point.png          # Fishing bite (REQUIRED)
│   │       ├── fish_arcane_odyssey.png
│   │       ├── treasure_arcane_odyssey.png
│   │       ├── sunken_arcane_odyssey.png
│   │       ├── junk_arcane_odyssey.png
│   │       └── caught_arcane_odyssey.png
│   └── screenshots/               # Runtime screenshots (auto-deleted)
│       └── .gitkeep
├── scripts/
│   └── install.bat                # Installation script
└── docs/                          # Additional documentation
```

---

## 🎓 For Developers / Contributors

### Setting Up Development Environment

```powershell
# Clone repository
git clone https://github.com/Naxumi/roblox-arcane-odyssey-macro-fishing.git
cd roblox-arcane-odyssey-macro-fishing

# Install dependencies
pip install -r requirements.txt

# Create your config
copy config.example.py config.py
# Edit config.py with your settings

# Run
python background_fishing_macro.py
```

### Important Notes

- **Never commit `config.py`** - It contains personal webhook URLs
- **config.example.py is the template** - This goes in git
- Users copy example to create their own config.py
- Screenshots folder is gitignored except .gitkeep

### Configuration System

- All settings centralized in `config.py`
- Import at top of main script
- Fallback to defaults if config.py missing
- Setup wizard creates/updates config.py

---

## ❓ FAQ

**Q: Why isn't the macro detecting fish bites?**
A: **#1 reason: Resolution mismatch!** Use Roblox's **Print Screen** button to capture a screenshot, then crop ONLY the bite indicator and save as `point.png`.

**Q: Do the provided detection images work for everyone?**
A: No! They only work if your game runs at the same resolution they were captured at. Most users need to retake screenshots using Roblox's Print Screen.

**Q: Should I use Windows Snipping Tool or Roblox's Print Screen?**
A: Always use Roblox's **Print Screen** button! This ensures consistent quality and resolution. Then crop the screenshot to show only the indicator.

**Q: How do I know what resolution to use?**
A: Use whatever resolution you normally play at. Take screenshots while playing using Print Screen, don't change resolution.

**Q: Can I use this in the background?**
A: Yes! The macro captures the window even when it's not focused. However, you must stay at your computer per game rules.

**Q: Will I get banned?**
A: Yes, this violates game rules. First offense = 3-day ban + 2 strikes. See ban risks section above.

**Q: Can I run this on multiple accounts?**
A: Alt accounts used exclusively for macroing = permanent ban per game rules.

**Q: How do I change which inventory slots are used?**
A: Edit `FOOD_SLOT_KEY` and `ROD_SLOT_KEY` in config.py. Key codes: 0x30=slot 0, 0x31=slot 1, ..., 0x39=slot 9.

**Q: Can I disable Discord notifications?**
A: Yes, set `ENABLE_DISCORD_NOTIFICATIONS = False` in config.py.

**Q: Can I disable screenshots?**
A: Yes, set `SAVE_DETECTION_SCREENSHOTS = False` in config.py.

**Q: How do I stop the macro?**
A: Press Ctrl+Alt+M (emergency stop) or close the PowerShell window.

---

## 📜 License

This project is for **educational purposes only**. Use at your own risk.

By using this software, you acknowledge:
- You understand this violates Roblox Terms of Service
- You understand this violates Arcane Odyssey game rules
- You accept full responsibility for any consequences
- The authors are not responsible for any bans or penalties

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Never commit:**
- Personal `config.py` files
- Discord webhook URLs
- Runtime screenshots
- Personal game data

---

## 📞 Support

- **Issues:** Open an issue on GitHub
- **Documentation:** Read this README and docs/ folder
- **Setup Help:** Run `python setup_wizard.py`
- **Detection Problems:** 99% of the time it's resolution mismatch - retake screenshots!

---

**🎣 Happy Fishing! (Responsibly and at your own risk)**

Remember: This is an educational project demonstrating AI-assisted development and computer vision techniques. Always follow game rules and use responsibly.
    ├── test_all_input_methods.py
    ├── visual_input_test.py
    └── background_input_examples.py
```

### Step 3: In-Game Setup

1. **Launch Roblox Arcane Odyssey**
2. **Equip your fishing rod** in slot **9**
3. **Put food items** in slot **0**
4. **Stand at your fishing location**
5. **Cast your fishing rod** once to start
6. Keep the window title as **"Roblox"** (default)

### Step 4: Run the Macro

1. **Open PowerShell as Administrator** (right-click → "Run as administrator")
   - This is required for input blocking to work properly

2. **Navigate to project folder:**
   ```powershell
   cd C:\path\to\roblox-arcane-odyssey-macro-fishing
   ```

3. **Activate virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. **Run the macro:**
   ```powershell
   python background_fishing_macro.py
   ```

5. **Follow the prompts:**
   - Enter how many seconds to run (e.g., 3600 for 1 hour)
   - Choose debug mode (y/n) - default is yes for detailed logs

6. **🚨 EMERGENCY STOP:** Press **ESC** or **END** key anytime to stop immediately

---

## ✨ Features

### Core Features
- ✅ **Background Operation** - Captures window even when not in focus
- ✅ **Smart Click Detection** - Detects fishing bite indicator and clicks automatically
- ✅ **High-Speed Clicking** - 150 clicks minimum (83 cps burst, then 66 cps sustained)
- ✅ **Auto-Casting** - Recasts fishing rod after 70 seconds of no activity
- ✅ **Input Blocking** - Blocks your keyboard/mouse during fishing to prevent interference
- ✅ **90-Second Safety Timeout** - Automatically unblocks input after 90 seconds (critical safety)
- ✅ **Emergency Stop** - Press ESC or END key to stop immediately and unblock input
- ✅ **Mouse Position Restoration** - Returns mouse to original position after fishing

### Eating System
- ✅ **Random Eating Schedule** - Eats food automatically every 60-120 seconds (randomized)
- ✅ **Smart Eating Logic** - Doesn't eat while actively fishing
- ✅ **Auto Re-equip** - Automatically re-equips fishing rod after eating

### Safety Features
- ✅ **90-Second Critical Safety** - Force-unblocks input after 90 seconds regardless of state
- ✅ **84-Second Click Timeout** - Stops clicking after 84 seconds
- ✅ **40-Second Normal Timeout** - Regular timeout for normal fish
- ✅ **Input Unblocking** - Always unblocks input even if script crashes
- ✅ **Window Restoration** - Returns focus to your previous window after actions
- ✅ **Mouse Position Restore** - Returns cursor to original position
- ✅ **Emergency Stop** - Works even when input is blocked (if run as admin)
- ✅ **Try-Finally Blocks** - Ensures cleanup always happens

### Advanced Features
- ✅ **Template Matching** - OpenCV-based image detection
- ✅ **Confidence Thresholds** - Adjustable detection sensitivity
- ✅ **Click Patterns** - Smart clicking (150 clicks minimum, handles rare/golden/massive fish)
- ✅ **Click Speed** - 83 cps initial burst (12ms delay), then 66 cps sustained (15ms delay)
- ✅ **Center-Screen Clicking** - All clicks at screen center for consistency
- ✅ **Multi-Timeout System** - 40s normal, 84s safety, 90s critical force-unblock
- ✅ **Detailed Logging** - Debug mode shows everything happening
- ✅ **Statistics Tracking** - Total detections, clicks, eating count

---

## 📋 How It Works

### The Fishing Cycle

```
1. Capture Window (Background) ──────────> No focus required ✅
        ↓
2. Detect point.png ─────────────────────> Image detection ✅
        ↓
3. [DETECTED] Save Mouse Position ───────> For restoration later 🖱️
        ↓
4. [DETECTED] Block Input ───────────────> Prevent interference 🔒
        ↓
5. Focus Window Briefly ─────────────────> Required for input ⚠️
        ↓
6. Spam Click at CENTER (150+ minimum) ──> Fast clicking (83->66 cps) 🖱️
        ↓
7. Check if point.png disappeared ───────> Fish caught? 🎣
        ↓
8. Unblock Input (max 90s) ──────────────> Critical safety timeout 🔓
        ↓
9. Restore Mouse Position ───────────────> Back to original spot 🖱️
        ↓
10. Restore Previous Window ─────────────> Back to what you were doing ✅
        ↓
11. Check if time to eat ────────────────> User-configured interval 🍖
        ↓
12. Repeat from step 1
```

### The Eating Cycle (User-Configured Interval)

```
1. Check Timer ───────────────────────────> Time elapsed? ⏱️
        ↓
2. [TIME TO EAT] Block Input ─────────────> Prevent interference 🔒
        ↓
3. Focus Window ──────────────────────────> Required for keypresses ⚠️
        ↓
4. Press configured food key ────────────> Select food slot (default: '0') 🍖
        ↓
5. Click 3 times (0.8s delay each) ───────> Consume 3 food items
        ↓
6. Wait 1 second ─────────────────────────> Let animation finish
        ↓
7. Press configured rod key ──────────────> Select fishing rod (default: '9') 🎣
        ↓
8. Click once ────────────────────────────> Cast rod
        ↓
9. Unblock Input ─────────────────────────> Restore control 🔓
        ↓
10. Schedule Next Meal ───────────────────> Based on config interval
```

---

## 🎓 For Developers

### Catch Type Detection

The macro detects multiple catch types based on configuration in `config.py`:

```python
# Catch type detectors (loaded from DETECTION_IMAGES dict)
detector_configs = [
    ('fish', FISH_CONFIDENCE),           # Regular fish
    ('treasure', TREASURE_CONFIDENCE),   # Treasure chests
    ('sunken', SUNKEN_CONFIDENCE),       # Sunken items
    ('junk', JUNK_CONFIDENCE),           # Junk items
    ('caught', CAUGHT_CONFIDENCE),       # Generic caught screen
]
```

Each catch type has:
- Dedicated detection image (e.g., `fish_arcane_odyssey.png`)
- Configurable confidence threshold
- Optional (macro works without them)

### Configuration System

All settings are externalized to `config.py`:
- Discord webhook settings
- Detection confidence thresholds
- Timing parameters (click duration, timeouts)
- Eating schedule defaults
- Inventory slot key codes
- Screenshot preferences

See `config.example.py` for all available options.

---

## 🎮 Inventory Setup

For the macro to work properly, set up your inventory:

- **Slot 0:** Food items (any food for hunger)
- **Slot 9:** Fishing rod (or change `ROD_SLOT_KEY` in config.py)
- **Other slots:** Whatever you want

The macro will:
1. Press configured food key (default: **'0'**)
2. Click **3 times** to consume food
3. Press configured rod key (default: **'9'**)
4. Click **once** to cast

---

## 🐛 Troubleshooting

### Common Issues

#### "Window 'Roblox' not found"
**Problem:** Script can't find Roblox window
**Solutions:**
- Make sure Roblox is running
- Check window title is exactly "Roblox" (or change `WINDOW_NAME` in config.py)
- Try running in-game (not in menu)

#### "Template image not found: assets/images/detection/point.png"
**Problem:** Missing required screenshot
**Solutions:**
- Use Roblox's **Print Screen** to capture a screenshot
- Crop ONLY the fishing bite indicator
- Save as `assets/images/detection/point.png`
- Check filename is exact (case-sensitive)

#### "Failed to capture window"
**Problem:** Can't capture Roblox window content
**Solutions:**
- Run PowerShell as Administrator
- Try keeping window visible but in background
- Some systems block PrintWindow API

#### Input blocking doesn't work
**Problem:** Your keyboard/mouse still work during fishing
**Solutions:**
- **Run PowerShell as Administrator** (required!)
- Input blocking requires admin privileges
- Emergency stop still works regardless

#### Keypresses not working
**Problem:** Food/rod not selected
**Solutions:**
- Script must briefly focus window (this is normal)
- Make sure slots have items (default: slot 0 for food, slot 9 for rod)
- Check `FOOD_SLOT_KEY` and `ROD_SLOT_KEY` in config.py
- Debug mode shows if keys are being pressed

#### No detections / Not clicking
**Problem:** Macro doesn't detect fishing indicator
**Solutions:**
- Use Roblox's **Print Screen** to capture screenshots at YOUR resolution
- Crop carefully - ONLY the indicator, not extra background
- Lower `POINT_CONFIDENCE` in config.py (try 0.55-0.60)
- Enable debug mode to see detection confidence scores
- Make sure fish are actually biting

---

## 🔧 Advanced Usage

### Debug Mode

Enable debug mode for detailed logging when running the macro. You'll be prompted:

```
Enable debug mode? (y/n): y
```

Debug output shows:
- Window capture status
- Detection confidence scores
- Click coordinates and timing
- Key press confirmations
- Input blocking status
- Eating schedule timing
- Catch type detection details

### Multiple Catch Type Detection

The macro automatically detects multiple catch types based on your `config.py`:

- **Fish** - Regular fish catches
- **Treasure** - Treasure chests
- **Sunken** - Sunken items
- **Junk** - Junk items
- **Caught** - Generic caught screen (fallback)

Each type:
- Has its own detection image in `assets/images/detection/`
- Has configurable confidence threshold
- Is tracked separately in catch statistics
- Appears in Discord notifications with catch breakdown

### Custom Window Title

If your Roblox window has a different title:

```python
window_capture = BackgroundWindowCapture("Your Custom Title")
```

---

## 📊 Statistics

The macro tracks and displays:

- **Total Detections:** How many times point.png was found
- **Total Clicks:** How many times it clicked
- **Eat Count:** How many times it ate food
- **Runtime:** How long the macro ran

Example output:
```
Fishing macro completed!
Total detections: 45
Total clicks: 3,250
Total meals: 15
```

---

## 🔐 Security & Safety

### What Gets Blocked

When `BlockInput()` is active:
- ✅ Your keyboard is disabled
- ✅ Your mouse is disabled
- ✅ Prevents you from interfering
- ⚠️ **Emergency stop (ESC/END) still works!**

### When Input is Blocked

1. **During fishing sequence** (when clicking on fish) - max 90 seconds
2. **During eating sequence** (pressing keys and clicking) - max 90 seconds

**CRITICAL SAFETY:** Input will automatically force-unblock after 90 seconds regardless of what's happening to prevent permanent lockout.

### When Input is Unblocked

1. **Between fishing attempts** (waiting for fish)
2. **After each sequence completes**
3. **On emergency stop (ESC/END key)**
4. **On script exit or crash**

---

## 📝 Technical Details

### Technologies Used

- **Python 3.8+**
- **OpenCV** - Image detection and template matching
- **NumPy** - Array operations
- **pywin32** - Windows API access
- **Pillow** - Image processing

### Windows APIs Used

- **PrintWindow** - Captures window in background
- **SendInput** - Hardware-level mouse clicking
- **keybd_event** - Hardware-level key pressing
- **BlockInput** - Blocks user input (requires admin)
- **GetAsyncKeyState** - Detects emergency stop keys
- **SetForegroundWindow** - Focuses window temporarily

### Why Window Focus is Required

**Q:** Why does it focus the window if it works in background?

**A:** Tested ALL 11 Windows input methods. Results:
- ❌ **SendMessage/PostMessage** (no focus) → Blocked by Roblox anti-cheat
- ✅ **keybd_event/SendInput** (needs focus) → Works with Roblox

**Current approach is optimal:**
- 95% runs in background (capture, detection, logic)
- 5% briefly focuses for input (0.05-0.1 seconds)
- Immediately restores previous window

See `INPUT_METHODS_REFERENCE.md` for full technical analysis.

---

## 📚 Additional Documentation

- **`docs/INPUT_METHODS_REFERENCE.md`** - Complete guide to all Windows input methods
- **`docs/ANSWER_BACKGROUND_INPUT.md`** - Why true background input is impossible
- **`docs/VALIDATION_RESULTS.md`** - Validation results and testing
- **`tests/test_all_input_methods.py`** - Test script for all 11 input methods
- **`tests/visual_input_test.py`** - Visual validation of which methods work
- **`tests/background_input_examples.py`** - Working examples for other apps

---

## ❓ FAQ

**Q: Will this get me banned from Roblox?**
A: Yes, likely. Using automation violates Roblox Terms of Service.

**Q: Will this get me banned in Arcane Odyssey?**
A: Yes, if caught. First offense = 3-day ban + 2 strikes. See rule 2.3 above.

**Q: Can I use this if I'm present at my computer?**
A: According to rule 2.3.1, if you are "present and able to respond to stimuli" it's permitted. However, fishing macro still automates a task requiring attention, which violates the rule's definition.

**Q: What if I only use it on an alt account?**
A: Alt accounts used exclusively for macroing = **permanent ban** (rule 2.3.2).

**Q: Can my inventory/fishing progress be wiped?**
A: Yes. Moderators can wipe your inventory and fishing journal (rule 2.3.5).

**Q: Can I run this on multiple accounts?**
A: Technically yes, but MUCH higher ban risk. Not recommended. Alt-only macroing = perma-ban.

**Q: Does this work for other Roblox games?**
A: With modifications, yes. You'd need different detection images.

**Q: Can I run this 24/7?**
A: Absolutely not. This violates rule 2.3.1 (requires attention). High ban risk.

**Q: Why does it briefly focus the window?**
A: Roblox anti-cheat blocks true background input. This is the best possible approach.

**Q: Can I disable eating?**
A: Yes, comment out the eating check in the main loop.

**Q: How do I stop the macro?**
A: Press **ESC** or **END** key at any time. Input will unblock immediately.

**Q: What's the 90-second timeout for?**
A: Critical safety feature. If something goes wrong, your input will NEVER be blocked for more than 90 seconds.

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs
- Suggest improvements
- Add new features
- Share better detection methods

---

## 📜 License

**Educational purposes only.** Use responsibly and at your own risk.

By using this software, you acknowledge that:
- Using automation violates both Roblox Terms of Service AND Arcane Odyssey in-game rules
- First macroing offense in Arcane Odyssey = 3-day ban + 2 strikes
- You may face inventory/fishing progress wipes (rule 2.3.5)
- Alt accounts used only for macroing will be permanently banned (rule 2.3.2)
- The author is not responsible for any consequences
- This is provided as-is with no warranties
- **You MUST be present and able to respond** to use within Arcane Odyssey rules (2.3.1)

**FINAL WARNING:** Even if you follow rule 2.3.1 by staying present, fishing macros are designed to automate tasks requiring attention, which fundamentally violates the rule. Use at your own risk of ban.

---

## 🎯 Credits

**🤖 100% AI Generated Project**
- Created entirely through AI-assisted development (GitHub Copilot)
- Human provided: Requirements, feature descriptions, and testing feedback
- AI provided: All code implementation, logic, technical decisions, AND this documentation
- **⚠️ Documentation Warning:** This README.md itself is AI-generated and may contain assumptions or errors
- Purpose: Educational demonstration of AI coding capabilities

**Technical Demonstrations:**
- Windows API usage in Python
- Computer vision with OpenCV
- Background window capture techniques
- Input simulation methods

**📖 Arcane Odyssey Rules Reference:** [Official Rulebook](https://docs.google.com/document/d/1oh7TLdW6aN6mAyk55BDF_ga-eMl_nHNECo2Bmqa71XA/edit?usp=sharing)

**Use wisely and responsibly!** 🎣
