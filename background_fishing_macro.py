"""
Roblox Arcane Odyssey - Background Fishing Macro
Detects images and clicks even when window is not in focus
"""

import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image
import time
from ctypes import windll, Structure, c_long, c_ulong, sizeof, byref
import ctypes
from ctypes import wintypes  # For MSG structure in message loop
import threading
import sys
import random
import queue
import requests
import json

# Define structures for SendInput
class MOUSEINPUT(Structure):
    _fields_ = [
        ("dx", c_long),
        ("dy", c_long),
        ("mouseData", c_ulong),
        ("dwFlags", c_ulong),
        ("time", c_ulong),
        ("dwExtraInfo", ctypes.POINTER(c_ulong))
    ]

class INPUT(Structure):
    _fields_ = [
        ("type", c_ulong),
        ("mi", MOUSEINPUT)
    ]

# Mouse event flags
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000
INPUT_MOUSE = 0

# Input blocking functions
def block_input():
    """Block all keyboard and mouse input"""
    return ctypes.windll.user32.BlockInput(True)

def unblock_input():
    """Unblock all keyboard and mouse input"""
    return ctypes.windll.user32.BlockInput(False)

def safe_set_cursor_pos(pos):
    """Safely set cursor position with validation"""
    try:
        if pos and isinstance(pos, (tuple, list)) and len(pos) == 2:
            x, y = pos
            # Validate coordinates are reasonable (within screen bounds)
            # Get screen dimensions
            screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            screen_height = ctypes.windll.user32.GetSystemMetrics(1)
            
            # Clamp coordinates to screen bounds
            x = max(0, min(x, screen_width - 1))
            y = max(0, min(y, screen_height - 1))
            
            win32api.SetCursorPos((int(x), int(y)))
            return True
    except Exception as e:
        print(f"[WARNING] Failed to set cursor position to {pos}: {e}")
        return False
    return False

# ============================================
# CONFIGURATION LOADING
# ============================================
# Try to load user configuration from config.py
# If not found, use default values and warn user
try:
    from config import (
        DISCORD_WEBHOOK_URL,
        ENABLE_DISCORD_NOTIFICATIONS,
        DISCORD_MENTION_USER_ID,
        MENTION_ON_COMBAT_DETECTED,
        MENTION_ON_AUTO_KILL,
        POINT_CONFIDENCE,
        FISH_CONFIDENCE,
        TREASURE_CONFIDENCE,
        SUNKEN_CONFIDENCE,
        JUNK_CONFIDENCE,
        CAUGHT_CONFIDENCE,
        MAX_CLICKING_DURATION,
        NO_DETECTION_TIMEOUT,
        CLICK_DELAY,
        DEFAULT_EATING_INTERVAL,
        DEFAULT_EATING_COUNT,
        FOOD_SLOT_KEY,
        ROD_SLOT_KEY,
        WINDOW_NAME,
        CRITICAL_SAFETY_TIMEOUT,
        SAVE_DETECTION_SCREENSHOTS,
        DELETE_SCREENSHOTS_AFTER_DISCORD,
        SCREENSHOT_FOLDER,
        DETECTION_IMAGES,
        ENABLE_COMBAT_DETECTION,
        COMBAT_CONFIDENCE,
        COMBAT_AUTO_KILL_ROBLOX,
        COMBAT_INSTANT_KILL,
        COMBAT_KILL_DELAY,
        RECORD_DETECTION_VIDEO,
        VIDEO_DURATION,
        VIDEO_FPS,
        VIDEO_QUALITY,
        DELETE_VIDEOS_AFTER_DISCORD
    )
    print("[CONFIG] ✅ Configuration loaded from config.py")
except ImportError:
    print("[CONFIG] ⚠️  config.py not found - using default settings")
    print("[CONFIG] ⚠️  Run 'python setup_wizard.py' to create a configuration file")
    print("[CONFIG] ⚠️  Or copy config.example.py to config.py and edit it")
    print()
    
    # Set default values if config.py doesn't exist
    DISCORD_WEBHOOK_URL = ""
    ENABLE_DISCORD_NOTIFICATIONS = False
    DISCORD_MENTION_USER_ID = ""
    MENTION_ON_COMBAT_DETECTED = True
    MENTION_ON_AUTO_KILL = True
    POINT_CONFIDENCE = 0.65
    FISH_CONFIDENCE = 0.75
    TREASURE_CONFIDENCE = 0.75
    SUNKEN_CONFIDENCE = 0.75
    JUNK_CONFIDENCE = 0.75
    CAUGHT_CONFIDENCE = 0.75
    MAX_CLICKING_DURATION = 20
    NO_DETECTION_TIMEOUT = 60
    CLICK_DELAY = 0.001
    DEFAULT_EATING_INTERVAL = 300
    DEFAULT_EATING_COUNT = 3
    FOOD_SLOT_KEY = 0x30
    ROD_SLOT_KEY = 0x39
    WINDOW_NAME = "Roblox"
    CRITICAL_SAFETY_TIMEOUT = 90
    SAVE_DETECTION_SCREENSHOTS = True
    DELETE_SCREENSHOTS_AFTER_DISCORD = True
    SCREENSHOT_FOLDER = "assets/screenshots"
    DETECTION_IMAGES = {
        'point': 'assets/images/detection/point.png',
        'fish': 'assets/images/detection/fish_arcane_odyssey.png',
        'treasure': 'assets/images/detection/treasure_arcane_odyssey.png',
        'sunken': 'assets/images/detection/sunken_arcane_odyssey.png',
        'junk': 'assets/images/detection/junk_arcane_odyssey.png',
        'caught': 'assets/images/detection/caught_arcane_odyssey.png',
        'combat': 'assets/images/detection/combat_arcane_odyssey.png',
    }
    ENABLE_COMBAT_DETECTION = True
    COMBAT_CONFIDENCE = 0.70
    COMBAT_AUTO_KILL_ROBLOX = False
    COMBAT_INSTANT_KILL = False
    COMBAT_KILL_DELAY = 10
    RECORD_DETECTION_VIDEO = True
    VIDEO_DURATION = 5
    VIDEO_FPS = 15
    VIDEO_QUALITY = 23
    DELETE_VIDEOS_AFTER_DISCORD = True
# ============================================

# Emergency stop flag
emergency_stop = False
input_currently_blocked = False
keyboard_hook = None
ctrl_pressed = False
alt_pressed = False
m_pressed = False
comma_pressed = False
period_pressed = False
script_paused = False  # Flag to pause/resume the script
config_phase_complete = False  # Flag to suppress debug output during initial config

# Keyboard hook constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104
WM_KEYUP = 0x0101
WM_SYSKEYUP = 0x0105

class KBDLLHOOKSTRUCT(Structure):
    _fields_ = [
        ("vkCode", c_ulong),
        ("scanCode", c_ulong),
        ("flags", c_ulong),
        ("time", c_ulong),
        ("dwExtraInfo", ctypes.POINTER(c_ulong))
    ]

def check_hotkey_combinations():
    """Check for hotkey combinations - called after every key state change"""
    global emergency_stop, input_currently_blocked, script_paused
    global ctrl_pressed, alt_pressed, m_pressed, comma_pressed, period_pressed
    
    # Check for Ctrl+, (pause script)
    if ctrl_pressed and comma_pressed and not script_paused:
        print(f"\n[HOTKEY] Ctrl+, detected - PAUSING SCRIPT")
        print("\n" + "=" * 50)
        print("⏸️  SCRIPT PAUSED (Ctrl+,)")
        print("=" * 50)
        script_paused = True
        print("[PAUSE] Script paused - press Ctrl+. to resume")
        
        # Send Discord notification about pause
        if ENABLE_DISCORD_NOTIFICATIONS and DISCORD_WEBHOOK_URL:
            def send_pause_notification():
                try:
                    embed = {
                        "title": "⏸️ Script Paused",
                        "description": "Fishing macro has been paused via Ctrl+, hotkey",
                        "color": 16776960,  # Yellow
                        "fields": [
                            {
                                "name": "📌 Status",
                                "value": "Paused - Press Ctrl+. to resume",
                                "inline": False
                            }
                        ],
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                    }
                    send_discord_notification(DISCORD_WEBHOOK_URL, "", embed)
                except Exception as e:
                    print(f"[HOOK DEBUG] Error in pause notification: {e}")
            threading.Thread(target=send_pause_notification, daemon=True).start()
    
    # Check for Ctrl+. (resume script)
    elif ctrl_pressed and period_pressed and script_paused:
        print(f"\n[HOTKEY] Ctrl+. detected - RESUMING SCRIPT")
        print("\n" + "=" * 50)
        print("▶️  SCRIPT RESUMED (Ctrl+.)")
        print("=" * 50)
        script_paused = False
        print("[RESUME] Script resumed - fishing continues")
        
        # Send Discord notification about resume
        if ENABLE_DISCORD_NOTIFICATIONS and DISCORD_WEBHOOK_URL:
            def send_resume_notification():
                try:
                    embed = {
                        "title": "▶️ Script Resumed",
                        "description": "Fishing macro has been resumed via Ctrl+. hotkey",
                        "color": 5763719,  # Green
                        "fields": [
                            {
                                "name": "📌 Status",
                                "value": "Active - Fishing continues",
                                "inline": False
                            }
                        ],
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                    }
                    send_discord_notification(DISCORD_WEBHOOK_URL, "", embed)
                except Exception as e:
                    print(f"[HOOK DEBUG] Error in resume notification: {e}")
            threading.Thread(target=send_resume_notification, daemon=True).start()
    
    # Check for Ctrl+Alt+M combination (emergency stop)
    elif ctrl_pressed and alt_pressed and m_pressed:
        print(f"\n[HOOK DEBUG] Ctrl+Alt+M combination detected!")
        if not emergency_stop:
            print("\n" + "=" * 50)
            print("🚨 EMERGENCY STOP ACTIVATED (Ctrl+Alt+M)! 🚨")
            print("=" * 50)
            emergency_stop = True
            
            # Immediately unblock input
            if input_currently_blocked:
                print("[EMERGENCY] Attempting to unblock input...")
                unblock_result = unblock_input()
                print(f"[EMERGENCY] UnblockInput() returned: {unblock_result}")
                input_currently_blocked = False
                print("[EMERGENCY] Input unblocked!")
            
            print("[EMERGENCY] Program will stop safely...")

def keyboard_hook_callback(nCode, wParam, lParam):
    """Low-level keyboard hook callback - this bypasses BlockInput!"""
    global emergency_stop, input_currently_blocked, script_paused
    global ctrl_pressed, alt_pressed, m_pressed, comma_pressed, period_pressed
    
    if nCode >= 0:
        kb_struct = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk_code = kb_struct.vkCode
        
        # Virtual key codes - include both generic and specific variants
        VK_CONTROL = 0x11       # Generic Ctrl
        VK_LCONTROL = 0xA2      # Left Ctrl (specific)
        VK_RCONTROL = 0xA3      # Right Ctrl (specific)
        VK_MENU = 0x12          # Generic ALT key
        VK_LMENU = 0xA4         # Left Alt (specific)
        VK_RMENU = 0xA5         # Right Alt (specific)
        VK_M = 0x4D
        VK_COMMA = 0xBC         # , key
        VK_PERIOD = 0xBE        # . key
        
        # Track key down/up
        if wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN:
            # Track Ctrl key (any variant)
            if vk_code in (VK_CONTROL, VK_LCONTROL, VK_RCONTROL):
                ctrl_pressed = True
            # Track Alt key (any variant)
            elif vk_code in (VK_MENU, VK_LMENU, VK_RMENU):
                alt_pressed = True
            elif vk_code == VK_M:
                m_pressed = True
            elif vk_code == VK_COMMA:
                comma_pressed = True
            elif vk_code == VK_PERIOD:
                period_pressed = True
            
            # Check for hotkey combinations after key press
            check_hotkey_combinations()
        
        elif wParam == WM_KEYUP or wParam == WM_SYSKEYUP:
            # Track key releases
            # Release Ctrl key (any variant)
            if vk_code in (VK_CONTROL, VK_LCONTROL, VK_RCONTROL):
                ctrl_pressed = False
            # Release Alt key (any variant)
            elif vk_code in (VK_MENU, VK_LMENU, VK_RMENU):
                alt_pressed = False
            elif vk_code == VK_M:
                m_pressed = False
            elif vk_code == VK_COMMA:
                comma_pressed = False
            elif vk_code == VK_PERIOD:
                period_pressed = False
            
            # Check for hotkey combinations after key release (in case keys held)
            check_hotkey_combinations()
    
    # Call next hook in chain
    return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)

# Create callback function pointer
HOOKPROC = ctypes.CFUNCTYPE(c_long, ctypes.c_int, ctypes.c_int, ctypes.POINTER(c_long))
keyboard_hook_pointer = HOOKPROC(keyboard_hook_callback)

def emergency_stop_listener():
    """Listen for Ctrl+Alt+M using low-level keyboard hook (bypasses BlockInput!)"""
    global emergency_stop, keyboard_hook, script_paused
    global ctrl_pressed, alt_pressed, m_pressed, config_phase_complete
    
    print("[EMERGENCY LISTENER] Thread started - installing low-level keyboard hook")
    print("[EMERGENCY LISTENER] This hook intercepts keys BEFORE BlockInput affects them!")
    print("[EMERGENCY LISTENER] Press Ctrl+Alt+M to emergency stop")
    print()
    
    try:
        # Install low-level keyboard hook (using Unicode version for consistency)
        # NOTE: For WH_KEYBOARD_LL, hMod parameter MUST be NULL (not a module handle)
        # Low-level hooks are implemented as callbacks, not DLL functions
        keyboard_hook = ctypes.windll.user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            keyboard_hook_pointer,
            None,  # hMod must be NULL for low-level hooks!
            0
        )
        
        if not keyboard_hook:
            # Get detailed Windows error information
            error_code = ctypes.windll.kernel32.GetLastError()
            error_messages = {
                0: "ERROR_SUCCESS (but hook still returned NULL)",
                126: "ERROR_MOD_NOT_FOUND - Module not found (API version mismatch - fixed!)",
                1428: "ERROR_HOOK_NEEDS_HMOD - Module handle required for this hook type",
                1429: "ERROR_INVALID_HOOK_HANDLE - Invalid hook handle",
                87: "ERROR_INVALID_PARAMETER - Invalid parameter passed to SetWindowsHookEx",
                5: "ERROR_ACCESS_DENIED - Access denied (Administrator privileges required)",
                8: "ERROR_NOT_ENOUGH_MEMORY - Not enough memory",
                6: "ERROR_INVALID_HANDLE - Invalid handle"
            }
            error_msg = error_messages.get(error_code, f"Unknown Windows error code: {error_code}")
            
            print(f"[HOOK ERROR] ❌ Failed to install keyboard hook!")
            print(f"[HOOK ERROR] Windows Error Code: {error_code}")
            print(f"[HOOK ERROR] Description: {error_msg}")
            print(f"[HOOK ERROR] ")
            print(f"[HOOK ERROR] This is most likely caused by:")
            print(f"[HOOK ERROR]   1. ⚠️  NOT running as Administrator (most common)")
            print(f"[HOOK ERROR]      Solution: Close PowerShell, right-click → 'Run as Administrator'")
            print(f"[HOOK ERROR]   2. Anti-virus blocking keyboard hooks (security feature)")
            print(f"[HOOK ERROR]      Solution: Add script to AV whitelist or temporarily disable AV")
            print(f"[HOOK ERROR]   3. Another application conflicting with hooks")
            print(f"[HOOK ERROR]      Solution: Close Discord overlay, OBS, game overlays, etc.")
            print(f"[HOOK ERROR] ")
            print(f"[HOOK ERROR] Falling back to GetAsyncKeyState (limited functionality)...")
            print()
            
            # Fallback to old method - check MORE frequently when input is NOT blocked
            VK_CONTROL = 0x11
            VK_MENU = 0x12
            VK_M = 0x4D
            VK_COMMA = 0xBC
            VK_PERIOD = 0xBE
            check_counter = 0
            last_status_print = time.time()
            last_input_block_state = False
            fallback_info_printed = False  # Track if we've printed the fallback info
            
            # Track key states to prevent repeated triggers
            last_ctrl_down = False
            last_comma_down = False
            last_period_down = False
            last_m_down = False
            last_alt_down = False
            
            while not emergency_stop:
                # Print fallback info only once after config phase is complete
                if config_phase_complete and not fallback_info_printed:
                    print("[FALLBACK] Using GetAsyncKeyState (won't work when input blocked)")
                    print("[FALLBACK] Will check hotkeys every 50ms when input is NOT blocked")
                    print("[FALLBACK] Supported hotkeys: Ctrl+Alt+M (stop), Ctrl+, (pause), Ctrl+. (resume)")
                    print("[FALLBACK] When input IS blocked, hotkeys won't work - unblock will happen after current action")
                    print()
                    fallback_info_printed = True
                
                check_counter += 1
                current_time = time.time()
                
                # When input is NOT blocked, we can detect keys - check very frequently!
                if not input_currently_blocked:
                    ctrl_state = ctypes.windll.user32.GetAsyncKeyState(VK_CONTROL)
                    alt_state = ctypes.windll.user32.GetAsyncKeyState(VK_MENU)
                    m_state = ctypes.windll.user32.GetAsyncKeyState(VK_M)
                    comma_state = ctypes.windll.user32.GetAsyncKeyState(VK_COMMA)
                    period_state = ctypes.windll.user32.GetAsyncKeyState(VK_PERIOD)
                    
                    # Check key states
                    ctrl_down = (ctrl_state & 0x8000) != 0
                    alt_down = (alt_state & 0x8000) != 0
                    m_down = (m_state & 0x8000) != 0
                    comma_down = (comma_state & 0x8000) != 0
                    period_down = (period_state & 0x8000) != 0
                    
                    # Check for Ctrl+Alt+M (emergency stop)
                    if ctrl_down and alt_down and m_down and not (last_ctrl_down and last_alt_down and last_m_down):
                        print(f"\n[FALLBACK] Ctrl+Alt+M detected while input NOT blocked!")
                        print("\n" + "=" * 50)
                        print("🚨 EMERGENCY STOP ACTIVATED (Ctrl+Alt+M)! 🚨")
                        print("=" * 50)
                        emergency_stop = True
                        print("[EMERGENCY] Program will stop after current action...")
                        break
                    
                    # Check for Ctrl+, (pause) - only trigger on new press
                    if ctrl_down and comma_down and not script_paused and not (last_ctrl_down and last_comma_down):
                        print(f"[FALLBACK DEBUG] ✓ Ctrl+, combination detected! Attempting to pause...")
                        print(f"\n[HOTKEY] Ctrl+, detected - PAUSING SCRIPT")
                        print("\n" + "=" * 50)
                        print("⏸️  SCRIPT PAUSED (Ctrl+,)")
                        print("=" * 50)
                        script_paused = True
                        print("[PAUSE] Script paused - press Ctrl+. to resume")
                        
                        # Send Discord notification
                        if ENABLE_DISCORD_NOTIFICATIONS and DISCORD_WEBHOOK_URL:
                            def send_pause_notification():
                                try:
                                    embed = {
                                        "title": "⏸️ Script Paused",
                                        "description": "Fishing macro has been paused via Ctrl+, hotkey",
                                        "color": 16776960,
                                        "fields": [{"name": "📌 Status", "value": "Paused - Press Ctrl+. to resume", "inline": False}],
                                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                                    }
                                    result = send_discord_notification(DISCORD_WEBHOOK_URL, "", embed)
                                    print(f"[FALLBACK DEBUG] Pause notification sent: {result}")
                                except Exception as e:
                                    print(f"[FALLBACK DEBUG] Error sending pause notification: {e}")
                            threading.Thread(target=send_pause_notification, daemon=True).start()
                    
                    # Check for Ctrl+. (resume) - only trigger on new press
                    if ctrl_down and period_down and script_paused and not (last_ctrl_down and last_period_down):
                        print(f"[FALLBACK DEBUG] ✓ Ctrl+. combination detected! Attempting to resume...")
                        print(f"\n[HOTKEY] Ctrl+. detected - RESUMING SCRIPT")
                        print("\n" + "=" * 50)
                        print("▶️  SCRIPT RESUMED (Ctrl+.)")
                        print("=" * 50)
                        script_paused = False
                        print("[RESUME] Script resumed - fishing continues")
                        
                        # Send Discord notification
                        if ENABLE_DISCORD_NOTIFICATIONS and DISCORD_WEBHOOK_URL:
                            def send_resume_notification():
                                try:
                                    embed = {
                                        "title": "▶️ Script Resumed",
                                        "description": "Fishing macro has been resumed via Ctrl+. hotkey",
                                        "color": 5763719,
                                        "fields": [{"name": "📌 Status", "value": "Active - Fishing continues", "inline": False}],
                                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                                    }
                                    result = send_discord_notification(DISCORD_WEBHOOK_URL, "", embed)
                                    print(f"[FALLBACK DEBUG] Resume notification sent: {result}")
                                except Exception as e:
                                    print(f"[FALLBACK DEBUG] Error sending resume notification: {e}")
                            threading.Thread(target=send_resume_notification, daemon=True).start()
                    
                    # Update last key states
                    last_ctrl_down = ctrl_down
                    last_alt_down = alt_down
                    last_m_down = m_down
                    last_comma_down = comma_down
                    last_period_down = period_down
                
                # Track when input blocking state changes
                if input_currently_blocked != last_input_block_state:
                    if input_currently_blocked and config_phase_complete:
                        print("[FALLBACK] Input is now BLOCKED - Ctrl+Alt+M won't be detected until unblocked")
                    elif not input_currently_blocked and config_phase_complete:
                        print("[FALLBACK] Input is now UNBLOCKED - Ctrl+Alt+M will be detected")
                    last_input_block_state = input_currently_blocked
                
                if current_time - last_status_print >= 10.0 and config_phase_complete:
                    print(f"[EMERGENCY DEBUG] Fallback mode - checked {check_counter} times | input_blocked={input_currently_blocked}")
                    last_status_print = current_time
                    check_counter = 0
                
                # Check more frequently when input is not blocked (50ms), less when blocked (200ms)
                time.sleep(0.05 if not input_currently_blocked else 0.2)
        else:
            print(f"[EMERGENCY LISTENER] Keyboard hook installed successfully (handle: {keyboard_hook})")
            print("[EMERGENCY LISTENER] Monitoring for Ctrl+Alt+M...")
            print()
            
            # Process messages to keep hook alive
            msg = wintypes.MSG()
            check_counter = 0
            last_status_print = time.time()
            
            while not emergency_stop:
                # Check for messages (non-blocking)
                if ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
                    ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                    ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
                
                check_counter += 1
                current_time = time.time()
                
                # Print periodic status (only after config phase)
                if current_time - last_status_print >= 10.0 and config_phase_complete:
                    print(f"[EMERGENCY DEBUG] Hook active - {check_counter} iterations | "
                          f"emergency_stop={emergency_stop} | input_blocked={input_currently_blocked}")
                    last_status_print = current_time
                    check_counter = 0
                
                time.sleep(0.01)  # Short sleep to avoid busy loop
    
    except Exception as e:
        print(f"[ERROR] Exception in emergency listener: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Unhook on exit
        if keyboard_hook:
            ctypes.windll.user32.UnhookWindowsHookEx(keyboard_hook)
            print("[EMERGENCY LISTENER] Keyboard hook uninstalled")
        
        print("[EMERGENCY LISTENER] Thread exiting...")
        print(f"[EMERGENCY DEBUG] Final state: emergency_stop={emergency_stop}")

def start_emergency_listener():
    """Start the emergency stop listener in a background thread"""
    listener_thread = threading.Thread(target=emergency_stop_listener, daemon=True)
    listener_thread.start()
    return listener_thread

def send_discord_notification_async(webhook_url, message, embed=None, image_path=None, video_path=None):
    """Send Discord notification in a background thread to avoid blocking"""
    def _send():
        if video_path:
            send_discord_notification_with_video(webhook_url, message, embed, video_path)
        else:
            send_discord_notification(webhook_url, message, embed, image_path)
    
    thread = threading.Thread(target=_send, daemon=True)
    thread.start()
    return thread

def send_discord_notification(webhook_url, message, embed=None, image_path=None):
    """Send a notification to Discord via webhook
    
    Args:
        webhook_url: Discord webhook URL
        message: Text message to send
        embed: Optional embed dict with title, description, color, fields
        image_path: Optional path to image file to attach
    """
    if not ENABLE_DISCORD_NOTIFICATIONS or not webhook_url:
        return False
    
    try:
        # If we have an image, send with multipart/form-data
        if image_path and embed:
            # Update embed to reference the attachment
            embed["image"] = {"url": "attachment://catch.png"}
            
            payload = {
                "content": message,
                "embeds": [embed]
            }
            
            with open(image_path, "rb") as image_file:
                response = requests.post(
                    webhook_url,
                    data={"payload_json": json.dumps(payload)},
                    files={"file": ("catch.png", image_file, "image/png")},
                    timeout=10
                )
        else:
            # Normal JSON payload without image
            payload = {
                "content": message
            }
            
            if embed:
                payload["embeds"] = [embed]
            
            response = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=5
            )
        
        if response.status_code == 204 or response.status_code == 200:
            return True
        else:
            print(f"[DISCORD] Failed to send notification: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[DISCORD] Error sending notification: {e}")
        import traceback
        traceback.print_exc()
        return False


def send_discord_notification_with_video(webhook_url, message, embed=None, video_path=None):
    """Send a notification to Discord via webhook with video attachment
    
    Args:
        webhook_url: Discord webhook URL
        message: Text message to send
        embed: Optional embed dict
        video_path: Path to video file to attach
    """
    if not ENABLE_DISCORD_NOTIFICATIONS or not webhook_url:
        return False
    
    try:
        payload = {
            "content": message
        }
        
        if embed:
            payload["embeds"] = [embed]
        
        # Send with video attachment
        with open(video_path, "rb") as video_file:
            response = requests.post(
                webhook_url,
                data={"payload_json": json.dumps(payload)},
                files={"file": ("fishing_detection.mp4", video_file, "video/mp4")},
                timeout=30  # Longer timeout for video upload
            )
        
        if response.status_code == 204 or response.status_code == 200:
            return True
        else:
            print(f"[DISCORD] Failed to send video: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[DISCORD] Error sending video: {e}")
        import traceback
        traceback.print_exc()
        return False

class BackgroundWindowCapture:
    """Captures window content even when it's not in focus"""
    
    def __init__(self, window_name="Roblox"):
        self.hwnd = None
        self.window_name = window_name
        self.find_window()
        
    def find_window(self):
        """Find the Roblox window"""
        self.hwnd = win32gui.FindWindow(None, self.window_name)
        if not self.hwnd:
            raise Exception(f"Window '{self.window_name}' not found! Make sure Roblox is running.")
        print(f"Found window: {self.window_name} (Handle: {self.hwnd})")
        
    def get_window_rect(self):
        """Get window dimensions"""
        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        return x, y, w, h
        
    def capture_window(self):
        """Capture window content as numpy array (works in background)"""
        try:
            # Get window dimensions
            x, y, w, h = self.get_window_rect()
            
            # Get window device context
            wDC = win32gui.GetWindowDC(self.hwnd)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
            cDC.SelectObject(dataBitMap)
            
            # Copy window content to bitmap
            result = windll.user32.PrintWindow(self.hwnd, cDC.GetSafeHdc(), 3)
            
            # Convert to numpy array
            bmpinfo = dataBitMap.GetInfo()
            bmpstr = dataBitMap.GetBitmapBits(True)
            img = np.frombuffer(bmpstr, dtype=np.uint8)
            img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
            
            # Clean up
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
            
            # Convert BGRA to BGR for OpenCV
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            return img if result == 1 else None
            
        except Exception as e:
            print(f"Error capturing window: {e}")
            return None
    
    def bring_to_front(self):
        """Bring window to foreground temporarily and return previous window handle"""
        try:
            # Get current foreground window to restore later
            previous_hwnd = win32gui.GetForegroundWindow()
            
            # Check if already foreground
            if previous_hwnd == self.hwnd:
                return previous_hwnd
                
            # Try to bring to front
            win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self.hwnd)
            time.sleep(0.05)  # Brief delay for window to come to front
            return previous_hwnd
        except Exception as e:
            # Silently fail - window might still accept clicks
            return None
    
    def restore_window(self, hwnd):
        """Restore a previously focused window"""
        try:
            if hwnd and hwnd != self.hwnd:
                win32gui.SetForegroundWindow(hwnd)
        except:
            pass  # Silently fail
    
    def send_click(self, x, y, debug=False, focus_window=True, return_previous_window=None, block_user_input=False):
        """Send mouse click to window
        
        Args:
            return_previous_window: If provided, will be used to restore previous window after click
            block_user_input: If True, blocks all user input during click to prevent interference
        """
        window_x, window_y, w, h = self.get_window_rect()
        
        # Calculate absolute screen position
        screen_x = window_x + x
        screen_y = window_y + y
        
        if debug:
            print(f"[CLICK DEBUG] Window rect: x={window_x}, y={window_y}, w={w}, h={h}")
            print(f"[CLICK DEBUG] Relative click: ({x}, {y})")
            print(f"[CLICK DEBUG] Screen position: ({screen_x}, {screen_y})")
            print(f"[CLICK DEBUG] Focus window: {focus_window}")
            print(f"[CLICK DEBUG] Block input: {block_user_input}")
        
        # Block user input if requested
        if block_user_input:
            block_input()
            if debug:
                print(f"[CLICK DEBUG] User input blocked")
        
        try:
            # Bring window to front if needed (required for Roblox)
            previous_hwnd = None
            if focus_window:
                previous_hwnd = self.bring_to_front()
            
            # Save current cursor position
            original_pos = win32api.GetCursorPos()
            
            # Move cursor to target position
            safe_set_cursor_pos((screen_x, screen_y))
            time.sleep(0.01)
            
            # Perform click using SendInput
            extra = c_ulong(0)
            ii_ = INPUT()
            ii_.type = INPUT_MOUSE
            
            # Mouse down
            ii_.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra))
            ctypes.windll.user32.SendInput(1, ctypes.byref(ii_), ctypes.sizeof(ii_))
            time.sleep(0.02)
            
            # Mouse up
            ii_.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra))
            ctypes.windll.user32.SendInput(1, ctypes.byref(ii_), ctypes.sizeof(ii_))
            
            # Restore cursor position
            time.sleep(0.01)
            safe_set_cursor_pos(original_pos)
            
            # Restore previous window if requested
            if return_previous_window and previous_hwnd:
                time.sleep(0.05)
                self.restore_window(previous_hwnd)
                if debug:
                    print(f"[CLICK DEBUG] Restored previous window")
            
            if debug:
                print(f"[CLICK DEBUG] Click completed at ({screen_x}, {screen_y})")
                print("-" * 40)
            
            return previous_hwnd
        
        finally:
            # Always unblock input even if there's an error
            if block_user_input:
                unblock_input()
                if debug:
                    print(f"[CLICK DEBUG] User input unblocked")
    
    def send_key(self, key_code, debug=False):
        """Send a key press to the window
        
        Args:
            key_code: Virtual key code (e.g., 0x30 for '0', 0x39 for '9')
            debug: Whether to show debug output
        """
        try:
            if debug:
                key_name = "0" if key_code == 0x30 else "9" if key_code == 0x39 else f"0x{key_code:02X}"
                print(f"[KEY DEBUG] Attempting to send key: {key_name} (code: 0x{key_code:02X})")
            
            # Bring window to front first and wait for it to be ready
            previous_hwnd = self.bring_to_front()
            time.sleep(0.3)  # Wait for window to be fully focused
            
            if debug:
                print(f"[KEY DEBUG] Window brought to front, previous handle: {previous_hwnd}")
            
            # Use keybd_event which works at a lower level and sometimes bypasses Roblox anti-cheat
            # This simulates actual hardware keyboard input
            import ctypes
            
            # Get scan code for the key
            scan_code = ctypes.windll.user32.MapVirtualKeyW(key_code, 0)
            
            if debug:
                print(f"[KEY DEBUG] Scan code: {scan_code}")
            
            # Press key down
            ctypes.windll.user32.keybd_event(key_code, scan_code, 0, 0)
            time.sleep(0.15)  # Hold the key down
            
            # Release key
            ctypes.windll.user32.keybd_event(key_code, scan_code, 2, 0)  # 2 = KEYEVENTF_KEYUP
            
            if debug:
                key_name = "0" if key_code == 0x30 else "9" if key_code == 0x39 else f"0x{key_code:02X}"
                print(f"[KEY DEBUG] Key {key_name} press completed via keybd_event (hardware simulation)")
            
            time.sleep(0.1)  # Small delay after keypress
            
            return previous_hwnd
            
        except Exception as e:
            print(f"[ERROR] Failed to send key: {e}")
            import traceback
            traceback.print_exc()
            return None


class ImageDetector:
    """Detects images in captured window"""
    
    def __init__(self, template_path, confidence=0.55, optional=False):
        self.template = cv2.imread(template_path)
        if self.template is None:
            if optional:
                print(f"[WARNING] Optional template image not found: {template_path}")
                self.template = None
            else:
                raise FileNotFoundError(f"Template image not found: {template_path}")
        self.confidence = confidence
        self.optional = optional
        if self.template is not None:
            self.template_height, self.template_width = self.template.shape[:2]
        
    def find_in_image(self, screenshot, debug=False):
        """Find template in screenshot using template matching"""
        if screenshot is None or self.template is None:
            return None
            
        # Perform template matching
        result = cv2.matchTemplate(screenshot, self.template, cv2.TM_CCOEFF_NORMED)
        
        if debug:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print(f"[DETECTION DEBUG] Max confidence: {max_val:.3f}, Threshold: {self.confidence}")
        
        # Find locations where matching exceeds confidence threshold
        locations = np.where(result >= self.confidence)
        
        if len(locations[0]) > 0:
            # Get the best match
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # Calculate center point
            center_x = max_loc[0] + self.template_width // 2
            center_y = max_loc[1] + self.template_height // 2
            
            return {
                'x': center_x,
                'y': center_y,
                'confidence': max_val,
                'rect': (max_loc[0], max_loc[1], self.template_width, self.template_height)
            }
        
        return None


class FishingMacro:
    """Main fishing macro controller"""
    
    def __init__(self, fishing_time_seconds, eating_interval_seconds, eating_count, debug=False, webhook_url=None):
        self.window_capture = BackgroundWindowCapture(WINDOW_NAME)
        self.point_detector = ImageDetector(DETECTION_IMAGES.get('point', 'assets/images/detection/point.png'), confidence=POINT_CONFIDENCE)
        
        # Store webhook URL (use provided or fall back to config)
        self.webhook_url = webhook_url if webhook_url else DISCORD_WEBHOOK_URL
        
        # Hunger detection (optional)
        hunger_image = DETECTION_IMAGES.get('hunger', 'assets/images/detection/hunger.png')
        self.hunger_detector = ImageDetector(hunger_image, confidence=0.15, optional=True) if hunger_image else None
        self.has_hunger_detector = self.hunger_detector and self.hunger_detector.template is not None
        if self.has_hunger_detector:
            print("[INFO] Hunger detection enabled - will auto-eat when hungry (threshold: 0.15)")
            print("[INFO] IMPORTANT: hunger.png should be a screenshot of the hunger BAR when it's LOW (≤35%)")
        
        # Combat detection (optional)
        combat_image = DETECTION_IMAGES.get('combat', 'assets/images/detection/combat_arcane_odyssey.png')
        self.combat_detector = ImageDetector(combat_image, confidence=COMBAT_CONFIDENCE, optional=True) if combat_image else None
        self.has_combat_detector = self.combat_detector and self.combat_detector.template is not None and ENABLE_COMBAT_DETECTION
        self.combat_detected_time = None  # Track when combat was first detected
        self.combat_notification_sent = False  # Track if we've sent the warning
        self.stop_combat_detection = threading.Event()  # Signal to stop combat detection thread
        self.combat_active = False  # Flag to pause fishing/eating during combat
        
        if self.has_combat_detector:
            print(f"[INFO] Combat detection enabled - will alert via Discord (confidence: {COMBAT_CONFIDENCE})")
            if COMBAT_AUTO_KILL_ROBLOX:
                print(f"[INFO] AUTO-KILL ENABLED - Roblox will be terminated {COMBAT_KILL_DELAY}s after combat detection!")
            else:
                print("[INFO] Auto-kill disabled - you'll be notified but game won't close")
        
        # Load caught detection images from config
        self.caught_detectors = []
        detector_configs = [
            ('fish', FISH_CONFIDENCE),
            ('treasure', TREASURE_CONFIDENCE),
            ('sunken', SUNKEN_CONFIDENCE),
            ('junk', JUNK_CONFIDENCE),
            ('caught', CAUGHT_CONFIDENCE),
        ]
        
        for img_key, conf in detector_configs:
            img_path = DETECTION_IMAGES.get(img_key)
            if img_path:  # Only process if image path exists
                detector = ImageDetector(img_path, confidence=conf, optional=True)
                if detector.template is not None:
                    self.caught_detectors.append((img_path, detector))
                    print(f"[INFO] Loaded catch detector: {img_path} (confidence: {conf})")
        
        self.has_caught_detector = len(self.caught_detectors) > 0
        if not self.has_caught_detector:
            print("[WARNING] No 'caught' detection images found. Will rely on timeout only.")
        
        self.fishing_time = fishing_time_seconds
        self.end_time = time.time() + fishing_time_seconds
        self.no_detection_timeout = NO_DETECTION_TIMEOUT
        self.last_detection_time = time.time()
        
        self.click_count = 0
        self.detection_count = 0
        self.debug = debug
        self.last_hunger_check = 0
        self.hunger_check_interval = 10  # Check hunger every 10 seconds
        self.fish_just_caught = False  # Track if we just caught a fish
        
        # User-configured eating schedule
        self.last_eat_time = time.time()
        self.next_eat_interval = eating_interval_seconds
        self.eating_count = eating_count  # How many food items to eat per session
        self.eat_count = 0  # Track number of eating sessions
        print(f"[INFO] Eating configured - will eat {eating_count} food items every {eating_interval_seconds}s (continuously throughout session)")
        
        # Threading for parallel detection
        self.detection_queue = queue.Queue()
        self.caught_flag = threading.Event()  # Signal when fish is caught
        self.stop_detection = threading.Event()  # Signal to stop detection thread
        self.detection_check_count = 0
        
        # Statistics tracking for Discord notifications
        self.total_catches = 0
        self.catch_history = []  # List of (detector_name, confidence, timestamp)
        self.macro_start_time = time.time()
        self.last_catch_time = time.time()  # Track time of last catch for duration calculation
        self.auto_cast_count = 0  # Track number of auto-casts (no detection timeout)
        self.combat_detection_count = 0  # Track number of times combat was detected
        self.consecutive_no_detection = 0  # Track consecutive auto-casts without detection (resets on catch)
    
    def _send_eating_notification(self):
        """Send Discord notification about eating completion (runs in background thread)"""
        duration_since_last_meal = time.time() - (self.last_eat_time - (self.last_eat_time - (time.time() - self.next_eat_interval)))
        elapsed_minutes = int(duration_since_last_meal // 60)
        elapsed_seconds = int(duration_since_last_meal % 60)
        
        embed = {
            "title": "🍖 Food Break!",
            "description": f"Eating session #{self.eat_count} completed (ate {self.eating_count} food items)",
            "color": 3447003,  # Blue color
            "fields": [
                {
                    "name": "⏱️ Duration Since Last Meal",
                    "value": f"{elapsed_minutes}m {elapsed_seconds}s",
                    "inline": True
                },
                {
                    "name": "⏰ Next Meal In",
                    "value": f"{self.next_eat_interval // 60}m {self.next_eat_interval % 60}s",
                    "inline": True
                },
                {
                    "name": "📊 Total Catches",
                    "value": f"{self.total_catches} fish",
                    "inline": True
                }
            ],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        }
        send_discord_notification(self.webhook_url, "", embed)
    
    def _save_and_notify_catch(self, screenshot, img_name, max_val, detector_name, time_since_last_catch, check_counter):
        """Save screenshot and send Discord notification for catch (runs in background thread)"""
        screenshot_saved = False
        screenshot_path = None
        
        if SAVE_DETECTION_SCREENSHOTS:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            detector_name_clean = img_name.split('/')[-1].replace('.png', '')
            screenshot_path = f"{SCREENSHOT_FOLDER}/detected_{detector_name_clean}_{timestamp}_conf{max_val:.2f}.png"
            
            try:
                import os
                os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
                cv2.imwrite(screenshot_path, screenshot)
                screenshot_saved = True
                print(f"[DETECTION THREAD] 📸 Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"[DETECTION THREAD] Failed to save screenshot: {e}")
        
        # Send Discord notification about the catch
        if ENABLE_DISCORD_NOTIFICATIONS:
            # Determine catch type emoji and check if it's a sunken item
            is_sunken = "sunken" in detector_name.lower()
            catch_emoji = "🐟"
            if "treasure" in detector_name.lower():
                catch_emoji = "💎"
            elif is_sunken:
                catch_emoji = "⚓"
            elif "junk" in detector_name.lower():
                catch_emoji = "🗑️"
            elif "caught" in detector_name.lower():
                catch_emoji = "🎣"
            
            # Calculate session duration
            session_duration = time.time() - self.macro_start_time
            session_minutes = int(session_duration // 60)
            session_seconds = int(session_duration % 60)
            
            # Time since last meal
            time_since_meal = time.time() - self.last_eat_time
            meal_minutes = int(time_since_meal // 60)
            meal_seconds = int(time_since_meal % 60)
            
            # Get catch breakdown by type
            catch_breakdown = {}
            for catch_name, conf, timestamp in self.catch_history:
                catch_breakdown[catch_name] = catch_breakdown.get(catch_name, 0) + 1
            
            catch_breakdown_text = " | ".join([f"{name.title()}: {count}" for name, count in sorted(catch_breakdown.items())])
            
            # Use different color and title for sunken items (most important)
            embed_color = 15105570 if is_sunken else 5763719  # Orange for sunken, green for others
            embed_title = f"🚨 {catch_emoji} SUNKEN ITEM CAUGHT! 🚨" if is_sunken else f"{catch_emoji} Catch Detected!"
            
            embed = {
                "title": embed_title,
                "description": f"**{detector_name.title()}** caught!",
                "color": embed_color,
                "fields": [
                    {
                        "name": "🎯 Confidence",
                        "value": f"{max_val:.1%}",
                        "inline": True
                    },
                    {
                        "name": "⏱️ Time Since Last Catch",
                        "value": f"{time_since_last_catch:.1f}s ({check_counter} checks)",
                        "inline": True
                    },
                    {
                        "name": "📊 Total Catches",
                        "value": f"{self.total_catches}",
                        "inline": True
                    },
                    {
                        "name": "🐟 Catch Breakdown",
                        "value": catch_breakdown_text or "First catch!",
                        "inline": False
                    },
                    {
                        "name": "🕐 Session Duration",
                        "value": f"{session_minutes}m {session_seconds}s",
                        "inline": True
                    },
                    {
                        "name": "🍖 Since Last Meal",
                        "value": f"{meal_minutes}m {meal_seconds}s",
                        "inline": True
                    },
                    {
                        "name": "🎣 Clicks",
                        "value": f"{self.click_count}",
                        "inline": True
                    }
                ],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            }
            
            # Add user mention for sunken items (most important)
            mention_message = ""
            if is_sunken and DISCORD_MENTION_USER_ID:
                mention_message = f"<@{DISCORD_MENTION_USER_ID}>"
                print(f"[DISCORD] 🚨 SUNKEN ITEM - Mentioning user {DISCORD_MENTION_USER_ID}")
            
            # Send notification with screenshot
            if screenshot_saved and screenshot_path:
                send_discord_notification(self.webhook_url, mention_message, embed, image_path=screenshot_path)
                
                # Delete screenshot after sending to save storage (if enabled)
                if DELETE_SCREENSHOTS_AFTER_DISCORD:
                    try:
                        import os
                        if os.path.exists(screenshot_path):
                            os.remove(screenshot_path)
                            print(f"[DISCORD] Screenshot deleted: {screenshot_path}")
                    except Exception as e:
                        print(f"[DISCORD] Failed to delete screenshot: {e}")
            else:
                # Send without screenshot if saving failed or disabled
                send_discord_notification(self.webhook_url, mention_message, embed)
    
    def _send_threshold_warning(self, screenshot, highest_conf_name, highest_confidence, max_confidences, check_counter):
        """Send threshold warning screenshot and notification (runs in background thread)"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        detector_name_clean = highest_conf_name.replace('.png', '')
        screenshot_path = f"{SCREENSHOT_FOLDER}/no_threshold_{detector_name_clean}_{timestamp}_conf{highest_confidence:.2f}.png"
        
        try:
            import os
            os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
            cv2.imwrite(screenshot_path, screenshot)
            
            embed = {
                "title": "⚠️ Detection Below Threshold",
                "description": f"Highest confidence: **{highest_conf_name}** at {highest_confidence:.1%}",
                "color": 16776960,  # Yellow color
                "fields": [
                    {
                        "name": "🎯 All Confidences",
                        "value": " | ".join([f"{name}: {conf:.1%}" for name, conf in max_confidences]),
                        "inline": False
                    },
                    {
                        "name": "🔍 Check Number",
                        "value": str(check_counter),
                        "inline": True
                    }
                ],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            }
            
            send_discord_notification(self.webhook_url, "", embed, image_path=screenshot_path)
            
            # Delete screenshot after sending
            if DELETE_SCREENSHOTS_AFTER_DISCORD and os.path.exists(screenshot_path):
                os.remove(screenshot_path)
                
        except Exception as e:
            print(f"[DETECTION THREAD] Failed to send threshold warning: {e}")
    
    def _save_point_screenshot_and_notify(self, screenshot, point_location, reason="timeout_or_low_confidence"):
        """Save point detection screenshot/video and send notification (runs in background thread)
        
        Args:
            reason: Why screenshot is being sent - "timeout_or_low_confidence" or "fish_bite"
        """
        screenshot_saved = False
        screenshot_path = None
        video_saved = False
        video_path = None
        
        # Record video if enabled (in separate thread for performance)
        if RECORD_DETECTION_VIDEO and reason != "fish_bite":
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            video_path = f"{SCREENSHOT_FOLDER}/point_{timestamp}_conf{point_location['confidence']:.2f}.mp4"
            
            # Spawn video recording thread (non-blocking)
            def record_video():
                nonlocal video_saved, video_path
                try:
                    import os
                    os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
                    
                    # Get window dimensions
                    _, _, w, h = self.window_capture.get_window_rect()
                    
                    if self.debug:
                        print(f"[VIDEO] 🎥 Recording {VIDEO_DURATION}s video at {VIDEO_FPS} FPS...")
                    
                    # Initialize video writer with H.264 compression
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 codec
                    video_writer = cv2.VideoWriter(video_path, fourcc, VIDEO_FPS, (w, h))
                    
                    if not video_writer.isOpened():
                        print(f"[VIDEO] ❌ Failed to open video writer")
                        return
                    
                    # Record frames for specified duration
                    start_time = time.time()
                    frame_count = 0
                    target_frame_time = 1.0 / VIDEO_FPS
                    
                    while time.time() - start_time < VIDEO_DURATION:
                        frame_start = time.time()
                        
                        # Capture frame
                        frame = self.window_capture.capture_window()
                        if frame is not None:
                            video_writer.write(frame)
                            frame_count += 1
                        
                        # Control frame rate precisely
                        elapsed = time.time() - frame_start
                        sleep_time = target_frame_time - elapsed
                        if sleep_time > 0:
                            time.sleep(sleep_time)
                    
                    # Release video writer
                    video_writer.release()
                    video_saved = True
                    
                    if self.debug:
                        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
                        print(f"[VIDEO] ✅ Video saved: {video_path} ({frame_count} frames, {file_size:.2f}MB)")
                    
                except Exception as e:
                    print(f"[VIDEO] ❌ Failed to record video: {e}")
                    if self.debug:
                        import traceback
                        traceback.print_exc()
            
            # Start video recording thread
            video_thread = threading.Thread(target=record_video, daemon=True)
            video_thread.start()
        
        # Also save a single screenshot as fallback
        if SAVE_DETECTION_SCREENSHOTS:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{SCREENSHOT_FOLDER}/point_{timestamp}_conf{point_location['confidence']:.2f}.png"
            try:
                import os
                os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
                cv2.imwrite(screenshot_path, screenshot)
                screenshot_saved = True
                if self.debug:
                    print(f"[POINT DETECTION] 📸 Screenshot saved: {screenshot_path}")
            except Exception as e:
                if self.debug:
                    print(f"[POINT DETECTION] Failed to save screenshot: {e}")
        
        # Send Discord notification for point detection (only if requested)
        if ENABLE_DISCORD_NOTIFICATIONS and reason != "fish_bite":
            # Determine title and color based on reason
            if reason == "timeout_or_low_confidence":
                title = "⚠️ Fishing Issue Detected"
                description = "Fish caught below threshold OR max clicking duration reached"
                color = 16776960  # Yellow
            else:
                title = "🎣 Fish Bite Detected!"
                description = "Starting clicking sequence..."
                color = 3447003  # Blue
            
            embed = {
                "title": title,
                "description": description,
                "color": color,
                "fields": [
                    {
                        "name": "🎯 Confidence",
                        "value": f"{point_location['confidence']:.1%}",
                        "inline": True
                    },
                    {
                        "name": "📍 Location",
                        "value": f"({point_location['x']}, {point_location['y']})",
                        "inline": True
                    },
                    {
                        "name": "🔢 Detection Count",
                        "value": str(self.detection_count),
                        "inline": True
                    }
                ],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            }
            
            # Wait for video to finish recording if enabled
            if RECORD_DETECTION_VIDEO and video_thread:
                if self.debug:
                    print(f"[VIDEO] ⏳ Waiting for video recording to complete...")
                video_thread.join(timeout=VIDEO_DURATION + 2)  # Wait max duration + 2s buffer
            
            # Prefer video over screenshot for Discord
            if RECORD_DETECTION_VIDEO and video_saved and video_path and os.path.exists(video_path):
                # Send video asynchronously (non-blocking)
                send_discord_notification_async(self.webhook_url, "", embed, video_path=video_path)
                
                # Delete video after sending
                if DELETE_VIDEOS_AFTER_DISCORD:
                    def delete_after_delay():
                        time.sleep(5)  # Wait 5s to ensure upload completes
                        try:
                            if os.path.exists(video_path):
                                os.remove(video_path)
                                if self.debug:
                                    print(f"[DISCORD] 🗑️ Video deleted: {video_path}")
                        except Exception as e:
                            if self.debug:
                                print(f"[DISCORD] Failed to delete video: {e}")
                    
                    threading.Thread(target=delete_after_delay, daemon=True).start()
                    
            elif screenshot_saved and screenshot_path:
                # Fallback to screenshot if video failed
                send_discord_notification(self.webhook_url, "", embed, image_path=screenshot_path)
                
                # Delete screenshot after sending
                if DELETE_SCREENSHOTS_AFTER_DISCORD:
                    try:
                        if os.path.exists(screenshot_path):
                            os.remove(screenshot_path)
                            if self.debug:
                                print(f"[DISCORD] Screenshot deleted: {screenshot_path}")
                    except Exception as e:
                        if self.debug:
                            print(f"[DISCORD] Failed to delete screenshot: {e}")
            else:
                send_discord_notification(self.webhook_url, "", embed)
    
    def eat_food(self):
        """Eat food - press 0, click 3 times, press 9, click once"""
        global input_currently_blocked, emergency_stop, script_paused
        
        # Check if script is paused or stopped before starting
        if script_paused:
            print("[PAUSE] Skipping eating - script is paused")
            return
        
        if emergency_stop:
            print("[STOP] Skipping eating - emergency stop active")
            return
        
        self.eat_count += 1
        print(f"[EATING] Time to eat! (Eat #{self.eat_count})")
        
        if self.debug:
            print("[DEBUG] Starting eat sequence")
        
        # Get window center for clicking
        _, _, w, h = self.window_capture.get_window_rect()
        center_x = w // 2
        center_y = h // 2
        
        # Block user input during eating sequence to prevent interference
        print("[INFO] Blocking user input during eating sequence...")
        input_currently_blocked = True
        eat_input_block_start_time = time.time()  # Track when blocking started for eating
        input_blocked = block_input()
        if self.debug:
            print(f"[DEBUG] BlockInput for eating returned: {input_blocked}")
        
        try:
            # Press configured food slot key to select food
            if self.debug:
                print(f"[DEBUG] About to press food slot key (0x{FOOD_SLOT_KEY:02X})")
            prev_win = self.window_capture.send_key(FOOD_SLOT_KEY, debug=self.debug)
            time.sleep(2)  # Longer delay to ensure game processes the key
            
            if self.debug:
                print(f"[DEBUG] Pressed food slot to select food - now clicking to eat {self.eating_count} times")
            
            # Click N times to eat with longer delays to ensure each food is consumed
            for i in range(self.eating_count):
                # Check if script is paused or stopped during eating
                if script_paused:
                    print("[PAUSE] Script paused during eating - stopping immediately!")
                    input_currently_blocked = False
                    unblock_input()
                    print("[INFO] User input unblocked after pause during eating")
                    return
                
                if emergency_stop:
                    print("[STOP] Emergency stop during eating - stopping immediately!")
                    input_currently_blocked = False
                    unblock_input()
                    print("[INFO] User input unblocked after emergency stop during eating")
                    return
                
                # Safety check: unblock if eating takes too long
                eat_duration = time.time() - eat_input_block_start_time
                if eat_duration > CRITICAL_SAFETY_TIMEOUT:
                    print(f"\n[CRITICAL SAFETY] Eating has taken 90+ seconds!")
                    print(f"[CRITICAL SAFETY] Auto-unblocking to prevent permanent lockout!")
                    input_currently_blocked = False
                    unblock_input()
                    print(f"[CRITICAL SAFETY] Input force-unblocked during eating")
                    return
                
                if self.debug:
                    print(f"[DEBUG] Eating click {i+1}/{self.eating_count}")
                self.window_capture.send_click(center_x, center_y, debug=False)
                self.click_count += 1
                time.sleep(0.8)  # Longer delay between clicks to let animation/consumption finish
            
            if self.debug:
                print("[DEBUG] Clicked 3 times to eat - waiting before selecting rod")
            
            time.sleep(2.0)  # Longer wait to ensure last food is fully consumed before switching
            
            # Press configured rod slot key to select fishing rod
            if self.debug:
                print(f"[DEBUG] About to press rod slot key (0x{ROD_SLOT_KEY:02X})")
            self.window_capture.send_key(ROD_SLOT_KEY, debug=self.debug)
            time.sleep(0.5)  # Longer delay to ensure game processes the key
            
            if self.debug:
                print("[DEBUG] Pressed 9 to select fishing rod - now clicking to cast")
            
            # Click once to equip/cast
            self.window_capture.send_click(center_x, center_y, debug=False, return_previous_window=True)
            self.click_count += 1
            time.sleep(0.5)
            
            # Restore previous window
            if prev_win:
                self.window_capture.restore_window(prev_win)
                if self.debug:
                    print("[DEBUG] Restored previous window")
            
            # Update last eat time (interval stays constant)
            self.last_eat_time = time.time()
            
            print(f"[EATING] Finished eating - next meal in {self.next_eat_interval}s")
            
            # Send Discord notification about eating (in background thread)
            if ENABLE_DISCORD_NOTIFICATIONS:
                threading.Thread(target=self._send_eating_notification, daemon=True).start()
            
        except Exception as e:
            print(f"[ERROR] Failed to eat food: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Always unblock input even if there's an error
            input_currently_blocked = False
            unblock_result = unblock_input()
            if self.debug:
                print(f"[DEBUG] UnblockInput after eating returned: {unblock_result}")
            print("[INFO] User input unblocked after eating - you can use keyboard/mouse again")
    
    def should_eat_now(self):
        """Check if it's time to eat based on user-configured interval"""
        elapsed = time.time() - self.last_eat_time
        if elapsed >= self.next_eat_interval:
            return True
        return False
    
    def combat_detection_worker(self):
        """Background thread that continuously monitors for combat
        
        This thread runs independently and checks for combat_arcane_odyssey.png
        If detected:
        1. Send Discord notification with @mention (3 times) and screenshot
        2. Wait COMBAT_KILL_DELAY seconds
        3. If still detected and COMBAT_AUTO_KILL_ROBLOX is True, kill Roblox process
        """
        global emergency_stop
        
        print("[COMBAT DETECTION] Thread started - monitoring for combat...")
        
        check_counter = 0
        last_debug_print = time.time()
        
        while not self.stop_combat_detection.is_set() and not emergency_stop:
            try:
                # Capture screenshot
                screenshot = self.window_capture.capture_window()
                
                if screenshot is not None and self.has_combat_detector:
                    check_counter += 1
                    
                    # Debug: Print status every 30 seconds
                    if self.debug and (time.time() - last_debug_print) >= 30.0:
                        print(f"[COMBAT DETECTION] Alive - {check_counter} checks performed")
                        last_debug_print = time.time()
                    
                    # Check for combat indicator
                    combat_location = self.combat_detector.find_in_image(screenshot)
                    
                    if combat_location:
                        # Combat detected!
                        if self.combat_detected_time is None:
                            # Check if script is paused - skip combat actions if paused
                            if script_paused:
                                if self.debug:
                                    print("[COMBAT DETECTION] ⏸️ Script is paused - skipping combat alerts and actions")
                                time.sleep(2)
                                continue
                            
                            # First detection
                            self.combat_detected_time = time.time()
                            self.combat_detection_count += 1
                            
                            print(f"\n{'='*60}")
                            print(f"[COMBAT DETECTED] ⚔️  WARNING! Combat indicator found!")
                            print(f"[COMBAT DETECTED] Confidence: {combat_location['confidence']:.2f}")
                            print(f"[COMBAT DETECTED] Location: ({combat_location['x']}, {combat_location['y']})")
                            print(f"{'='*60}\n")
                            
                            # Send Discord notification with mention (SPAM 3 MESSAGES for maximum urgency) in background
                            def send_combat_alert():
                                """Send urgent combat alert to Discord (3 SEPARATE MESSAGES WITH FRESH SCREENSHOTS)"""
                                # Send Discord notification (3 TIMES!)
                                if ENABLE_DISCORD_NOTIFICATIONS:
                                    # Build mention string
                                    mention = ""
                                    if DISCORD_MENTION_USER_ID and MENTION_ON_COMBAT_DETECTED:
                                        mention = f"<@{DISCORD_MENTION_USER_ID}>\n"
                                    
                                    session_duration = time.time() - self.macro_start_time
                                    session_minutes = int(session_duration // 60)
                                    session_seconds = int(session_duration % 60)
                                    
                                    # Determine action text based on kill settings
                                    if COMBAT_AUTO_KILL_ROBLOX:
                                        if COMBAT_INSTANT_KILL:
                                            action_text = "⚡ Roblox will be terminated INSTANTLY (no delay)"
                                        else:
                                            action_text = f"Roblox will be terminated in {COMBAT_KILL_DELAY}s"
                                    else:
                                        action_text = "Game will NOT be closed (auto-kill disabled)"
                                    
                                    # SPAM 3 MESSAGES with FRESH screenshots for maximum urgency!
                                    for i in range(3):
                                        # Capture fresh screenshot for each message
                                        fresh_screenshot = self.window_capture.capture_window()
                                        screenshot_saved = False
                                        screenshot_path = None
                                        
                                        if SAVE_DETECTION_SCREENSHOTS and fresh_screenshot is not None:
                                            timestamp = time.strftime("%Y%m%d_%H%M%S")
                                            screenshot_path = f"{SCREENSHOT_FOLDER}/combat_detected_{timestamp}_msg{i+1}_conf{combat_location['confidence']:.2f}.png"
                                            
                                            try:
                                                import os
                                                os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
                                                cv2.imwrite(screenshot_path, fresh_screenshot)
                                                screenshot_saved = True
                                                print(f"[COMBAT DETECTION] 📸 Screenshot {i+1}/3 saved: {screenshot_path}")
                                            except Exception as e:
                                                print(f"[COMBAT DETECTION] Failed to save screenshot {i+1}: {e}")
                                        
                                        embed = {
                                            "title": f"⚔️🚨 COMBAT DETECTED! 🚨⚔️ (Alert {i+1}/3)",
                                            "description": f"**Combat indicator found on screen!**\n\n{action_text}",
                                            "color": 15158332,  # Red color
                                            "fields": [
                                                {
                                                    "name": "🎯 Confidence",
                                                    "value": f"{combat_location['confidence']:.1%}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "📍 Location",
                                                    "value": f"({combat_location['x']}, {combat_location['y']})",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "🔔 Detection #",
                                                    "value": f"{self.combat_detection_count}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "🕐 Session Duration",
                                                    "value": f"{session_minutes}m {session_seconds}s",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "📊 Total Catches",
                                                    "value": f"{self.total_catches}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "⏱️ Action",
                                                    "value": f"{'⚡ INSTANT KILL' if (COMBAT_AUTO_KILL_ROBLOX and COMBAT_INSTANT_KILL) else ('AUTO-KILL in ' + str(COMBAT_KILL_DELAY) + 's' if COMBAT_AUTO_KILL_ROBLOX else 'Manual intervention required')}",
                                                    "inline": True
                                                }
                                            ],
                                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                                        }
                                        
                                        # Send message with screenshot
                                        if screenshot_saved and screenshot_path:
                                            send_discord_notification(self.webhook_url, mention, embed, image_path=screenshot_path)
                                            
                                            # Delete screenshot after sending
                                            if DELETE_SCREENSHOTS_AFTER_DISCORD:
                                                try:
                                                    if os.path.exists(screenshot_path):
                                                        os.remove(screenshot_path)
                                                except Exception as e:
                                                    print(f"[COMBAT DETECTION] Failed to delete screenshot {i+1}: {e}")
                                        else:
                                            # Send without screenshot if capture/save failed
                                            send_discord_notification(self.webhook_url, mention, embed)
                                        
                                        # Small delay between messages to ensure they arrive in order
                                        time.sleep(0.5)
                                    
                                    print(f"[COMBAT DETECTION] 🚨 Sent 3 urgent Discord notifications with fresh screenshots!")
                            
                            # Send alert in background thread
                            threading.Thread(target=send_combat_alert, daemon=True).start()
                            self.combat_notification_sent = True
                            
                            # Set combat flag to pause fishing/eating
                            self.combat_active = True
                            print("[COMBAT DETECTION] ⚠️  Fishing and eating paused - combat mode active")
                            
                            # Start random movement thread to avoid suspicion
                            def random_movement_worker():
                                """Randomly move WASD to appear active during combat"""
                                import random
                                print("[COMBAT MOVEMENT] Thread started - moving randomly to avoid suspicion")
                                
                                # Virtual key codes for WASD
                                VK_W = 0x57
                                VK_A = 0x41
                                VK_S = 0x53
                                VK_D = 0x44
                                movement_keys = [VK_W, VK_A, VK_S, VK_D]
                                
                                while self.combat_active and not self.stop_combat_detection.is_set():
                                    try:
                                        # Pick random direction
                                        key = random.choice(movement_keys)
                                        key_name = {VK_W: 'W', VK_A: 'A', VK_S: 'S', VK_D: 'D'}[key]
                                        
                                        # Press and hold for random duration
                                        hold_duration = random.uniform(0.3, 1.2)
                                        
                                        if self.debug:
                                            print(f"[COMBAT MOVEMENT] Pressing {key_name} for {hold_duration:.2f}s")
                                        
                                        # Press key down
                                        scan_code = ctypes.windll.user32.MapVirtualKeyW(key, 0)
                                        ctypes.windll.user32.keybd_event(key, scan_code, 0, 0)
                                        time.sleep(hold_duration)
                                        
                                        # Release key
                                        ctypes.windll.user32.keybd_event(key, scan_code, 2, 0)  # 2 = KEYEVENTF_KEYUP
                                        
                                        # Random pause between movements
                                        time.sleep(random.uniform(0.5, 2.0))
                                        
                                    except Exception as e:
                                        if self.debug:
                                            print(f"[COMBAT MOVEMENT ERROR] {e}")
                                        time.sleep(1)
                                
                                print("[COMBAT MOVEMENT] Thread stopped")
                            
                            # Start movement thread
                            threading.Thread(target=random_movement_worker, daemon=True).start()
                        
                        # Check if we should kill Roblox process
                        elapsed_since_detection = time.time() - self.combat_detected_time
                        
                        # Skip kill actions if script is paused
                        if script_paused:
                            if self.debug:
                                print("[COMBAT DETECTION] ⏸️ Script is paused - skipping Roblox kill actions")
                            time.sleep(2)
                            continue
                        
                        # Instant kill: kill immediately without delay
                        if COMBAT_AUTO_KILL_ROBLOX and COMBAT_INSTANT_KILL:
                            print(f"\n{'='*60}")
                            print(f"[COMBAT DETECTION] ⚠️  INSTANT KILL ENABLED - TERMINATING IMMEDIATELY!")
                            print(f"[COMBAT DETECTION] 🔴 TERMINATING ROBLOX PROCESS...")
                            print(f"{'='*60}\n")
                            
                            # Kill Roblox process
                            try:
                                import psutil
                                killed = False
                                
                                for proc in psutil.process_iter(['name', 'pid']):
                                    if proc.info['name'] and 'roblox' in proc.info['name'].lower():
                                        print(f"[COMBAT DETECTION] Killing process: {proc.info['name']} (PID: {proc.info['pid']})")
                                        proc.kill()
                                        killed = True
                                
                                if killed:
                                    print("[COMBAT DETECTION] ✅ Roblox process terminated successfully (INSTANT)")
                                    
                                    # Send final Discord notification
                                    if ENABLE_DISCORD_NOTIFICATIONS:
                                        mention = ""
                                        if DISCORD_MENTION_USER_ID and MENTION_ON_AUTO_KILL:
                                            mention = f"<@{DISCORD_MENTION_USER_ID}>\n"
                                        
                                        embed = {
                                            "title": "🔴 Roblox Process Terminated (INSTANT KILL)",
                                            "description": "Combat detected - Roblox was instantly terminated without delay",
                                            "color": 16711680,  # Bright red
                                            "fields": [
                                                {
                                                    "name": "⚡ Kill Mode",
                                                    "value": "INSTANT (no delay)",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "🔔 Combat Detection #",
                                                    "value": f"{self.combat_detection_count}",
                                                    "inline": True
                                                }
                                            ],
                                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                                        }
                                        send_discord_notification(self.webhook_url, mention, embed)
                                else:
                                    print("[COMBAT DETECTION] ⚠️  No Roblox process found to kill")
                                    
                            except Exception as e:
                                print(f"[COMBAT DETECTION] ❌ Failed to kill Roblox process: {e}")
                                import traceback
                                traceback.print_exc()
                            
                            # Stop combat detection after instant killing
                            break
                        
                        # Delayed kill: wait for configured delay before killing
                        elif COMBAT_AUTO_KILL_ROBLOX and elapsed_since_detection >= COMBAT_KILL_DELAY:
                            print(f"\n{'='*60}")
                            print(f"[COMBAT DETECTION] ⚠️  Combat still active after {COMBAT_KILL_DELAY}s!")
                            print(f"[COMBAT DETECTION] 🔴 TERMINATING ROBLOX PROCESS...")
                            print(f"{'='*60}\n")
                            
                            # Kill Roblox process
                            try:
                                import psutil
                                killed = False
                                
                                for proc in psutil.process_iter(['name', 'pid']):
                                    if proc.info['name'] and 'roblox' in proc.info['name'].lower():
                                        print(f"[COMBAT DETECTION] Killing process: {proc.info['name']} (PID: {proc.info['pid']})")
                                        proc.kill()
                                        killed = True
                                
                                if killed:
                                    print("[COMBAT DETECTION] ✅ Roblox process terminated successfully")
                                    
                                    # Send final Discord notification
                                    if ENABLE_DISCORD_NOTIFICATIONS:
                                        mention = ""
                                        if DISCORD_MENTION_USER_ID and MENTION_ON_AUTO_KILL:
                                            mention = f"<@{DISCORD_MENTION_USER_ID}>\n"
                                        
                                        embed = {
                                            "title": "🔴 Roblox Process Terminated",
                                            "description": f"Combat was still active after {COMBAT_KILL_DELAY}s - Roblox has been closed.",
                                            "color": 10038562,  # Dark red
                                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                                        }
                                        send_discord_notification_async(self.webhook_url, mention, embed)
                                    
                                    # Trigger emergency stop
                                    emergency_stop = True
                                else:
                                    print("[COMBAT DETECTION] ⚠️  No Roblox process found to terminate")
                                    
                            except Exception as e:
                                print(f"[COMBAT DETECTION] ❌ Failed to kill Roblox process: {e}")
                                import traceback
                                traceback.print_exc()
                            
                            # Stop combat detection after killing
                            break
                    
                    else:
                        # Combat not detected - reset timer and resume macro
                        if self.combat_detected_time is not None:
                            print(f"[COMBAT DETECTION] ✅ Combat indicator cleared")
                            self.combat_detected_time = None
                            self.combat_notification_sent = False
                            
                            # Resume fishing and eating
                            self.combat_active = False
                            print("[COMBAT DETECTION] ✅ Fishing and eating resumed - combat ended")
                
                # Check every 2 seconds (no need to spam)
                time.sleep(2)
                
            except Exception as e:
                if not self.stop_combat_detection.is_set():
                    print(f"[COMBAT DETECTION ERROR] {e}")
                    import traceback
                    traceback.print_exc()
                time.sleep(2)
        
        print("[COMBAT DETECTION] Thread stopped")
    
    def start_combat_detection(self):
        """Start the combat detection thread"""
        if self.has_combat_detector:
            combat_thread = threading.Thread(target=self.combat_detection_worker, daemon=True)
            combat_thread.start()
            return combat_thread
        return None
    
    def detection_worker(self, point_detected_time=None):
        """Background thread that continuously checks for caught fish"""
        thread_start_time = time.time()
        if self.debug:
            print("[DETECTION THREAD] Started - will check for caught visuals in background")
        
        check_counter = 0
        last_debug_print = time.time()
        capture_errors = 0
        
        while not self.stop_detection.is_set():
            try:
                # Capture screenshot with timing
                capture_start = time.time()
                screenshot = self.window_capture.capture_window()
                capture_time = time.time() - capture_start
                
                if screenshot is not None and self.has_caught_detector:
                    check_counter += 1
                    self.detection_check_count = check_counter
                    
                    # Debug: Print status every 5 seconds
                    if self.debug and (time.time() - last_debug_print) >= 5.0:
                        elapsed = time.time() - thread_start_time
                        avg_capture_time = capture_time * 1000  # Convert to ms
                        print(f"[DETECTION THREAD] Alive - {check_counter} checks in {elapsed:.1f}s "
                              f"(~{check_counter/elapsed:.1f} checks/sec) | "
                              f"Last capture: {avg_capture_time:.0f}ms")
                        last_debug_print = time.time()
                    
                    # Check all caught detectors with VERBOSE logging
                    detection_start = time.time()
                    max_confidences = []  # Track all confidence scores
                    highest_confidence = 0.0
                    highest_conf_name = ""
                    
                    for img_name, detector in self.caught_detectors:
                        if self.stop_detection.is_set():
                            if self.debug:
                                print(f"[DETECTION THREAD] Stop signal received, exiting...")
                            break
                        
                        # Perform template matching with debug to see max confidence
                        result = cv2.matchTemplate(screenshot, detector.template, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                        max_confidences.append((img_name.split('/')[-1], max_val))
                        
                        # Track highest confidence
                        if max_val > highest_confidence:
                            highest_confidence = max_val
                            highest_conf_name = img_name.split('/')[-1]
                        
                        # Check if it meets threshold
                        if max_val >= detector.confidence:
                            detection_time = time.time() - detection_start
                            elapsed = time.time() - thread_start_time
                            
                            # Calculate duration from point detection to catch detection
                            point_to_catch_duration = time.time() - point_detected_time if point_detected_time else elapsed
                            
                            # Calculate duration between catches (time since last catch)
                            time_since_last_catch = time.time() - self.last_catch_time
                            
                            # Track catch statistics
                            detector_name = img_name.split('/')[-1].replace('.png', '').replace('_arcane_odyssey', '')
                            self.total_catches += 1
                            self.catch_history.append((detector_name, max_val, time.time()))
                            self.last_catch_time = time.time()  # Update last catch time
                            
                            # Reset consecutive no-detection counter on successful catch
                            self.consecutive_no_detection = 0
                            
                            print(f"[DETECTION THREAD] ✓ Found {img_name}! Confidence: {max_val:.2f}")
                            print(f"[DETECTION THREAD] Detection took {elapsed:.2f}s with {check_counter} checks")
                            print(f"[DETECTION THREAD] Last check: capture={capture_time*1000:.0f}ms, detection={detection_time*1000:.0f}ms")
                            
                            # Start background thread for screenshot and notification
                            threading.Thread(
                                target=self._save_and_notify_catch,
                                args=(screenshot, img_name, max_val, detector_name, time_since_last_catch, check_counter),
                                daemon=True
                            ).start()
                            
                            self.caught_flag.set()  # Signal main thread
                            self.detection_queue.put({
                                'type': 'caught',
                                'image': img_name,
                                'location': {'x': max_loc[0], 'y': max_loc[1], 'confidence': max_val},
                                'checks': check_counter,
                                'elapsed': elapsed,
                                'confidence_met_threshold': True  # Flag indicating detection was successful
                            })
                            if self.debug:
                                print(f"[DETECTION THREAD] Exiting after successful detection")
                            return  # Exit thread after first detection
                    
                    # Save screenshot if confidence is close to threshold (0.40-0.49)
                        # if 0.40 <= highest_confidence < detector.confidence:
                        #     timestamp = time.strftime("%Y%m%d_%H%M%S")
                        #     detector_name = highest_conf_name.replace('.png', '')  # e.g., "caught", "fish", "treasure"
                        #     screenshot_path = f"assets/screenshots/close_{detector_name}_{timestamp}_conf{highest_confidence:.2f}.png"
                        #     try:
                        #         import os
                        #         os.makedirs("assets/screenshots", exist_ok=True)
                        #         cv2.imwrite(screenshot_path, screenshot)
                        #         print(f"[DETECTION THREAD] 📸 Close match saved: {screenshot_path} ({highest_conf_name}: {highest_confidence:.2f})")
                        #     except Exception as e:
                        #         print(f"[DETECTION THREAD] Failed to save screenshot: {e}")
                    
                    # Show confidence scores every check in debug mode
                    if self.debug and check_counter % 5 == 0:
                        conf_str = " | ".join([f"{name}:{conf:.2f}" for name, conf in max_confidences])
                        print(f"[DETECTION CHECK #{check_counter}] Confidences: {conf_str}")
                    
                    # Send screenshot to Discord if no detector meets threshold (every 10 checks to avoid spam)
                    # Run in background thread to avoid blocking detection
                    if check_counter % 10 == 0 and highest_confidence > 0 and ENABLE_DISCORD_NOTIFICATIONS:
                        # Start background thread with method call
                        threading.Thread(
                            target=self._send_threshold_warning,
                            args=(screenshot, highest_conf_name, highest_confidence, max_confidences, check_counter),
                            daemon=True
                        ).start()
                    
                else:
                    capture_errors += 1
                    if capture_errors > 3 and self.debug:
                        print(f"[DETECTION THREAD WARNING] {capture_errors} failed captures")
                
                # Don't sleep - check as fast as possible
                # The capture itself provides natural throttling (~100-200ms per check)
                # time.sleep(0.1)  # REMOVED - was limiting us to 10 checks/sec max
                
            except Exception as e:
                if not self.stop_detection.is_set():
                    print(f"[DETECTION THREAD ERROR] {e}")
                    import traceback
                    traceback.print_exc()
        
        elapsed = time.time() - thread_start_time
        if self.debug:
            print(f"[DETECTION THREAD] Stopped after {check_counter} checks in {elapsed:.1f}s")
            if capture_errors > 0:
                print(f"[DETECTION THREAD] Had {capture_errors} capture errors")
        
    def run(self):
        """Main macro loop"""
        global emergency_stop, input_currently_blocked, script_paused
        
        print(f"Starting fishing macro for {self.fishing_time} seconds...")
        print("The Roblox window can be in the background!")
        print("-" * 50)
        
        # Start combat detection thread
        combat_thread = self.start_combat_detection()
        if combat_thread:
            print("[INFO] Combat detection thread started")
            print()
        
        # Track last pause notification time
        last_pause_screenshot_time = 0
        pause_screenshot_interval = 60  # Send screenshot every 60 seconds while paused
        
        while time.time() < self.end_time and not emergency_stop:
            # Check emergency stop at the very start of each iteration
            if emergency_stop:
                print("[STOP] Emergency stop detected at start of loop, exiting...")
                break
            
            # Check if script is paused
            if script_paused:
                if self.debug:
                    print("[DEBUG] Script paused - waiting...")
                
                # Send periodic screenshot while paused
                current_time = time.time()
                if current_time - last_pause_screenshot_time >= pause_screenshot_interval:
                    last_pause_screenshot_time = current_time
                    
                    # Capture screenshot
                    screenshot = self.window_capture.capture_window()
                    if screenshot is not None:
                        # Send to Discord in background thread
                        def send_pause_screenshot():
                            try:
                                # Save screenshot
                                screenshot_saved = False
                                screenshot_path = None
                                
                                if SAVE_DETECTION_SCREENSHOTS:
                                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                                    screenshot_path = f"{SCREENSHOT_FOLDER}/paused_{timestamp}.png"
                                    
                                    try:
                                        import os
                                        os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
                                        cv2.imwrite(screenshot_path, screenshot)
                                        screenshot_saved = True
                                        print(f"[PAUSE] 📸 Screenshot saved: {screenshot_path}")
                                    except Exception as e:
                                        print(f"[PAUSE] Failed to save screenshot: {e}")
                                
                                # Calculate pause duration
                                pause_duration = current_time - self.macro_start_time
                                pause_minutes = int(pause_duration // 60)
                                pause_seconds = int(pause_duration % 60)
                                
                                # Send Discord notification
                                if ENABLE_DISCORD_NOTIFICATIONS and self.webhook_url:
                                    embed = {
                                        "title": "⏸️ Script Still Paused - Status Update",
                                        "description": "Periodic screenshot while fishing macro is paused",
                                        "color": 16776960,  # Yellow
                                        "fields": [
                                            {
                                                "name": "📌 Status",
                                                "value": "Paused - Press Ctrl+. to resume",
                                                "inline": True
                                            },
                                            {
                                                "name": "⏱️ Session Duration",
                                                "value": f"{pause_minutes}m {pause_seconds}s",
                                                "inline": True
                                            },
                                            {
                                                "name": "📊 Total Catches",
                                                "value": f"{self.total_catches}",
                                                "inline": True
                                            },
                                            {
                                                "name": "🎯 Total Detections",
                                                "value": f"{self.detection_count}",
                                                "inline": True
                                            },
                                            {
                                                "name": "🔄 Auto-Cast Count",
                                                "value": f"{self.auto_cast_count}",
                                                "inline": True
                                            },
                                            {
                                                "name": "⚠️ Consecutive No-Detections",
                                                "value": f"{self.consecutive_no_detection}/5",
                                                "inline": True
                                            }
                                        ],
                                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                                    }
                                    
                                    if screenshot_saved and screenshot_path:
                                        send_discord_notification(self.webhook_url, "", embed, image_path=screenshot_path)
                                        
                                        # Delete screenshot after sending
                                        if DELETE_SCREENSHOTS_AFTER_DISCORD:
                                            try:
                                                if os.path.exists(screenshot_path):
                                                    os.remove(screenshot_path)
                                            except Exception as e:
                                                print(f"[PAUSE] Failed to delete screenshot: {e}")
                                    else:
                                        send_discord_notification(self.webhook_url, "", embed)
                                    
                                    print(f"[PAUSE] 📤 Status update sent to Discord")
                            
                            except Exception as e:
                                print(f"[PAUSE] Error sending pause screenshot: {e}")
                        
                        threading.Thread(target=send_pause_screenshot, daemon=True).start()
                
                time.sleep(1)
                continue
            
            # Capture window
            screenshot = self.window_capture.capture_window()
            
            if screenshot is None:
                print("Failed to capture window. Retrying...")
                time.sleep(1)
                continue
            
            # Check emergency stop after capture
            if emergency_stop:
                print("[STOP] Emergency stop detected after capture, exiting...")
                break
            
            # Look for fishing point indicator first
            point_location = self.point_detector.find_in_image(screenshot)
            
            # Check if it's time to eat (based on random interval)
            if not point_location and self.should_eat_now():
                if self.debug:
                    print("[DEBUG] No active fishing detected, time to eat")
                
                # Only eat if not in combat and not paused
                if not self.combat_active and not script_paused:
                    self.eat_food()
                    # Wait a bit after eating before continuing
                    time.sleep(2)
                else:
                    if self.debug:
                        if self.combat_active:
                            print("[DEBUG] Skipping eating - combat active")
                        if script_paused:
                            print("[DEBUG] Skipping eating - script paused")
                
                continue
            
            # Skip fishing detection if combat is active or script is paused
            if self.combat_active or script_paused:
                if self.debug:
                    if self.combat_active:
                        print("[DEBUG] Skipping fishing - combat active")
                    if script_paused:
                        print("[DEBUG] Skipping fishing - script paused")
                time.sleep(1)
                continue
            
            # Process fishing point if detected
            if point_location:
                self.detection_count += 1
                self.last_detection_time = time.time()
                
                print(f"[DETECTED] Point found at ({point_location['x']}, {point_location['y']}) "
                      f"- Confidence: {point_location['confidence']:.2f}")
                
                # Save screenshot for later (in case we need to send it due to timeout or low confidence)
                screenshot_for_notification = screenshot.copy()
                point_location_for_notification = point_location.copy()
                
                # Get window center for clicking - we'll click at center instead of point location
                _, _, w, h = self.window_capture.get_window_rect()
                center_x = w // 2
                center_y = h // 2
                
                if self.debug:
                    print(f"[DEBUG] Point detected, but will click at screen center ({center_x}, {center_y})")
                
                # Save original mouse position to restore later
                original_mouse_pos = win32api.GetCursorPos()
                if self.debug:
                    print(f"[DEBUG] Saved original mouse position: {original_mouse_pos}")
                
                print("[INFO] Blocking user input during fishing sequence...")
                
                # Block user input for the entire fishing sequence
                input_currently_blocked = True
                input_block_start_time = time.time()  # Track when blocking started
                input_blocked = block_input()
                if self.debug:
                    print(f"[DEBUG] BlockInput API returned: {input_blocked}")
                    if not input_blocked:
                        print("[DEBUG] WARNING: Failed to block input - may require admin privileges")
                
                try:
                    # START DETECTION THREAD
                    self.caught_flag.clear()
                    self.stop_detection.clear()
                    self.detection_check_count = 0
                    point_detected_time = time.time()  # Record when fishing point was detected
                    detection_thread = threading.Thread(target=lambda: self.detection_worker(point_detected_time), daemon=True)
                    detection_thread.start()
                    
                    if self.debug:
                        print("[DEBUG] Detection thread started in background")
                    
                    # Start auto-clicking - no detection overhead!
                    auto_clicker_start_time = time.time()
                    click_duration = 0
                    clicks_in_loop = 0
                    previous_window = None  # Track previous window to restore later
                    
                    print("[CLICKING] Starting high-speed clicking with parallel background detection...")
                    
                    while True:
                        # Check emergency stop OR pause before each click - CRITICAL for responsiveness
                        if emergency_stop:
                            print("[STOP] Emergency stop detected during clicking!")
                            print("[STOP] Breaking out of click loop immediately...")
                            break
                        
                        # Check if script is paused - stop clicking immediately
                        if script_paused:
                            print("[PAUSE] Script paused during clicking - stopping clicks immediately!")
                            print(f"[PAUSE] Completed {clicks_in_loop} clicks before pause")
                            self.fish_just_caught = False  # Don't count as caught
                            break
                        
                        # Check if detection thread found caught visual
                        if self.caught_flag.is_set():
                            try:
                                detection_result = self.detection_queue.get_nowait()
                                print(f"[CAUGHT] ✓ {detection_result['image']} detected by background thread!")
                                print(f"[CAUGHT] Confidence: {detection_result['location']['confidence']:.2f}")
                                print(f"[CAUGHT] Stopping after {clicks_in_loop} clicks ({click_duration:.1f}s)")
                                print(f"[CAUGHT] Detection stats: {detection_result['checks']} checks in {detection_result['elapsed']:.2f}s")
                                self.fish_just_caught = True
                                
                                # Check if detection confidence met threshold
                                if not detection_result.get('confidence_met_threshold', False):
                                    # Detection was below threshold - send screenshot
                                    print(f"[CAUGHT] Detection below threshold - sending screenshot to Discord")
                                    threading.Thread(
                                        target=self._save_point_screenshot_and_notify,
                                        args=(screenshot_for_notification, point_location_for_notification, "timeout_or_low_confidence"),
                                        daemon=True
                                    ).start()
                                
                                if previous_window:
                                    time.sleep(0.2)
                                    self.window_capture.restore_window(previous_window)
                                    if self.debug:
                                        print(f"[DEBUG] Restored previous window")
                                break
                            except queue.Empty:
                                if self.debug:
                                    print(f"[DEBUG] Caught flag set but queue empty - race condition")
                                pass
                        
                        # FAST CLICKING - No detection overhead!
                        debug_this_click = self.debug and clicks_in_loop == 0
                        if clicks_in_loop == 0:
                            # First click - capture previous window
                            previous_window = self.window_capture.send_click(center_x, center_y, debug=debug_this_click)
                        else:
                            self.window_capture.send_click(center_x, center_y, debug=False)
                        
                        self.click_count += 1
                        clicks_in_loop += 1
                        
                        # Check emergency stop or pause after click
                        if emergency_stop:
                            print("[STOP] Emergency stop detected after click!")
                            break
                        
                        if script_paused:
                            print("[PAUSE] Script paused during clicking - stopping!")
                            self.fish_just_caught = False  # Don't count as caught
                            break
                        
                        click_duration = time.time() - auto_clicker_start_time
                        input_block_duration = time.time() - input_block_start_time
                        
                        # Stop after configured max clicking duration
                        if click_duration > MAX_CLICKING_DURATION:
                            print(f"[{MAX_CLICKING_DURATION}s TIMEOUT] Stopped clicking after {MAX_CLICKING_DURATION} seconds ({clicks_in_loop} clicks)")
                            print(f"[{MAX_CLICKING_DURATION}s TIMEOUT] Background detection performed {self.detection_check_count} checks")
                            self.fish_just_caught = True  # Assume fish was caught
                            
                            # Send screenshot and notification since we hit timeout (fish detection failed)
                            print(f"[{MAX_CLICKING_DURATION}s TIMEOUT] Sending screenshot to Discord - detection may have failed")
                            threading.Thread(
                                target=self._save_point_screenshot_and_notify,
                                args=(screenshot_for_notification, point_location_for_notification, "timeout_or_low_confidence"),
                                daemon=True
                            ).start()
                            
                            # Restore previous window after timeout
                            if previous_window:
                                time.sleep(0.2)
                                self.window_capture.restore_window(previous_window)
                                if self.debug:
                                    print(f"[DEBUG] Restored previous window after 20s timeout")
                            break
                        
                        # Show progress every 100 clicks
                        if self.debug and clicks_in_loop % 100 == 0:
                            print(f"[DEBUG] {clicks_in_loop} clicks, {click_duration:.1f}s, "
                                  f"detection_thread_alive={detection_thread.is_alive()}, "
                                  f"detection_checks={self.detection_check_count}")
                            # Re-block input periodically to ensure it stays blocked (only if under safety timeout)
                            if input_blocked and input_block_duration < CRITICAL_SAFETY_TIMEOUT:
                                block_input()
                        
                        # CRITICAL SAFETY: Auto-unblock input after configured timeout regardless of state
                        if input_block_duration > CRITICAL_SAFETY_TIMEOUT:
                            print(f"\n[CRITICAL SAFETY] Input has been blocked for {CRITICAL_SAFETY_TIMEOUT}+ seconds!")
                            print(f"[CRITICAL SAFETY] Auto-unblocking to prevent permanent lockout!")
                            input_currently_blocked = False
                            unblock_input()
                            print(f"[CRITICAL SAFETY] Input force-unblocked after {input_block_duration:.1f}s")
                            # Restore mouse and window
                            safe_set_cursor_pos(original_mouse_pos)
                            if previous_window:
                                self.window_capture.restore_window(previous_window)
                            break
                        
                        # Configurable click speed
                        time.sleep(CLICK_DELAY)
                    
                    # STOP DETECTION THREAD
                    self.stop_detection.set()
                    if detection_thread.is_alive():
                        detection_thread.join(timeout=2)
                        if self.debug:
                            print(f"[DEBUG] Detection thread stopped")
                    
                    # If script was paused during clicking, skip all post-click processing
                    # Input will be unblocked in the finally block
                    if not script_paused:
                        if self.debug:
                            print("[DEBUG] Sending reset clicks...")
                        time.sleep(4)
                        
                        # Check if it's time to eat after catching a fish (good time to eat!)
                        if self.fish_just_caught:
                            if self.debug:
                                print("[DEBUG] Fish just caught - checking if it's time to eat...")
                            
                            if self.should_eat_now():
                                if self.debug:
                                    print("[DEBUG] Time to eat after catching fish!")
                                self.eat_food()
                                # Skip reset clicks since eat_food already re-equips rod
                                self.fish_just_caught = False
                                # Restore original mouse position before continuing
                                safe_set_cursor_pos(original_mouse_pos)
                                if self.debug:
                                    print(f"[DEBUG] Restored original mouse position: {original_mouse_pos}")
                                continue
                            
                            self.fish_just_caught = False
                        
                        # Normal reset clicks at center
                        prev_win = self.window_capture.send_click(center_x, center_y, debug=self.debug)
                        self.click_count += 1
                        
                        time.sleep(1)
                        self.window_capture.send_click(center_x, center_y, debug=self.debug, return_previous_window=True)
                        self.click_count += 1
                        
                        # Restore previous window after reset clicks
                        if prev_win:
                            time.sleep(0.2)
                            self.window_capture.restore_window(prev_win)
                            if self.debug:
                                print("[DEBUG] Restored previous window after reset")
                    else:
                        print("[PAUSE] Skipping reset clicks and post-processing - script is paused")
                        if previous_window:
                            self.window_capture.restore_window(previous_window)
                            if self.debug:
                                print("[DEBUG] Restored previous window before pause")
                
                finally:
                    # STOP DETECTION THREAD if still running
                    self.stop_detection.set()
                    if 'detection_thread' in locals() and detection_thread.is_alive():
                        detection_thread.join(timeout=2)
                        if self.debug:
                            print(f"[DEBUG] Detection thread cleanup completed")
                    
                    # Always unblock input even if there's an error
                    input_currently_blocked = False
                    unblock_result = unblock_input()
                    if self.debug:
                        print(f"[DEBUG] UnblockInput API returned: {unblock_result}")
                    print("[INFO] User input unblocked - you can use your keyboard/mouse again")
                    
                    # Restore original mouse position after fishing sequence completes
                    safe_set_cursor_pos(original_mouse_pos)
                    if self.debug:
                        print(f"[DEBUG] Restored original mouse position: {original_mouse_pos}")
                    else:
                        print(f"[INFO] Mouse position restored to original location")
                
            else:
                # No detection - check if we need to cast rod
                time_since_last_detection = time.time() - self.last_detection_time
                
                if time_since_last_detection > self.no_detection_timeout:
                    self.auto_cast_count += 1
                    self.consecutive_no_detection += 1  # Increment consecutive no-detection counter
                    print(f"[AUTO-CAST] No detection for {self.no_detection_timeout}s. Casting rod... (Auto-cast #{self.auto_cast_count}, Consecutive: {self.consecutive_no_detection}/5)")
                    
                    # Capture screenshot for Discord notification
                    screenshot_saved = False
                    screenshot_path = None
                    
                    if SAVE_DETECTION_SCREENSHOTS and screenshot is not None:
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        screenshot_path = f"{SCREENSHOT_FOLDER}/auto_cast_{timestamp}_count{self.auto_cast_count}.png"
                        
                        try:
                            import os
                            os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
                            cv2.imwrite(screenshot_path, screenshot)
                            screenshot_saved = True
                            print(f"[AUTO-CAST] 📸 Screenshot saved: {screenshot_path}")
                        except Exception as e:
                            print(f"[AUTO-CAST] Failed to save screenshot: {e}")
                    
                    # Click center of screen to cast
                    _, _, w, h = self.window_capture.get_window_rect()
                    center_x = w // 2
                    center_y = h // 2
                    
                    if self.debug:
                        print(f"[DEBUG] Auto-cast at center ({center_x}, {center_y})")
                    
                    self.window_capture.send_click(center_x, center_y, debug=self.debug)
                    self.click_count += 1
                    self.last_detection_time = time.time()
                    
                    # Send Discord notification EVERY TIME auto-cast happens
                    if ENABLE_DISCORD_NOTIFICATIONS:
                        # Check if this triggers auto-pause (5 consecutive no-detections)
                        is_milestone = self.consecutive_no_detection >= 5
                        
                        # Build mention string (only for milestones)
                        mention = ""
                        if is_milestone:
                            if DISCORD_MENTION_USER_ID:
                                mention = f"<@{DISCORD_MENTION_USER_ID}>\n"
                            print(f"[AUTO-CAST] 🚨 ALERT: {self.consecutive_no_detection} consecutive no-detections - triggering auto-pause with mention")
                        else:
                            print(f"[AUTO-CAST] Sending Discord notification (#{self.auto_cast_count}, consecutive: {self.consecutive_no_detection}/5)")
                        
                        # Calculate session duration
                        session_duration = time.time() - self.macro_start_time
                        session_minutes = int(session_duration // 60)
                        session_seconds = int(session_duration % 60)
                        
                        # Different styling for milestones vs regular notifications
                        if is_milestone:
                            # MILESTONE: Special alert with mention (5 consecutive no-detections)
                            embed = {
                                "title": "🚨 ⚠️ CONSECUTIVE NO-DETECTION ALERT!",
                                "description": f"**{self.consecutive_no_detection} consecutive auto-casts without catching anything!**\n\n⚠️ No fish caught in the last {self.consecutive_no_detection} casts - something may be wrong.\n\n**⏸️ SCRIPT AUTO-PAUSED FOR INVESTIGATION**\n\n**This may indicate:**\n• Wrong fishing location\n• Detection images need updating\n• Low confidence threshold\n• Game lag or issues\n• Character moved from fishing spot\n\n**To resume:** Press **Ctrl+.** (period key)",
                                "color": 16711680,  # Red color for urgency
                            "fields": [
                                {
                                    "name": "⚠️ Consecutive No-Detections",
                                    "value": f"**{self.consecutive_no_detection}** (Auto-pause triggered!)",
                                    "inline": True
                                },
                                {
                                    "name": "🔄 Total Auto-Cast Count",
                                    "value": f"{self.auto_cast_count}",
                                    "inline": True
                                },
                                {
                                    "name": "⏱️ Time Since Last Detection",
                                    "value": f"{time_since_last_detection:.1f}s",
                                    "inline": True
                                },
                                {
                                    "name": "⏳ Detection Timeout",
                                    "value": f"{self.no_detection_timeout}s",
                                    "inline": True
                                },
                                {
                                    "name": "🕐 Session Duration",
                                    "value": f"{session_minutes}m {session_seconds}s",
                                    "inline": True
                                },
                                {
                                    "name": "📊 Total Catches",
                                    "value": f"{self.total_catches}",
                                    "inline": True
                                },
                                {
                                    "name": "🎯 Total Detections",
                                    "value": f"{self.detection_count}",
                                    "inline": True
                                }
                            ],
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                        }
                        else:
                            # REGULAR: Standard notification without mention
                            embed = {
                                "title": "🎣 Auto-Cast Triggered",
                                "description": f"No fish bite detected for {self.no_detection_timeout}s - automatically re-casting rod\n\n⚠️ Consecutive no-detections: **{self.consecutive_no_detection}/5**",
                                "color": 16744272,  # Orange color
                                "fields": [
                                    {
                                        "name": "⚠️ Consecutive No-Detections",
                                        "value": f"**{self.consecutive_no_detection}**/5",
                                        "inline": True
                                    },
                                    {
                                        "name": "🔄 Total Auto-Cast Count",
                                        "value": f"{self.auto_cast_count}",
                                        "inline": True
                                    },
                                    {
                                        "name": "⏱️ Time Since Last Detection",
                                        "value": f"{time_since_last_detection:.1f}s",
                                        "inline": True
                                    },
                                    {
                                        "name": "⏳ Detection Timeout",
                                        "value": f"{self.no_detection_timeout}s",
                                        "inline": True
                                    },
                                    {
                                        "name": "🕐 Session Duration",
                                        "value": f"{session_minutes}m {session_seconds}s",
                                        "inline": True
                                    },
                                    {
                                        "name": "📊 Total Catches",
                                        "value": f"{self.total_catches}",
                                        "inline": True
                                    },
                                    {
                                        "name": "🎯 Total Detections",
                                        "value": f"{self.detection_count}",
                                        "inline": True
                                    }
                                ],
                                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                            }
                        
                        # Send with screenshot if available
                        if screenshot_saved and screenshot_path:
                            send_discord_notification(self.webhook_url, mention, embed, image_path=screenshot_path)
                            
                            # Delete screenshot after sending
                            if DELETE_SCREENSHOTS_AFTER_DISCORD:
                                try:
                                    if os.path.exists(screenshot_path):
                                        os.remove(screenshot_path)
                                except Exception as e:
                                    print(f"[AUTO-CAST] Failed to delete screenshot: {e}")
                        else:
                            # Send without screenshot
                            send_discord_notification(self.webhook_url, mention, embed)
                        
                        # PAUSE SCRIPT when consecutive no-detections reach threshold (5)
                        if is_milestone:
                            script_paused = True
                            print("\n" + "=" * 70)
                            print("⏸️  SCRIPT AUTO-PAUSED - CONSECUTIVE NO-DETECTION THRESHOLD!")
                            print("=" * 70)
                            print(f"[AUTO-PAUSE] {self.consecutive_no_detection} consecutive auto-casts without catching anything")
                            print(f"[AUTO-PAUSE] Total auto-casts: {self.auto_cast_count}")
                            print(f"[AUTO-PAUSE] Script paused for investigation")
                            print(f"[AUTO-PAUSE] Press Ctrl+. (period) to RESUME fishing")
                            print("=" * 70 + "\n")
            
            # Status update
            remaining_time = int(self.end_time - time.time())
            if remaining_time % 10 == 0 and remaining_time > 0:
                print(f"[STATUS] Running... {remaining_time}s remaining | "
                      f"Detections: {self.detection_count} | Clicks: {self.click_count}")
            
            # Debug: Show loop is continuing
            if self.debug and remaining_time > 0:
                print(f"[DEBUG] Main loop iteration - {remaining_time}s remaining")
            
            time.sleep(0.25)
        
        # Print why we exited
        if emergency_stop:
            print("[EXIT] Stopped due to emergency stop")
        elif time.time() >= self.end_time:
            print("[EXIT] Stopped due to time duration completed")
        else:
            print("[EXIT] Stopped for unknown reason")
        
        print("-" * 50)
        print(f"Fishing macro completed!")
        print(f"Total detections: {self.detection_count}")
        print(f"Total clicks: {self.click_count}")
        if self.combat_detection_count > 0:
            print(f"Combat detections: {self.combat_detection_count}")
        
        # Stop combat detection thread
        self.stop_combat_detection.set()
        if combat_thread and combat_thread.is_alive():
            combat_thread.join(timeout=2)
            print("[CLEANUP] Combat detection thread stopped")
        
        # Ensure input is unblocked at the end
        if input_currently_blocked:
            unblock_input()
            input_currently_blocked = False
            print("[CLEANUP] Input unblocked on exit")


def main():
    """Entry point"""
    global emergency_stop, input_currently_blocked, config_phase_complete
    
    try:
        print("=" * 50)
        print("Roblox Arcane Odyssey - Background Fishing Macro")
        print("=" * 50)
        print()
        
        # Start emergency stop listener
        print("🚨 EMERGENCY STOP: Press Ctrl+Alt+M at any time to stop and unblock input!")
        print("⏸️  PAUSE SCRIPT: Press Ctrl+, to pause the script")
        print("▶️  RESUME SCRIPT: Press Ctrl+. to resume the script")
        print("-" * 50)
        listener_thread = start_emergency_listener()
        
        print()
        
        # Optional: Override Discord webhook URL
        webhook_url_override = None
        if ENABLE_DISCORD_NOTIFICATIONS:
            print("📱 Discord Webhook Configuration:")
            if DISCORD_WEBHOOK_URL:
                print(f"   Current webhook: {DISCORD_WEBHOOK_URL[:50]}...")
            else:
                print("   ⚠️  No webhook configured in config.py")
            print()
            webhook_input = input("Enter Discord webhook URL (press Enter to use config default): ").strip()
            if webhook_input:
                webhook_url_override = webhook_input
                print(f"✅ Using custom webhook: {webhook_url_override[:50]}...")
            else:
                print(f"✅ Using webhook from config.py")
            print()
        
        # Get fishing duration from user
        fishing_time = int(input("Enter in seconds how long should scan last: "))
        
        # Get eating configuration from user (with defaults from config)
        print()
        print(f"Eating configuration (defaults from config.py):")
        eating_count_input = input(f"Enter number of food items per eating session (default={DEFAULT_EATING_COUNT}): ").strip()
        eating_count = int(eating_count_input) if eating_count_input else DEFAULT_EATING_COUNT
        
        eating_interval_input = input(f"Enter eating interval in seconds (default={DEFAULT_EATING_INTERVAL}): ").strip()
        eating_interval = int(eating_interval_input) if eating_interval_input else DEFAULT_EATING_INTERVAL
        
        print(f"[INFO] Will eat {eating_count} food items every {eating_interval}s continuously throughout the session")
        
        # Ask if user wants debug mode
        debug_input = input("Enable debug mode? (y/n, default=y): ").strip().lower()
        debug_mode = debug_input != 'n'  # Default to yes
        
        # Configuration phase is complete - allow debug messages now
        config_phase_complete = True
        
        print()
        if debug_mode:
            print("[DEBUG MODE ENABLED] - Detailed click information will be shown")
            print()
        
        # Use webhook override if provided
        active_webhook_url = webhook_url_override if webhook_url_override else DISCORD_WEBHOOK_URL
        
        if ENABLE_DISCORD_NOTIFICATIONS:
            print("🔔 [DISCORD NOTIFICATIONS ENABLED]")
            print(f"    Webhook: {active_webhook_url[:50]}...")
            print()
        
        print("⚠️  IMPORTANT NOTES:")
        print("    1. Roblox window will be brought to foreground when clicking")
        print("    2. Your keyboard/mouse will be BLOCKED during fishing sequences")
        print("    3. This prevents your input from interfering with the macro")
        print("    4. Input will be unblocked after each fish is caught/escaped")
        print("    5. ⚠️ Run as Administrator for best results!")
        print("       - Required for input blocking to work")
        print("       - Required for keyboard hook (emergency stop during blocking)")
        print("    6. 🚨 Hotkeys available:")
        print("       - Ctrl+Alt+M: Emergency stop (exits program)")
        print("       - Ctrl+,: Pause script (temporary pause)")
        print("       - Ctrl+.: Resume script (continue fishing)")
        print("    7. Works immediately when input is NOT blocked")
        print("       - If hook installed: works even during blocking")
        print("       - If hook failed: stops after current fishing action completes")
        print()
        
        # Create and run macro (pass active webhook URL)
        macro = FishingMacro(fishing_time, eating_interval, eating_count, debug=debug_mode, webhook_url=active_webhook_url)
        
        # Send startup notification
        if ENABLE_DISCORD_NOTIFICATIONS:
            embed = {
                "title": "🎣 Fishing Macro Started!",
                "description": "Roblox Arcane Odyssey Fishing Bot is now active",
                "color": 3066993,  # Green color
                "fields": [
                    {
                        "name": "⏱️ Duration",
                        "value": f"{fishing_time // 60}m {fishing_time % 60}s" if fishing_time < 86400 else f"{fishing_time // 3600}h",
                        "inline": True
                    },
                    {
                        "name": "🍖 Eating Config",
                        "value": f"{eating_count}x every {eating_interval}s (continuous)",
                        "inline": True
                    },
                    {
                        "name": "🐛 Debug Mode",
                        "value": "Enabled" if debug_mode else "Disabled",
                        "inline": True
                    },
                    {
                        "name": "🔔 Notifications",
                        "value": "✅ Active",
                        "inline": True
                    }
                ],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            }
            # Send in background thread to avoid startup delay (use active webhook)
            send_discord_notification_async(active_webhook_url, "🚀 Bot Starting...", embed)
        
        macro.run()
        
        # Send completion notification
        if ENABLE_DISCORD_NOTIFICATIONS:
            session_duration = time.time() - macro.macro_start_time
            session_hours = int(session_duration // 3600)
            session_minutes = int((session_duration % 3600) // 60)
            
            # Get catch breakdown
            catch_types = {}
            for catch_name, conf, timestamp in macro.catch_history:
                catch_types[catch_name] = catch_types.get(catch_name, 0) + 1
            
            catch_breakdown = "\n".join([f"**{name.title()}**: {count}" for name, count in catch_types.items()]) or "No catches"
            
            embed = {
                "title": "🏁 Fishing Session Complete!",
                "description": f"Session ended after {session_hours}h {session_minutes}m",
                "color": 15158332,  # Red color
                "fields": [
                    {
                        "name": "📊 Total Catches",
                        "value": f"{macro.total_catches}",
                        "inline": True
                    },
                    {
                        "name": "🖱️ Total Clicks",
                        "value": f"{macro.click_count}",
                        "inline": True
                    },
                    {
                        "name": "🍖 Meals Eaten",
                        "value": f"{macro.eat_count}",
                        "inline": True
                    },
                    {
                        "name": "🐟 Catch Breakdown",
                        "value": catch_breakdown,
                        "inline": False
                    }
                ],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            }
            # Send in background thread - no need to wait for completion notification (use active webhook)
            send_discord_notification_async(active_webhook_url, "✅ Session Finished!", embed)
        
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Ctrl+C detected")
        # Ensure input is unblocked
        if input_currently_blocked:
            unblock_input()
            input_currently_blocked = False
            print("[CLEANUP] Input unblocked")
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("\nMake sure 'point.png' and 'caught.png' are in the same directory as this script!")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Final safety check - ensure input is ALWAYS unblocked
        if input_currently_blocked:
            unblock_input()
            input_currently_blocked = False
            print("[FINAL CLEANUP] Input unblocked")
        
        # Set emergency stop to terminate listener thread
        emergency_stop = True


if __name__ == "__main__":
    main()
