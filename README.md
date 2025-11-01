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
   .\scripts\install.bat
   ```

   This will:
   - Check Python installation
   - Create a virtual environment (`.venv`)
   - Activate the virtual environment
   - Install required packages in the venv
   
   Or install manually:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Step 2: Configuration

**⚠️ IMPORTANT: Always activate the virtual environment first!**
```powershell
.venv\Scripts\activate
```

**Option A: Quick Setup (Recommended)**
```powershell
python setup_wizard.py
```

The wizard will guide you through:
- Discord webhook setup (optional)
- Detection sensitivity configuration
- Combat detection and auto-kill options (instant vs delayed)
- Kill delay customization (if delayed mode selected)
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

**OPTIONAL: Combat Detection (`combat_arcane_odyssey.png`)**

For AFK safety and combat alerts:
1. Get into combat or find a combat indicator screenshot
2. Press **Print Screen** when the combat indicator is visible
3. Crop ONLY the combat indicator from the screenshot
4. Save as `assets/images/detection/combat_arcane_odyssey.png`
5. Configure combat detection settings in `config.py`

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

3. **Activate the virtual environment:**
   ```powershell
   .venv\Scripts\activate
   ```
   
   You should see `(.venv)` appear at the start of your prompt.

4. **Run the macro:**
   ```powershell
   python background_fishing_macro.py
   ```

5. **Follow the prompts:**
   - Enter Discord webhook URL (or press Enter to use config default)
   - Enter duration in seconds (e.g., 3600 for 1 hour)
   - Enter number of food items per eating session (or press Enter for default from config)
   - Enter eating interval (or press Enter for default from config)
   - Enable debug mode (y/n) - shows detailed information

6. **🎮 HOTKEYS:**
   - **Ctrl+Alt+M** - Emergency stop (exits program immediately)
   - **Ctrl+,** - Pause script (temporary pause, can resume)
   - **Ctrl+.** - Resume script (continues fishing)

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
- ✅ **Pause/Resume Control** - Press Ctrl+, to pause, Ctrl+. to resume (Discord notifications included)
- ✅ **Emergency Stop** - Press Ctrl+Alt+M to stop immediately and unblock input
- ✅ **Mouse Position Restoration** - Returns mouse to original position after fishing

### Eating System
- ✅ **User-Configurable Schedule** - Set eating count and interval
- ✅ **Continuous Eating** - Configurable N food items per session, continuously throughout macro runtime
- ✅ **Smart Eating Logic** - Doesn't eat while actively fishing
- ✅ **Auto Re-equip** - Automatically re-equips fishing rod after eating
- ✅ **Configurable Slots** - Change food/rod slots in config.py

### Discord Integration
- ✅ **Catch Notifications** - Get notified on Discord when fish are caught
- ✅ **Screenshot Attachments** - Sends actual game screenshot with notification
- ✅ **Video Attachments** - Records and sends 5-second MP4 videos when fishing issues detected
- ✅ **Catch Statistics** - Shows total catches, catch breakdown by type
- ✅ **Session Info** - Displays session duration, time since last meal, clicks
- ✅ **Auto-cleanup** - Optionally deletes screenshots/videos after sending to save storage
- ✅ **@Mention Support** - Tag yourself in Discord notifications for important alerts
- ✅ **Sunken Item Alerts** - Automatic @mention when rare sunken items are caught (most valuable catches)
- ✅ **Combat Alerts** - Sends 3 urgent @mention messages when combat detected
- ✅ **Auto-Cast Alerts** - Notifies every auto-cast occurrence with milestone alerts every 5th cast
- ✅ **Runtime Webhook Override** - Prompt at startup to use custom webhook URL without editing config

### Combat Detection System (AFK Safety)
- ✅ **Background Monitoring** - Continuously checks for combat indicator every 2 seconds
- ✅ **Triple Message Spam** - Sends 3 separate @mention Discord alerts for maximum urgency
- ✅ **Fresh Screenshots** - Captures and sends NEW screenshot with EACH of the 3 messages for real-time updates
- ✅ **Automatic Macro Pause** - Stops fishing and eating activities when combat detected (resumes when cleared)
- ✅ **Random WASD Movement** - Simulates human evasion during combat to avoid appearing AFK
- ✅ **10-Second Grace Period** - Countdown timer before taking action
- ✅ **Optional Auto-Kill** - Can automatically close Roblox process after grace period

### Auto-Cast Detection & Safety
- ✅ **Every-Time Notifications** - Discord notification sent for every auto-cast occurrence
- ✅ **Consecutive Detection Counter** - Tracks consecutive auto-casts without catching anything
- ✅ **Smart Auto-Pause** - Script pauses after 5 consecutive no-detections (resets on any catch)
- ✅ **Progress Indicators** - Shows "Consecutive: 3/5" in console and Discord to track toward threshold
- ✅ **Milestone Alerts** - Special @mention alerts when 5 consecutive failures reached
- ✅ **Resume Instructions** - Console and Discord notifications display clear instructions to press Ctrl+. to resume
- ✅ **Screenshot Attachments** - Sends game screenshot with each auto-cast notification
- ✅ **Session Statistics** - Shows consecutive count, total auto-cast count, session duration, total catches in alerts

### Video Recording System
- ✅ **Automatic Recording** - Records 5-second MP4 videos when fishing detection issues occur
- ✅ **H.264 Compression** - Efficient compression (1-3MB per 5s video at 15 FPS)
- ✅ **Non-Blocking Threads** - Records in background without affecting fishing performance
- ✅ **Discord Upload** - Automatically uploads videos to Discord webhook (30s timeout)
- ✅ **Configurable Settings** - Customize duration (1-30s), FPS (5-60), quality (CRF 0-51)
- ✅ **Auto-Cleanup** - Optionally deletes videos after Discord upload to save storage
- ✅ **Screenshot Fallback** - Falls back to screenshot if video recording fails

### Catch-Specific Alerts
- ✅ **Sunken Item @Mentions** - Automatically mentions you when rare sunken items are caught
- ✅ **Priority Notifications** - Sunken items get special alert status (most valuable loot)
- ✅ **Catch Type Detection** - Distinguishes between fish, treasure, sunken items, and junk
- ✅ **Separate Statistics** - Tracks each catch type independently for detailed analytics
- ✅ **Discord Embeds** - Rich embeds with catch type, confidence, and session stats

### Safety Features
- ✅ **Configurable Safety Timeout** - Force-unblocks input after configured time (default: 90s)
- ✅ **Configurable Click Timeout** - Stops clicking after configured duration (default: 20s)
- ✅ **Input Unblocking** - Always unblocks input even if script crashes
- ✅ **Window Restoration** - Returns focus to your previous window after actions
- ✅ **Mouse Position Restore** - Returns cursor to original position
- ✅ **Pause/Resume System** - Temporarily pause script without exiting (Ctrl+, / Ctrl+.)
- ✅ **Emergency Stop** - Works even when input is blocked (requires admin)
- ✅ **Try-Finally Blocks** - Ensures cleanup always happens

### Control Features
- ✅ **Pause Script** - Press Ctrl+, to temporarily pause fishing and eating
- ✅ **Resume Script** - Press Ctrl+. to continue from where you paused
- ✅ **Discord Pause Notifications** - Get notified on Discord when script pauses (yellow embed)
- ✅ **Discord Resume Notifications** - Get notified on Discord when script resumes (green embed)
- ✅ **Periodic Pause Updates** - Sends screenshot every 60 seconds while paused with session statistics
- ✅ **Remote Monitoring** - See game state and progress while script is paused via Discord
- ✅ **Non-Destructive Pause** - Pausing doesn't exit the program, just suspends activities
- ✅ **Combined with Combat** - Works alongside combat detection system

### Advanced Features
- ✅ **Template Matching** - OpenCV-based image detection
- ✅ **Adjustable Confidence** - Configure detection sensitivity in config.py
- ✅ **Multiple Catch Types** - Detects fish, treasure, sunken items, junk separately
- ✅ **Parallel Detection** - Separate thread for detection while clicking
- ✅ **Resolution-Independent** - Works with custom screenshots at any resolution
- ✅ **Setup Wizard** - Interactive configuration tool for first-time setup
- ✅ **Process Management** - Can terminate Roblox process when combat detected (optional)

---

## ⚙️ Configuration

### Configuration File (`config.py`)

All settings are in `config.py`. Copy from `config.example.py` to get started.

#### Discord Settings
```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
ENABLE_DISCORD_NOTIFICATIONS = True
DISCORD_MENTION_USER_ID = ""  # Your Discord User ID for @mentions
MENTION_ON_COMBAT_DETECTED = True  # Mention you when combat detected
MENTION_ON_AUTO_KILL = True  # Mention you when Roblox auto-killed
```

**@Mention Behavior:**
- **Sunken Items**: Always mentions you (most valuable/rare catches)
- **Combat Detection**: Mentions you if `MENTION_ON_COMBAT_DETECTED = True`
- **Auto-Cast Milestones**: Mentions you every 5th auto-cast (5, 10, 15, 20...)
- **Auto-Kill**: Mentions you if `MENTION_ON_AUTO_KILL = True` and Roblox is closed

**Getting Your Discord User ID:**
1. Enable Developer Mode: User Settings > Advanced > Developer Mode
2. Right-click your profile anywhere in Discord
3. Click "Copy User ID"
4. Paste into `DISCORD_MENTION_USER_ID` in config.py

#### Combat Detection Settings
```python
ENABLE_COMBAT_DETECTION = True  # Enable combat monitoring
COMBAT_CONFIDENCE = 0.70  # Combat indicator detection threshold
COMBAT_AUTO_KILL_ROBLOX = False  # Kill Roblox on combat (default: disabled)
COMBAT_INSTANT_KILL = False  # Instant kill without delay (default: disabled)
COMBAT_KILL_DELAY = 10  # Seconds before killing process (ignored if instant kill enabled)
```

**How Combat Detection Works:**
1. Background thread continuously monitors for `combat_arcane_odyssey.png`
2. If detected: 
   - Captures fresh screenshot #1 → Sends Discord message #1 with screenshot
   - Captures fresh screenshot #2 → Sends Discord message #2 with screenshot  
   - Captures fresh screenshot #3 → Sends Discord message #3 with screenshot
   - Sets `combat_active` flag to pause fishing and eating
   - Starts random WASD movement thread (simulates evasion)
3. During combat: Randomly presses W/A/S/D keys (0.3-1.2s hold, 0.5-2.0s intervals)
4. **Kill Options:**
   - **Instant Kill** (`COMBAT_INSTANT_KILL = True`): Closes Roblox **immediately** with no delay
   - **Delayed Kill** (`COMBAT_INSTANT_KILL = False`): Waits configured delay (default 10s) before closing
   - **No Kill** (`COMBAT_AUTO_KILL_ROBLOX = False`): Notifications only, game stays open
5. If combat clears naturally: Clears flag, resumes fishing/eating, stops movement

**⚠️ SAFETY:** 
- Auto-kill is **disabled by default** to prevent accidental game closures
- Instant kill is **disabled by default** for maximum safety
- Configure kill delay in setup wizard or config.py (1-999 seconds)

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
DEFAULT_EATING_COUNT = 3      # Default: eat 3 food items per session
FOOD_SLOT_KEY = 0x30          # Slot 0 for food
ROD_SLOT_KEY = 0x39           # Slot 9 for rod
```

**Note:** The macro eats a configurable number of food items (default 3) per eating session, and will continue eating at the configured interval throughout the entire fishing duration to prevent death from hunger.

#### Safety Settings
```python
CRITICAL_SAFETY_TIMEOUT = 90  # Force unblock after 90s
```

#### Screenshot Settings
```python
SAVE_DETECTION_SCREENSHOTS = True   # Save screenshots
DELETE_SCREENSHOTS_AFTER_DISCORD = True  # Delete after sending
```

#### Video Recording Settings
```python
RECORD_DETECTION_VIDEO = True  # Enable video recording for fishing issues
VIDEO_DURATION = 5  # Seconds to record (1-30s)
VIDEO_FPS = 15  # Frames per second (5-60 FPS)
VIDEO_QUALITY = 23  # H.264 CRF quality (0-51, lower=better)
DELETE_VIDEOS_AFTER_DISCORD = True  # Delete videos after Discord upload
```

**Video Quality Guide:**
- **CRF 18**: High quality, larger files (~3-5MB per 5s)
- **CRF 23**: Balanced quality/size (~1-3MB per 5s) [RECOMMENDED]
- **CRF 28**: Lower quality, smaller files (~0.5-1.5MB per 5s)

**FPS Guide:**
- **10 FPS**: Lower quality, smallest files
- **15 FPS**: Smooth, good balance [RECOMMENDED]
- **30 FPS**: Very smooth, larger files

### Runtime Webhook Override

At startup, the macro prompts you to enter a Discord webhook URL:
- **Press Enter** - Uses the webhook from `config.py` (default)
- **Paste a URL** - Uses the custom webhook for this session only

**Use Cases:**
- Testing with a different Discord channel without editing config
- Using different webhooks for different fishing sessions
- Temporary override for testing notifications
- Quick webhook changes without reconfiguration

**Note:** Pause/resume hotkey notifications always use the webhook from `config.py` (global scope limitation).

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

### Pause/Resume System

The pause/resume feature provides temporary control without exiting the program:

**How Pause Works (Ctrl+,):**
1. Keyboard hook detects Ctrl+, combination
2. Sets global `script_paused` flag to `True`
3. Sends initial yellow Discord notification (color: 16776960)
4. Main loop checks flag at start of each iteration
5. While paused: Skips fishing detection, clicking, and eating
6. **Periodic Updates**: Every 60 seconds, sends screenshot with statistics to Discord
7. Sleeps for 1 second per iteration to reduce CPU usage
8. Debug output shows "Script paused - waiting..." if enabled

**Periodic Pause Status Updates (Every 60s):**
- Captures fresh screenshot of game window
- Sends to Discord with yellow embed titled "⏸️ Script Still Paused - Status Update"
- **Statistics Included:**
  - Session Duration (how long macro has been running)
  - Total Catches (number of fish caught)
  - Total Detections (point detection count)
  - Auto-Cast Count (total auto-casts)
  - Consecutive No-Detections (progress toward auto-pause: X/5)
- Screenshot auto-deleted after sending (if configured)
- Helps you monitor game state remotely while paused

**How Resume Works (Ctrl+.):**
1. Keyboard hook detects Ctrl+. combination
2. Sets global `script_paused` flag to `False`
3. Sends green Discord notification (color: 5763719)
4. Main loop resumes normal fishing and eating operations
5. Debug output shows "Script resumed" if enabled

**Auto-Pause on Consecutive No-Detections:**
- Script automatically pauses when **5 consecutive auto-casts** occur without catching anything
- Counter increments on each auto-cast, **resets to 0** on every successful catch
- Displays "Consecutive: X/5" in console and Discord notifications to track progress
- Sends urgent Discord notification with @mention when threshold reached
- Displays clear console message with resume instructions
- Prevents wasting time if detection is failing or wrong fishing location
- Must press **Ctrl+.** to resume after investigating the issue
- **Smarter than total count**: Won't pause if you're catching fish between auto-casts

**Integration with Other Systems:**
- Works alongside combat detection (both can pause script)
- Doesn't interfere with emergency stop (Ctrl+Alt+M)
- Respects all safety timeouts and input blocking
- Discord notifications keep you informed of script state

**Use Cases:**
- Taking a break without stopping the entire program
- Responding to in-game chat or events
- Checking inventory or adjusting position
- Testing if script is causing issues
- Remote monitoring via Discord notifications
- Investigating why auto-cast is happening repeatedly
- **Remote oversight**: See game state every 60s without being at computer
- **Progress tracking**: Check statistics while paused to decide if resume needed
- **Safety checks**: Verify character position and surroundings via screenshots

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

### Pause/resume hotkeys not working
**Problem:** Ctrl+, or Ctrl+. doesn't pause/resume the script
**Solutions:**
- **Run PowerShell as Administrator** (required for keyboard hooks)
- Check if Ctrl key is working properly on your keyboard
- Make sure you're pressing the comma (,) and period (.) keys, not < or >
- Enable debug mode to see if keypresses are being detected
- Check console output for "Script paused" or "Script resumed" messages

### Script won't resume after pausing
**Problem:** Pressed Ctrl+. but script still paused
**Solutions:**
- Try pressing Ctrl+. again (may need to register)
- Check Discord for resume notification to confirm it worked
- Enable debug mode to see current pause state
- Check console shows "Script resumed" message
- As last resort, use Ctrl+Alt+M emergency stop and restart

### Pause notification not appearing in Discord
**Problem:** Script pauses but no Discord notification
**Solutions:**
- Verify `ENABLE_DISCORD_NOTIFICATIONS = True` in config.py
- Check Discord webhook URL is correct
- Test webhook with a catch notification first
- Check console for "Discord notification sent" messages
- Webhook may be rate-limited (small delay between messages)

### Combat detection behavior
- **Fresh screenshots**: Each of the 3 Discord messages gets a newly captured screenshot for real-time updates
- **Macro pausing**: Fishing and eating automatically stop when combat detected, resume when cleared
- **Random movement**: WASD keys pressed randomly (0.3-1.2s hold, 0.5-2.0s intervals) to simulate human evasion
- **Movement stops**: Random movement automatically stops when combat clears
- **Debug logs**: Enable debug mode to see detailed movement actions (which keys, durations)

### Auto-pause after consecutive no-detections
**Problem:** Script auto-paused after 5 consecutive auto-casts without catching anything
**This is intentional!** The script auto-pauses to alert you of potential issues:

**How the consecutive counter works:**
- Counter increments by 1 each time auto-cast happens (no fish bite detected)
- Counter **resets to 0** whenever a fish is successfully caught
- Script auto-pauses when counter reaches **5 consecutive failures**
- This means: 5 auto-casts in a row without catching anything

**Example scenarios:**
- ✅ **Won't pause:** Auto-cast → Catch → Auto-cast → Catch → Auto-cast → Catch (counter keeps resetting)
- ❌ **Will pause:** Auto-cast → Auto-cast → Auto-cast → Auto-cast → Auto-cast (5 consecutive, counter reaches 5)
- ✅ **Won't pause:** Auto-cast → Auto-cast → Auto-cast → Catch → Auto-cast → Auto-cast (counter reset by catch)

**Console output example:**
```
[AUTO-CAST] No detection for 60s. Casting rod... (Auto-cast #3, Consecutive: 1/5)
[AUTO-CAST] No detection for 60s. Casting rod... (Auto-cast #4, Consecutive: 2/5)
[CAUGHT] Fish caught! (Counter resets to 0)
[AUTO-CAST] No detection for 60s. Casting rod... (Auto-cast #5, Consecutive: 1/5)
[AUTO-CAST] No detection for 60s. Casting rod... (Auto-cast #6, Consecutive: 2/5)
[AUTO-CAST] No detection for 60s. Casting rod... (Auto-cast #7, Consecutive: 3/5)
[AUTO-CAST] No detection for 60s. Casting rod... (Auto-cast #8, Consecutive: 4/5)
[AUTO-CAST] No detection for 60s. Casting rod... (Auto-cast #9, Consecutive: 5/5)
🚨 ALERT: 5 consecutive no-detections - triggering auto-pause
⏸️  SCRIPT AUTO-PAUSED
```

**Why it pauses:**
- 5 consecutive failures suggests something is wrong
- Could indicate wrong fishing location, bad detection images, or game issues
- Prevents wasting hours fishing in the wrong spot
- Smarter than pausing every 5th auto-cast regardless of catches

**What to check when paused:**
1. Are you in the correct fishing location?
2. Are detection images matching your game resolution?
3. Is the fishing bite indicator actually appearing?
4. Check `POINT_CONFIDENCE` - may need adjustment
5. Look at the Discord screenshot to see what game looks like

**How to continue:**
- Press **Ctrl+.** to resume if everything looks correct
- Counter will continue from current value
- Catching a fish will reset the counter back to 0
- Or press **Ctrl+Alt+M** to emergency stop and investigate further

### Video recording not working
**Problem:** Videos not being created or uploaded to Discord
**Solutions:**
- Check `RECORD_DETECTION_VIDEO = True` in config.py
- Ensure OpenCV is installed: `pip install opencv-python`
- Videos only record when detection **issues** occur (timeout or low confidence)
- Check screenshot folder for .mp4 files
- Enable debug mode to see video recording status
- Increase `VIDEO_DURATION` if videos seem too short

### Runtime webhook override not working
**Problem:** Custom webhook URL not being used
**Solutions:**
- Make sure you pasted the full webhook URL at startup prompt
- Verify the URL starts with `https://discord.com/api/webhooks/`
- Check console output confirms "Using custom webhook"
- Test the webhook manually to ensure it's valid
- Note: Pause/resume notifications always use config webhook (limitation)

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
│   │       ├── caught_arcane_odyssey.png
│   │       └── combat_arcane_odyssey.png  # Combat indicator (OPTIONAL)
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

# Run installation script (creates venv and installs dependencies)
.\scripts\install.bat

# OR manually:
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your config
copy config.example.py config.py
# Edit config.py with your settings

# Run (always activate venv first!)
.venv\Scripts\activate
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

**Q: What's the difference between pause and emergency stop?**
A: 
- **Pause (Ctrl+,)**: Temporarily suspends fishing and eating, but keeps program running. Use when you need to step away briefly.
- **Emergency Stop (Ctrl+Alt+M)**: Completely exits the program and unblocks input immediately. Use for emergencies or when done fishing.

**Q: Can I resume the macro after pausing?**
A: Yes! Press Ctrl+. to resume. The macro will continue fishing and eating from where it left off.

**Q: Do I get Discord notifications when I pause/resume?**
A: Yes! Pausing sends a yellow Discord notification, resuming sends a green notification. This helps you track script state remotely.

**Q: What happens when the script is paused?**
A: The macro stops all activities (fishing detection, clicking, eating) and enters a waiting state. It checks every second if you've resumed.

**Q: Can I pause while combat detection is active?**
A: Yes! The pause system works independently. You can pause even during combat, and both systems will coordinate properly.

**Q: What's the difference between total auto-cast count and consecutive no-detections?**
A:
- **Total Auto-Cast Count**: Total number of times the script auto-cast throughout the entire session (never resets)
- **Consecutive No-Detections**: Number of auto-casts in a row without catching anything (resets to 0 on each catch)
- Example: If you have 20 total auto-casts but caught fish between them, consecutive count stays low
- Auto-pause triggers at **5 consecutive**, not 5 total

**Q: Why did my script auto-pause when I'm catching fish?**
A: The script only pauses after **5 consecutive no-detections** (5 auto-casts in a row without catching). If you're catching fish between auto-casts, the counter resets and won't trigger auto-pause. Check the console output for "Consecutive: X/5" to track the counter.

**Q: Can I change the consecutive no-detection threshold?**
A: Currently it's hardcoded to 5. You can modify the code by changing `if self.consecutive_no_detection >= 5` to a different number in the auto-cast section.

**Q: How often are periodic pause screenshots sent to Discord?**
A: By default, screenshots are sent every 60 seconds while the script is paused. This includes the current game view and session statistics (catches, detections, auto-cast count, consecutive no-detections). This helps you monitor the game remotely without being at your computer.

**Q: Can I disable the periodic pause screenshots?**
A: Currently the feature is always enabled when Discord notifications are active. You can modify the code by commenting out the periodic screenshot section in the pause loop if desired.

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
- ✅ **Statistics Tracking** - Total detections, clicks, eating sessions

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
5. Click N times (0.8s delay each) ──────> Consume N food items per session (configurable)
        ↓
6. Wait 1 second ─────────────────────────> Let animation finish
        ↓
7. Press configured rod key ──────────────> Select fishing rod (default: '9') 🎣
        ↓
8. Click once ────────────────────────────> Cast rod
        ↓
9. Unblock Input ─────────────────────────> Restore control 🔓
        ↓
10. Schedule Next Meal ───────────────────> Based on config interval (repeats indefinitely)
```

**Note:** The macro will continue eating at the configured interval throughout the entire fishing session to prevent death from hunger.

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

#### Combat detection not working
**Problem:** Combat alerts not triggering
**Solutions:**
- Make sure `combat_arcane_odyssey.png` exists in detection folder
- Use Roblox's **Print Screen** to capture combat indicator at YOUR resolution
- Verify `ENABLE_COMBAT_DETECTION = True` in config.py
- Check `DISCORD_MENTION_USER_ID` is set for @mentions
- Lower `COMBAT_CONFIDENCE` if needed (try 0.60-0.65)
- Enable debug mode to see if combat thread is running

#### Not receiving 3 Discord messages
**Problem:** Only getting 1 combat message instead of 3
**Solutions:**
- Check Discord webhook URL is correct
- Verify `ENABLE_DISCORD_NOTIFICATIONS = True`
- Check `MENTION_ON_COMBAT_DETECTED = True`
- Webhook may be rate-limited by Discord (small delay between messages)
- Check console for "Sent 3 urgent Discord notifications!" message

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
- Combat detection thread status

### Combat Detection System

The combat detection system runs independently in a background thread:

**How it works:**
1. Monitors for `combat_arcane_odyssey.png` every 2 seconds
2. First detection triggers **3 separate Discord messages** with @mention
3. **Each message gets a freshly captured screenshot** for real-time updates
4. **Fishing and eating activities automatically pause** when combat detected
5. **Random WASD movement starts** to simulate human evasion (appears less AFK)
6. 10-second countdown begins
7. If `COMBAT_AUTO_KILL_ROBLOX = True`, Roblox process is terminated after countdown
8. If combat clears naturally, timer resets and **fishing/eating resume**

**Discord notification format:**
```
Message 1: @YourName + ⚔️🚨 COMBAT DETECTED! 🚨⚔️ (Alert 1/3) + fresh screenshot #1
Message 2: @YourName + ⚔️🚨 COMBAT DETECTED! 🚨⚔️ (Alert 2/3) + fresh screenshot #2
Message 3: @YourName + ⚔️🚨 COMBAT DETECTED! 🚨⚔️ (Alert 3/3) + fresh screenshot #3
```

**Random Movement Behavior:**
- Randomly selects W, A, S, or D keys
- Holds each key for 0.3-1.2 seconds (randomized)
- Pauses 0.5-2.0 seconds between movements (randomized)
- Continues until combat clears
- Makes bot appear like player trying to evade/escape

**Configuration:**
- `COMBAT_AUTO_KILL_ROBLOX` - Enable/disable auto-kill (default: False)
- `COMBAT_KILL_DELAY` - Seconds before killing (default: 10)
- `COMBAT_CONFIDENCE` - Detection sensitivity (default: 0.70)
- `MENTION_ON_COMBAT_DETECTED` - Enable @mentions for combat (default: True)

**Getting your Discord User ID:**
1. Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
2. Right-click your profile anywhere
3. Click "Copy User ID"
4. Paste into `DISCORD_MENTION_USER_ID` in config.py

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
- **Combat Detections:** How many times combat was detected
- **Runtime:** How long the macro ran

Example output:
```
Fishing macro completed!
Total detections: 45
Total clicks: 3,250
Total meals: 15
Combat detections: 2
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
- **psutil** - Process management (combat auto-kill feature)
- **requests** - Discord webhook notifications

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
A: Press **Ctrl+Alt+M** at any time. Input will unblock immediately.

**Q: What's the combat detection for?**
A: AFK safety feature. If someone attacks you while fishing, you get 3 urgent Discord @mentions with fresh screenshots. The macro automatically pauses fishing/eating and moves randomly (W/A/S/D) to simulate human evasion. Optionally can auto-close Roblox after 10 seconds.

**Q: Will the macro spam me with Discord notifications?**
A: Only when important events happen (catches, combat, eating). Combat triggers 3 messages for urgency, each with a fresh screenshot.

**Q: How do I get my Discord User ID?**
A: Enable Developer Mode in Discord (User Settings > Advanced), right-click your profile, "Copy User ID".

**Q: Does combat auto-kill close Roblox immediately?**
A: No, 10-second grace period. If combat clears, timer resets. Default is disabled (notifications only).

**Q: Can I disable combat detection?**
A: Yes, set `ENABLE_COMBAT_DETECTION = False` in config.py.

**Q: Why does combat send 3 screenshots instead of 1?**
A: Each screenshot is freshly captured at the moment of sending, giving you real-time visual updates of the combat situation. This helps you see if the threat is escalating or if you need to act immediately.

**Q: Why does the macro move WASD during combat?**
A: To simulate human evasion behavior and avoid appearing as an AFK bot. The random movements (0.3-1.2s holds with 0.5-2.0s intervals) make it look like a player trying to escape combat.

**Q: What is instant kill mode?**
A: When `COMBAT_INSTANT_KILL = True`, Roblox closes **immediately** when combat is detected with no delay. This is the fastest response option but gives you no time to react manually.

**Q: Can I change the 10-second kill delay?**
A: Yes! The kill delay is configurable. Set it in the setup wizard or change `COMBAT_KILL_DELAY` in config.py (1-999 seconds). Note: This is ignored if instant kill mode is enabled.

**Q: When should I use instant kill vs delayed kill?**
A: 
- **Instant kill**: Best for high-risk areas where every second counts. No delay means no chance for damage.
- **Delayed kill**: Safer option that gives you time to assess if the combat warning is legitimate before Roblox closes. Recommended for beginners.
- **No kill**: Just notifications, no automatic closure. You handle combat manually.

**Q: What happens if I don't set Discord User ID?**
A: Discord notifications work but won't @mention you (less noticeable).

**Q: What's the 90-second timeout for?**
A: Critical safety feature. If something goes wrong, your input will NEVER be blocked for more than 90 seconds.

---
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
