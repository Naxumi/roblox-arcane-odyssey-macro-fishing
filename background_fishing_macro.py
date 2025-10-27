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

# ============================================
# CONFIGURATION LOADING
# ============================================
# Try to load user configuration from config.py
# If not found, use default values and warn user
try:
    from config import (
        DISCORD_WEBHOOK_URL,
        ENABLE_DISCORD_NOTIFICATIONS,
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
        DETECTION_IMAGES
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
    }
# ============================================

# Emergency stop flag
emergency_stop = False
input_currently_blocked = False
keyboard_hook = None
ctrl_pressed = False
alt_pressed = False
m_pressed = False
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

def keyboard_hook_callback(nCode, wParam, lParam):
    """Low-level keyboard hook callback - this bypasses BlockInput!"""
    global emergency_stop, input_currently_blocked
    global ctrl_pressed, alt_pressed, m_pressed
    
    if nCode >= 0:
        kb_struct = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk_code = kb_struct.vkCode
        
        VK_CONTROL = 0x11
        VK_MENU = 0x12  # ALT key
        VK_M = 0x4D
        
        # Track key down/up
        if wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN:
            if vk_code == VK_CONTROL:
                ctrl_pressed = True
            elif vk_code == VK_MENU:
                alt_pressed = True
            elif vk_code == VK_M:
                m_pressed = True
            
            # Check for Ctrl+Alt+M combination
            if ctrl_pressed and alt_pressed and m_pressed:
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
        
        elif wParam == WM_KEYUP or wParam == WM_SYSKEYUP:
            # Track key releases
            if vk_code == VK_CONTROL:
                ctrl_pressed = False
            elif vk_code == VK_MENU:
                alt_pressed = False
            elif vk_code == VK_M:
                m_pressed = False
    
    # Call next hook in chain
    return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)

# Create callback function pointer
HOOKPROC = ctypes.CFUNCTYPE(c_long, ctypes.c_int, ctypes.c_int, ctypes.POINTER(c_long))
keyboard_hook_pointer = HOOKPROC(keyboard_hook_callback)

def emergency_stop_listener():
    """Listen for Ctrl+Alt+M using low-level keyboard hook (bypasses BlockInput!)"""
    global emergency_stop, keyboard_hook
    global ctrl_pressed, alt_pressed, m_pressed, config_phase_complete
    
    print("[EMERGENCY LISTENER] Thread started - installing low-level keyboard hook")
    print("[EMERGENCY LISTENER] This hook intercepts keys BEFORE BlockInput affects them!")
    print("[EMERGENCY LISTENER] Press Ctrl+Alt+M to emergency stop")
    print()
    
    try:
        # Install low-level keyboard hook
        keyboard_hook = ctypes.windll.user32.SetWindowsHookExA(
            WH_KEYBOARD_LL,
            keyboard_hook_pointer,
            ctypes.windll.kernel32.GetModuleHandleW(None),
            0
        )
        
        if not keyboard_hook:
            # print("[ERROR] Failed to install keyboard hook!")
            
            # Fallback to old method - check MORE frequently when input is NOT blocked
            VK_CONTROL = 0x11
            VK_MENU = 0x12
            VK_M = 0x4D
            check_counter = 0
            last_status_print = time.time()
            last_input_block_state = False
            fallback_info_printed = False  # Track if we've printed the fallback info
            
            while not emergency_stop:
                # Print fallback info only once after config phase is complete
                if config_phase_complete and not fallback_info_printed:
                    print("[FALLBACK] Using GetAsyncKeyState (won't work when input blocked)")
                    print("[FALLBACK] Will check Ctrl+Alt+M every 50ms when input is NOT blocked")
                    print("[FALLBACK] When input IS blocked, emergency stop won't work - unblock will happen after current action")
                    print()
                    fallback_info_printed = True
                
                check_counter += 1
                current_time = time.time()
                
                # When input is NOT blocked, we can detect keys - check very frequently!
                if not input_currently_blocked:
                    ctrl_state = ctypes.windll.user32.GetAsyncKeyState(VK_CONTROL)
                    alt_state = ctypes.windll.user32.GetAsyncKeyState(VK_MENU)
                    m_state = ctypes.windll.user32.GetAsyncKeyState(VK_M)
                    
                    # Check for Ctrl+Alt+M
                    ctrl_down = (ctrl_state & 0x8000) != 0
                    alt_down = (alt_state & 0x8000) != 0
                    m_down = (m_state & 0x8000) != 0
                    
                    if ctrl_down and alt_down and m_down:
                        print(f"\n[FALLBACK] Ctrl+Alt+M detected while input NOT blocked!")
                        print("\n" + "=" * 50)
                        print("🚨 EMERGENCY STOP ACTIVATED (Ctrl+Alt+M)! 🚨")
                        print("=" * 50)
                        emergency_stop = True
                        print("[EMERGENCY] Program will stop after current action...")
                        break
                
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
            msg = ctypes.wintypes.MSG()
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
            win32api.SetCursorPos((screen_x, screen_y))
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
            win32api.SetCursorPos(original_pos)
            
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
    
    def __init__(self, fishing_time_seconds, eating_interval_seconds, max_eat_count, debug=False):
        self.window_capture = BackgroundWindowCapture(WINDOW_NAME)
        self.point_detector = ImageDetector(DETECTION_IMAGES.get('point', 'assets/images/detection/point.png'), confidence=POINT_CONFIDENCE)
        
        # Hunger detection (optional)
        hunger_image = DETECTION_IMAGES.get('hunger', 'assets/images/detection/hunger.png')
        self.hunger_detector = ImageDetector(hunger_image, confidence=0.15, optional=True) if hunger_image else None
        self.has_hunger_detector = self.hunger_detector and self.hunger_detector.template is not None
        if self.has_hunger_detector:
            print("[INFO] Hunger detection enabled - will auto-eat when hungry (threshold: 0.15)")
            print("[INFO] IMPORTANT: hunger.png should be a screenshot of the hunger BAR when it's LOW (≤35%)")
        
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
            if img_path:
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
        self.max_eat_count = max_eat_count
        self.eat_count = 0
        print(f"[INFO] Eating configured - will eat {max_eat_count} times, every {eating_interval_seconds}s")
        
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
    
    def eat_food(self):
        """Eat food - press 0, click 3 times, press 9, click once"""
        global input_currently_blocked
        
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
                print("[DEBUG] Pressed food slot to select food - now clicking to eat")
            
            # Click 3 times to eat with longer delays to ensure each food is consumed
            for i in range(3):
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
                    print(f"[DEBUG] Eating click {i+1}/3")
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
            
            # Check if we've reached max eat count
            if self.eat_count >= self.max_eat_count:
                print(f"[EATING] Finished eating - reached max eat count ({self.max_eat_count})")
            else:
                print(f"[EATING] Finished eating - next meal in {self.next_eat_interval}s (Meal {self.eat_count}/{self.max_eat_count})")
            
            # Send Discord notification about eating
            if ENABLE_DISCORD_NOTIFICATIONS:
                duration_since_last_meal = time.time() - (self.last_eat_time - (self.last_eat_time - (time.time() - self.next_eat_interval)))
                elapsed_minutes = int(duration_since_last_meal // 60)
                elapsed_seconds = int(duration_since_last_meal % 60)
                
                embed = {
                    "title": "🍖 Food Break!",
                    "description": f"Eating session #{self.eat_count} of {self.max_eat_count} completed",
                    "color": 3447003,  # Blue color
                    "fields": [
                        {
                            "name": "⏱️ Duration Since Last Meal",
                            "value": f"{elapsed_minutes}m {elapsed_seconds}s",
                            "inline": True
                        },
                        {
                            "name": "⏰ Next Meal In",
                            "value": f"{self.next_eat_interval // 60}m {self.next_eat_interval % 60}s" if self.eat_count < self.max_eat_count else "No more meals",
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
                send_discord_notification(DISCORD_WEBHOOK_URL, "", embed)
            
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
        """Check if it's time to eat based on user-configured interval and eat count limit"""
        # Don't eat if we've reached the max count
        if self.eat_count >= self.max_eat_count:
            return False
        
        elapsed = time.time() - self.last_eat_time
        if elapsed >= self.next_eat_interval:
            return True
        return False
    
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
                            
                            # SAVE SCREENSHOT when detection succeeds (if enabled)
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
                            
                            print(f"[DETECTION THREAD] ✓ Found {img_name}! Confidence: {max_val:.2f}")
                            print(f"[DETECTION THREAD] Detection took {elapsed:.2f}s with {check_counter} checks")
                            print(f"[DETECTION THREAD] Last check: capture={capture_time*1000:.0f}ms, detection={detection_time*1000:.0f}ms")
                            
                            # Send Discord notification about the catch
                            if ENABLE_DISCORD_NOTIFICATIONS:
                                # Determine catch type emoji
                                catch_emoji = "🐟"
                                if "treasure" in detector_name.lower():
                                    catch_emoji = "💎"
                                elif "sunken" in detector_name.lower():
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
                                
                                embed = {
                                    "title": f"{catch_emoji} Catch Detected!",
                                    "description": f"**{detector_name.title()}** caught!",
                                    "color": 5763719,  # Green color
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
                                
                                # Send notification with screenshot
                                if screenshot_saved and screenshot_path:
                                    send_discord_notification(DISCORD_WEBHOOK_URL, "", embed, image_path=screenshot_path)
                                    
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
                                    send_discord_notification(DISCORD_WEBHOOK_URL, "", embed)
                            
                            self.caught_flag.set()  # Signal main thread
                            self.detection_queue.put({
                                'type': 'caught',
                                'image': img_name,
                                'location': {'x': max_loc[0], 'y': max_loc[1], 'confidence': max_val},
                                'checks': check_counter,
                                'elapsed': elapsed
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
                        print(f"[DETECTION CHECK #{check_counter}] Confidences: {conf_str} (threshold: 0.50)")
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
        global emergency_stop, input_currently_blocked
        
        print(f"Starting fishing macro for {self.fishing_time} seconds...")
        print("The Roblox window can be in the background!")
        print("-" * 50)
        
        while time.time() < self.end_time and not emergency_stop:
            # Check emergency stop at the very start of each iteration
            if emergency_stop:
                print("[STOP] Emergency stop detected at start of loop, exiting...")
                break
            
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
                self.eat_food()
                # Wait a bit after eating before continuing
                time.sleep(2)
                continue
            
            # Process fishing point if detected
            if point_location:
                self.detection_count += 1
                self.last_detection_time = time.time()
                
                # SAVE SCREENSHOT when point is detected!
                # timestamp = time.strftime("%Y%m%d_%H%M%S")
                # screenshot_path = f"assets/screenshots/point_{timestamp}_conf{point_location['confidence']:.2f}.png"
                # try:
                #     import os
                #     os.makedirs("assets/screenshots", exist_ok=True)
                #     cv2.imwrite(screenshot_path, screenshot)
                #     if self.debug:
                #         print(f"[POINT DETECTION] 📸 Screenshot saved: {screenshot_path}")
                # except Exception as e:
                #     if self.debug:
                #         print(f"[POINT DETECTION] Failed to save screenshot: {e}")
                
                print(f"[DETECTED] Point found at ({point_location['x']}, {point_location['y']}) "
                      f"- Confidence: {point_location['confidence']:.2f}")
                
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
                        # Check emergency stop before each click - CRITICAL for responsiveness
                        if emergency_stop:
                            print("[STOP] Emergency stop detected during clicking!")
                            print("[STOP] Breaking out of click loop immediately...")
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
                        
                        # Check emergency stop after click
                        if emergency_stop:
                            print("[STOP] Emergency stop detected after click!")
                            break
                        
                        click_duration = time.time() - auto_clicker_start_time
                        input_block_duration = time.time() - input_block_start_time
                        
                        # Stop after configured max clicking duration
                        if click_duration > MAX_CLICKING_DURATION:
                            print(f"[{MAX_CLICKING_DURATION}s TIMEOUT] Stopped clicking after {MAX_CLICKING_DURATION} seconds ({clicks_in_loop} clicks)")
                            print(f"[{MAX_CLICKING_DURATION}s TIMEOUT] Background detection performed {self.detection_check_count} checks")
                            self.fish_just_caught = True  # Assume fish was caught
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
                            win32api.SetCursorPos(original_mouse_pos)
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
                            win32api.SetCursorPos(original_mouse_pos)
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
                    win32api.SetCursorPos(original_mouse_pos)
                    if self.debug:
                        print(f"[DEBUG] Restored original mouse position: {original_mouse_pos}")
                    else:
                        print(f"[INFO] Mouse position restored to original location")
                
            else:
                # No detection - check if we need to cast rod
                time_since_last_detection = time.time() - self.last_detection_time
                
                if time_since_last_detection > self.no_detection_timeout:
                    print(f"[AUTO-CAST] No detection for {self.no_detection_timeout}s. Casting rod...")
                    
                    # Click center of screen to cast
                    _, _, w, h = self.window_capture.get_window_rect()
                    center_x = w // 2
                    center_y = h // 2
                    
                    if self.debug:
                        print(f"[DEBUG] Auto-cast at center ({center_x}, {center_y})")
                    
                    self.window_capture.send_click(center_x, center_y, debug=self.debug)
                    self.click_count += 1
                    self.last_detection_time = time.time()
            
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
        print("-" * 50)
        listener_thread = start_emergency_listener()
        
        print()
        
        # Get fishing duration from user
        fishing_time = int(input("Enter in seconds how long should scan last: "))
        
        # Get eating configuration from user (with defaults from config)
        print()
        print(f"Eating configuration (defaults from config.py):")
        eating_interval_input = input(f"Enter eating interval in seconds (default={DEFAULT_EATING_INTERVAL}): ").strip()
        eating_interval = int(eating_interval_input) if eating_interval_input else DEFAULT_EATING_INTERVAL
        
        eating_count_input = input(f"How many times to eat (default={DEFAULT_EATING_COUNT}): ").strip()
        eating_count = int(eating_count_input) if eating_count_input else DEFAULT_EATING_COUNT
        
        # Ask if user wants debug mode
        debug_input = input("Enable debug mode? (y/n, default=y): ").strip().lower()
        debug_mode = debug_input != 'n'  # Default to yes
        
        # Configuration phase is complete - allow debug messages now
        config_phase_complete = True
        
        print()
        if debug_mode:
            print("[DEBUG MODE ENABLED] - Detailed click information will be shown")
            print()
        
        if ENABLE_DISCORD_NOTIFICATIONS:
            print("🔔 [DISCORD NOTIFICATIONS ENABLED]")
            print(f"    Webhook: {DISCORD_WEBHOOK_URL[:50]}...")
            print()
        
        print("⚠️  IMPORTANT NOTES:")
        print("    1. Roblox window will be brought to foreground when clicking")
        print("    2. Your keyboard/mouse will be BLOCKED during fishing sequences")
        print("    3. This prevents your input from interfering with the macro")
        print("    4. Input will be unblocked after each fish is caught/escaped")
        print("    5. ⚠️ Run as Administrator for best results!")
        print("       - Required for input blocking to work")
        print("       - Required for keyboard hook (emergency stop during blocking)")
        print("    6. 🚨 Press Ctrl+Alt+M to emergency stop!")
        print("       - Works immediately when input is NOT blocked")
        print("       - If hook installed: works even during blocking")
        print("       - If hook failed: stops after current fishing action completes")
        print()
        
        # Create and run macro
        macro = FishingMacro(fishing_time, eating_interval, eating_count, debug=debug_mode)
        
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
                        "value": f"{eating_count}x every {eating_interval}s",
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
            send_discord_notification(DISCORD_WEBHOOK_URL, "🚀 Bot Starting...", embed)
        
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
            send_discord_notification(DISCORD_WEBHOOK_URL, "✅ Session Finished!", embed)
        
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