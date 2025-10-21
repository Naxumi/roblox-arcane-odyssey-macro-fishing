# Roblox Arcane Odyssey - Background Fishing Macro

A sophisticated fishing automation script for Roblox Arcane Odyssey that works even when the game window is in the background. Features automatic fishing, hunger management, and emergency stop capabilities.

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
   .\install.bat
   ```
   
   This will:
   - Create a Python virtual environment (`.venv`)
   - Install all required dependencies
   - Set up the project automatically

   **Alternative manual installation:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

### Step 2: Prepare Detection Images

You need to create screenshot images that the macro will detect:

#### Required Images:

1. **`point.png`** - The fishing bite indicator
   - When a fish bites, a small indicator appears on screen
   - Take a screenshot of JUST that indicator
   - Save it as `point.png` in the project folder
   - **This is REQUIRED** for the macro to work

#### Optional Images:

2. **`hunger.png`** - Low hunger bar indicator (OPTIONAL)
   - ⚠️ **NOTE:** Random eating is now enabled by default (every 60-120 seconds)
   - This image is no longer required unless you want hunger-based eating
   - Take a screenshot of your hunger bar when it's at ≤35%
   - Save it as `hunger.png` in the project folder

3. **`caught.png`** or **`fish_caught.png`** - Fish caught indicator (OPTIONAL)
   - Screenshot of the "fish caught" message
   - Helps detect when fish is caught
   - Macro will work without this (uses timeout instead)

#### How to Take Screenshots:

1. Open Roblox Arcane Odyssey
2. Use Windows **Snipping Tool** (Win + Shift + S)
3. Capture the specific indicator you want
4. Save with exact filename in project folder

**Example file structure:**
```
roblox-arcane-odyssey-macro-fishing/
├── background_fishing_macro.py
├── point.png              ← REQUIRED
├── hunger.png             ← OPTIONAL (not used with random eating)
├── caught.png             ← OPTIONAL
├── requirements.txt
├── install.bat
└── README.md
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
9. Restore Mouse Position ───────────────> Back to original spot �️
        ↓
10. Restore Previous Window ─────────────> Back to what you were doing ✅
        ↓
11. Check if time to eat ────────────────> Random 60-120s interval 🍖
        ↓
12. Repeat from step 1
```

### The Eating Cycle (Every 60-120 seconds)

```
1. Check Timer ───────────────────────────> Time elapsed? ⏱️
        ↓
2. [TIME TO EAT] Block Input ─────────────> Prevent interference 🔒
        ↓
3. Focus Window ──────────────────────────> Required for keypresses ⚠️
        ↓
4. Press '0' key ─────────────────────────> Select food slot 🍖
        ↓
5. Click 3 times (0.8s delay each) ───────> Consume 3 food items
        ↓
6. Wait 1 second ─────────────────────────> Let animation finish
        ↓
7. Press '9' key ─────────────────────────> Select fishing rod 🎣
        ↓
8. Click once ────────────────────────────> Cast rod
        ↓
9. Unblock Input ─────────────────────────> Restore control 🔓
        ↓
10. Schedule Next Meal ───────────────────> Random 60-120s later
```

---

## ⚙️ Configuration

### Basic Settings

Edit these in `background_fishing_macro.py`:

```python
# Detection confidence (0.0 - 1.0)
point_detector = ImageDetector('point.png', confidence=0.55)

# Auto-cast timeout (seconds)
no_detection_timeout = 70

# Eating interval (seconds)
next_eat_interval = random.randint(60, 120)  # Random between 1-2 minutes
```

### Advanced Settings

```python
# Click patterns (optimized for rare/golden/massive fish)
# First 150 clicks: 0.012s delay = ~83 clicks/second
# After 150 clicks: 0.015s delay = ~66 clicks/second

# Maximum clicking duration with safety timeouts
if click_duration > 40:   # Normal timeout (40 seconds)
    break
if click_duration > 84:   # Safety timeout (84 seconds)
    break
if input_block_duration > 90:  # CRITICAL force-unblock (90 seconds)
    force_unblock_and_exit()

# Minimum clicks guarantee (handles rare fish)
if clicks_in_loop < 150:  # Always do at least 150 clicks
    continue

# All clicks happen at screen center
center_x = w // 2
center_y = h // 2
```

---

## 🎮 Inventory Setup

For the macro to work properly, set up your inventory:

- **Slot 0:** Food items (any food for hunger)
- **Slot 9:** Fishing rod
- **Other slots:** Whatever you want

The macro will:
1. Press **'0'** to select food
2. Click **3 times** to consume food
3. Press **'9'** to re-equip fishing rod
4. Click **once** to cast

---

## 🐛 Troubleshooting

### Common Issues

#### "Window 'Roblox' not found"
**Problem:** Script can't find Roblox window
**Solutions:**
- Make sure Roblox is running
- Check window title is exactly "Roblox"
- Try running in-game (not in menu)

#### "Template image not found: point.png"
**Problem:** Missing required screenshot
**Solutions:**
- Create `point.png` screenshot of fishing bite indicator
- Place in same folder as script
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

#### Keypresses not working (0 and 9)
**Problem:** Food/rod not selected
**Solutions:**
- Script must briefly focus window (this is normal)
- Make sure slots 0 and 9 have items
- Check items are actually in those slots
- Debug mode shows if keys are being pressed

#### No detections / Not clicking
**Problem:** Macro doesn't detect fishing indicator
**Solutions:**
- Lower confidence: `confidence=0.4` instead of `0.55`
- Retake `point.png` at current resolution
- Enable debug mode to see detection confidence
- Make sure fish are actually biting

---

## 🔧 Advanced Usage

### Debug Mode

Enable debug mode for detailed logging:

```powershell
python background_fishing_macro.py
# When prompted for debug mode, enter: y
```

Debug output shows:
- Window capture status
- Detection confidence scores
- Click coordinates and timing
- Key press confirmations
- Input blocking status
- Eating schedule timing

### Multiple Detection Images

The macro supports multiple "caught" indicators:

```python
caught_images = [
    ('caught.png', 0.35),
    ('fish_caught.png', 0.35),
    ('treasure_caught.png', 0.35),
]
```

Add more images if you catch different types:
- Regular fish
- Treasure chests
- Special catches

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

- **`INPUT_METHODS_REFERENCE.md`** - Complete guide to all Windows input methods
- **`ANSWER_BACKGROUND_INPUT.md`** - Why true background input is impossible
- **`test_all_input_methods.py`** - Test script for all 11 input methods
- **`visual_input_test.py`** - Visual validation of which methods work
- **`background_input_examples.py`** - Working examples for other apps

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
