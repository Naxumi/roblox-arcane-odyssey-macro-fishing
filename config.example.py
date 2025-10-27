"""
EXAMPLE Configuration file for Roblox Arcane Odyssey Fishing Macro
Copy this file to config.py and edit your settings:
    cp config.example.py config.py

This file is included in the repository as a template.
Your actual config.py will be ignored by git to protect your webhook URL.
"""

# ============================================
# DISCORD WEBHOOK SETTINGS
# ============================================
# Get your webhook URL from Discord:
# Server Settings > Integrations > Webhooks > New Webhook > Copy Webhook URL
DISCORD_WEBHOOK_URL = ""  # PASTE YOUR WEBHOOK URL HERE

# Enable/disable Discord notifications
ENABLE_DISCORD_NOTIFICATIONS = True  # Set to False to disable all Discord notifications


# ============================================
# DETECTION SETTINGS
# ============================================
# Confidence thresholds (0.0 to 1.0) - lower = more sensitive, higher = more accurate
# ⚠️ IMPORTANT: These values are HIGHLY dependent on your monitor resolution and game settings!
# If detection is not working, you MUST adjust these values and retake screenshots at YOUR resolution.

POINT_CONFIDENCE = 0.65  # Fishing bite indicator detection
FISH_CONFIDENCE = 0.75   # Fish caught detection
TREASURE_CONFIDENCE = 0.75  # Treasure caught detection
SUNKEN_CONFIDENCE = 0.75  # Sunken item detection
JUNK_CONFIDENCE = 0.75  # Junk caught detection
CAUGHT_CONFIDENCE = 0.75  # Generic "caught" screen detection

# Detection image paths (relative to project root)
# ⚠️ IMPORTANT: Provided images may not work for your resolution!
# You may need to retake these screenshots at YOUR game resolution for best results.
DETECTION_IMAGES = {
    'point': 'assets/images/detection/point.png',  # REQUIRED - fishing bite indicator
    'fish': 'assets/images/detection/fish_arcane_odyssey.png',
    'treasure': 'assets/images/detection/treasure_arcane_odyssey.png',
    'sunken': 'assets/images/detection/sunken_arcane_odyssey.png',
    'junk': 'assets/images/detection/junk_arcane_odyssey.png',
    'caught': 'assets/images/detection/caught_arcane_odyssey.png',
    'hunger': 'assets/images/detection/hunger.png',  # Optional - hunger bar
}


# ============================================
# TIMING SETTINGS
# ============================================
# How long to click when fish bites (seconds)
MAX_CLICKING_DURATION = 20  # Stop clicking after this many seconds

# How long to wait before auto-casting rod if no fish bite (seconds)
NO_DETECTION_TIMEOUT = 60  # Auto-cast rod after this many seconds of no detection

# Click speed (seconds between clicks)
CLICK_DELAY = 0.001  # 0.001 = ~1000 clicks/sec theoretical max


# ============================================
# EATING SETTINGS
# ============================================
# These are default values - you'll be prompted to set them when running the script
DEFAULT_EATING_INTERVAL = 300  # Default: eat every 300 seconds (5 minutes)
DEFAULT_EATING_COUNT = 3  # Default: eat 3 times per session

# Inventory slots
FOOD_SLOT_KEY = 0x30  # Key code for slot 0 (food)
ROD_SLOT_KEY = 0x39   # Key code for slot 9 (fishing rod)


# ============================================
# WINDOW SETTINGS
# ============================================
# Roblox window title to search for
WINDOW_NAME = "Roblox"  # Change if your window has a different title


# ============================================
# SAFETY SETTINGS
# ============================================
# Emergency input unblock timeouts (seconds)
CRITICAL_SAFETY_TIMEOUT = 90  # Force unblock input after this many seconds
EATING_SAFETY_TIMEOUT = 90  # Force unblock during eating after this many seconds


# ============================================
# SCREENSHOT SETTINGS
# ============================================
# Save screenshots when detections occur
SAVE_DETECTION_SCREENSHOTS = True  # Set to False to disable screenshot saving
DELETE_SCREENSHOTS_AFTER_DISCORD = True  # Delete screenshots after sending to Discord

# Screenshot save location
SCREENSHOT_FOLDER = "assets/screenshots"


# ============================================
# ADVANCED SETTINGS (MODIFY WITH CAUTION)
# ============================================
# Emergency stop key combination: Ctrl+Alt+M
EMERGENCY_STOP_KEYS = {
    'ctrl': True,
    'alt': True,
    'm': True
}

# Detection thread settings
DETECTION_CHECK_INTERVAL = 0  # Seconds between checks (0 = as fast as possible)
DETECTION_STATUS_PRINT_INTERVAL = 5  # Print detection thread status every X seconds

# Main loop settings
MAIN_LOOP_DELAY = 0.25  # Seconds between main loop iterations
STATUS_UPDATE_INTERVAL = 10  # Print status update every X seconds
