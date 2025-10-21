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

# Emergency stop flag
emergency_stop = False
input_currently_blocked = False
keyboard_hook = None
esc_pressed = False
end_pressed = False

# Keyboard hook constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104

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
    global emergency_stop, input_currently_blocked, esc_pressed, end_pressed
    
    if nCode >= 0:
        if wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN:
            kb_struct = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk_code = kb_struct.vkCode
            
            VK_ESCAPE = 0x1B
            VK_END = 0x23
            
            # Check for ESC or END key
            if vk_code == VK_ESCAPE:
                esc_pressed = True
                print(f"\n[HOOK DEBUG] ESC key detected via keyboard hook!")
            elif vk_code == VK_END:
                end_pressed = True
                print(f"\n[HOOK DEBUG] END key detected via keyboard hook!")
            
            if esc_pressed or end_pressed:
                print(f"[HOOK DEBUG] Emergency key pressed! esc={esc_pressed}, end={end_pressed}")
                print(f"[HOOK DEBUG] input_currently_blocked = {input_currently_blocked}")
                
                if not emergency_stop:
                    print("\n" + "=" * 50)
                    print("🚨 EMERGENCY STOP ACTIVATED! 🚨")
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
    
    # Call next hook in chain
    return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)

# Create callback function pointer
HOOKPROC = ctypes.CFUNCTYPE(c_long, ctypes.c_int, ctypes.c_int, ctypes.POINTER(c_long))
keyboard_hook_pointer = HOOKPROC(keyboard_hook_callback)

def emergency_stop_listener():
    """Listen for ESC/END keys using low-level keyboard hook (bypasses BlockInput!)"""
    global emergency_stop, keyboard_hook, esc_pressed, end_pressed
    
    print("[EMERGENCY LISTENER] Thread started - installing low-level keyboard hook")
    print("[EMERGENCY LISTENER] This hook intercepts keys BEFORE BlockInput affects them!")
    print("[EMERGENCY LISTENER] Press ESC or END to emergency stop")
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
            print("[ERROR] Failed to install keyboard hook!")
            print("[FALLBACK] Using GetAsyncKeyState (won't work when input blocked)")
            
            # Fallback to old method - check MORE frequently when input is NOT blocked
            VK_ESCAPE = 0x1B
            VK_END = 0x23
            check_counter = 0
            last_status_print = time.time()
            last_input_block_state = False
            
            print("[FALLBACK] Will check keys every 50ms when input is NOT blocked")
            print("[FALLBACK] When input IS blocked, emergency stop won't work - unblock will happen after current action")
            print()
            
            while not emergency_stop:
                check_counter += 1
                current_time = time.time()
                
                # When input is NOT blocked, we can detect keys - check very frequently!
                if not input_currently_blocked:
                    esc_state = ctypes.windll.user32.GetAsyncKeyState(VK_ESCAPE)
                    end_state = ctypes.windll.user32.GetAsyncKeyState(VK_END)
                    
                    if esc_state & 0x8000 or end_state & 0x8000:
                        print(f"\n[FALLBACK] Emergency key detected while input NOT blocked!")
                        print(f"[FALLBACK] ESC: {(esc_state & 0x8000) != 0}, END: {(end_state & 0x8000) != 0}")
                        
                        print("\n" + "=" * 50)
                        print("🚨 EMERGENCY STOP ACTIVATED! 🚨")
                        print("=" * 50)
                        emergency_stop = True
                        print("[EMERGENCY] Program will stop after current action...")
                        break
                
                # Track when input blocking state changes
                if input_currently_blocked != last_input_block_state:
                    if input_currently_blocked:
                        print("[FALLBACK] Input is now BLOCKED - emergency keys won't be detected until unblocked")
                    else:
                        print("[FALLBACK] Input is now UNBLOCKED - emergency keys will be detected")
                    last_input_block_state = input_currently_blocked
                
                if current_time - last_status_print >= 10.0:
                    print(f"[EMERGENCY DEBUG] Fallback mode - checked {check_counter} times | input_blocked={input_currently_blocked}")
                    last_status_print = current_time
                    check_counter = 0
                
                # Check more frequently when input is not blocked (50ms), less when blocked (200ms)
                time.sleep(0.05 if not input_currently_blocked else 0.2)
        else:
            print(f"[EMERGENCY LISTENER] Keyboard hook installed successfully (handle: {keyboard_hook})")
            print("[EMERGENCY LISTENER] Monitoring for ESC/END keys...")
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
                
                # Print periodic status
                if current_time - last_status_print >= 10.0:
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
    
    def __init__(self, fishing_time_seconds, debug=False):
        self.window_capture = BackgroundWindowCapture("Roblox")
        self.point_detector = ImageDetector('point.png', confidence=0.55)
        
        # Hunger detection
        self.hunger_detector = ImageDetector('hunger.png', confidence=0.15, optional=True)  # Very low threshold for flexibility
        self.has_hunger_detector = self.hunger_detector.template is not None
        if self.has_hunger_detector:
            print("[INFO] Hunger detection enabled - will auto-eat when hungry (threshold: 0.15)")
            print("[INFO] IMPORTANT: hunger.png should be a screenshot of the hunger BAR when it's LOW (≤35%)")
            print("[INFO]           The macro will detect when the bar looks similar to your hunger.png image")
        else:
            print("[WARNING] hunger.png not found - auto-eating disabled")
            print("[WARNING] To enable: Take a screenshot of your hunger bar when it's at 35% or lower")
            print("[WARNING]           Save it as 'hunger.png' in the same folder as this script")
        
        # Try multiple caught detection images
        self.caught_detectors = []
        caught_images = [
            ('caught.png', 0.35),  # Balanced confidence to avoid false positives
            ('fish_caught.png', 0.35),  # Alternative image
            ('treasure_caught.png', 0.35),  # Alternative image
        ]
        
        for img_path, conf in caught_images:
            detector = ImageDetector(img_path, confidence=conf, optional=True)
            if detector.template is not None:
                self.caught_detectors.append((img_path, detector))
                print(f"[INFO] Loaded catch detector: {img_path} (confidence: {conf})")
        
        self.has_caught_detector = len(self.caught_detectors) > 0
        if not self.has_caught_detector:
            print("[WARNING] No 'caught' detection images found. Will rely on timeout only.")
        
        self.fishing_time = fishing_time_seconds
        self.end_time = time.time() + fishing_time_seconds
        self.no_detection_timeout = 70
        self.last_detection_time = time.time()
        
        self.click_count = 0
        self.detection_count = 0
        self.debug = debug
        self.last_hunger_check = 0
        self.hunger_check_interval = 10  # Check hunger every 10 seconds
        self.fish_just_caught = False  # Track if we just caught a fish
        
        # Random eating schedule
        self.last_eat_time = time.time()
        self.next_eat_interval = random.randint(60, 120)  # Random interval between 60-120 seconds
        self.eat_count = 0
        print(f"[INFO] Random eating enabled - will eat every {self.next_eat_interval}s (randomly 60-120s)")
    
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
            # Press 0 to select food
            if self.debug:
                print("[DEBUG] About to press key '0' (0x30)")
            prev_win = self.window_capture.send_key(0x30, debug=self.debug)  # 0 key
            time.sleep(0.5)  # Longer delay to ensure game processes the key
            
            if self.debug:
                print("[DEBUG] Pressed 0 to select food - now clicking to eat")
            
            # Click 3 times to eat with longer delays to ensure each food is consumed
            for i in range(3):
                # Safety check: unblock if eating takes too long
                eat_duration = time.time() - eat_input_block_start_time
                if eat_duration > 90:
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
            
            time.sleep(1.0)  # Longer wait to ensure last food is fully consumed before switching
            
            # Press 9 to select fishing rod
            if self.debug:
                print("[DEBUG] About to press key '9' (0x39)")
            self.window_capture.send_key(0x39, debug=self.debug)  # 9 key
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
            
            # Schedule next eating time
            self.last_eat_time = time.time()
            self.next_eat_interval = random.randint(60, 120)
            print(f"[EATING] Finished eating - next meal in {self.next_eat_interval}s")
            
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
        """Check if it's time to eat based on random interval"""
        elapsed = time.time() - self.last_eat_time
        if elapsed >= self.next_eat_interval:
            return True
        return False
        
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
                    # Start auto-clicking until point disappears or timeout
                    auto_clicker_start_time = time.time()
                    click_duration = 0
                    clicks_in_loop = 0
                    previous_window = None  # Track previous window to restore later
                    
                    while True:
                        # Check emergency stop before each click - CRITICAL for responsiveness
                        if emergency_stop:
                            print("[STOP] Emergency stop detected during clicking!")
                            print("[STOP] Breaking out of click loop immediately...")
                            break
                        
                        # Click at the CENTER of screen (not at point location)
                        debug_this_click = self.debug and clicks_in_loop == 0
                        if clicks_in_loop == 0:
                            # First click - capture previous window
                            previous_window = self.window_capture.send_click(center_x, center_y, debug=debug_this_click)
                        else:
                            self.window_capture.send_click(center_x, center_y, debug=debug_this_click)
                        
                        self.click_count += 1
                        clicks_in_loop += 1
                        
                        # Check emergency stop more frequently during initial burst
                        if emergency_stop:
                            print("[STOP] Emergency stop detected after click!")
                            break
                        
                        # Minimum guarantee: Don't check for first 150 clicks to ensure we get enough clicks in
                        # This handles rare/golden/massive fish that need more clicks
                        if clicks_in_loop < 150:
                            time.sleep(0.012)  # Very fast for initial burst - 12ms = ~83 clicks/sec
                            continue
                        
                        # After 150 clicks, only check every 30 clicks to avoid premature detection
                        if clicks_in_loop % 30 != 0:
                            time.sleep(0.015)  # Fast speed continues - 15ms = ~66 clicks/sec
                            continue
                        
                        # Check if point is still visible (fish still biting)
                        current_screenshot = self.window_capture.capture_window()
                        
                        if current_screenshot is not None:
                            # Check if point.png is still there
                            point_still_there = self.point_detector.find_in_image(current_screenshot)
                            
                            if not point_still_there:
                                # Point disappeared - fish caught or line broke
                                print(f"[INFO] Point indicator disappeared after {clicks_in_loop} clicks (fish caught or escaped)")
                                self.fish_just_caught = True  # Mark that we just caught a fish
                                # Restore previous window
                                if previous_window:
                                    time.sleep(0.2)
                                    self.window_capture.restore_window(previous_window)
                                    if self.debug:
                                        print(f"[DEBUG] Restored previous window")
                                break
                            
                            # Optional: Also check for caught visual (but point disappearing is primary indicator)
                            if clicks_in_loop >= 5 and self.has_caught_detector:
                                debug_detection = self.debug and clicks_in_loop == 5
                                
                                # Try all caught detectors (secondary check)
                                for img_name, detector in self.caught_detectors:
                                    caught_location = detector.find_in_image(current_screenshot, debug=debug_detection)
                                    
                                    if caught_location:
                                        if self.debug:
                                            print(f"[DEBUG] Also detected {img_name} visual")
                                        break
                        
                        click_duration = time.time() - auto_clicker_start_time
                        input_block_duration = time.time() - input_block_start_time
                        
                        # Show progress every 1 second
                        if self.debug and clicks_in_loop % 70 == 0:  # Every ~1 second at 70 cps
                            print(f"[DEBUG] Still clicking... {clicks_in_loop} clicks, {click_duration:.1f}s elapsed, input_blocked={input_blocked}")
                            # Re-block input periodically to ensure it stays blocked (only if under 90s)
                            if input_blocked and input_block_duration < 90:
                                block_input()
                        
                        # CRITICAL SAFETY: Auto-unblock input after 90 seconds regardless of state
                        if input_block_duration > 90:
                            print(f"\n[CRITICAL SAFETY] Input has been blocked for 90+ seconds!")
                            print(f"[CRITICAL SAFETY] Auto-unblocking to prevent permanent lockout!")
                            input_currently_blocked = False
                            unblock_input()
                            print(f"[CRITICAL SAFETY] Input force-unblocked after {input_block_duration:.1f}s")
                            # Restore mouse and window
                            win32api.SetCursorPos(original_mouse_pos)
                            if previous_window:
                                self.window_capture.restore_window(previous_window)
                            break
                        
                        # Safety timeout: Automatically unblock input after 84 seconds to prevent stuck state
                        if click_duration > 84:
                            print(f"[SAFETY TIMEOUT] Stopped clicking after 84 seconds ({clicks_in_loop} clicks)")
                            print(f"[SAFETY] Auto-unblocking input to prevent stuck state!")
                            # Restore previous window after timeout too
                            if previous_window:
                                time.sleep(0.2)
                                self.window_capture.restore_window(previous_window)
                                if self.debug:
                                    print(f"[DEBUG] Restored previous window after timeout")
                            break
                        
                        # Normal timeout after 40 seconds for regular fish (increased to handle rare fish)
                        if click_duration > 40:
                            print(f"[TIMEOUT] Stopped clicking after 40 seconds ({clicks_in_loop} clicks)")
                            # Restore previous window after timeout too
                            if previous_window:
                                time.sleep(0.2)
                                self.window_capture.restore_window(previous_window)
                                if self.debug:
                                    print(f"[DEBUG] Restored previous window after timeout")
                            break
                        
                        time.sleep(0.015)  # Fast clicking - 15ms delay = ~66 clicks/second
                
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
            
            time.sleep(0.25)
        
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
    global emergency_stop, input_currently_blocked
    
    try:
        print("=" * 50)
        print("Roblox Arcane Odyssey - Background Fishing Macro")
        print("=" * 50)
        print()
        
        # Start emergency stop listener
        print("🚨 EMERGENCY STOP: Press ESC or END key at any time to stop and unblock input!")
        print("-" * 50)
        listener_thread = start_emergency_listener()
        print()
        
        # Get fishing duration from user
        fishing_time = int(input("Enter in seconds how long should scan last: "))
        
        # Ask if user wants debug mode
        debug_input = input("Enable debug mode? (y/n, default=y): ").strip().lower()
        debug_mode = debug_input != 'n'  # Default to yes
        
        print()
        if debug_mode:
            print("[DEBUG MODE ENABLED] - Detailed click information will be shown")
            print()
        
        print("⚠️  IMPORTANT NOTES:")
        print("    1. Roblox window will be brought to foreground when clicking")
        print("    2. Your keyboard/mouse will be BLOCKED during fishing sequences")
        print("    3. This prevents your input from interfering with the macro")
        print("    4. Input will be unblocked after each fish is caught/escaped")
        print("    5. ⚠️ Run as Administrator for best results!")
        print("       - Required for input blocking to work")
        print("       - Required for keyboard hook (emergency stop during blocking)")
        print("    6. 🚨 Press ESC or END key to emergency stop!")
        print("       - Works immediately when input is NOT blocked")
        print("       - If hook installed: works even during blocking")
        print("       - If hook failed: stops after current fishing action completes")
        print()
        
        # Create and run macro
        macro = FishingMacro(fishing_time, debug=debug_mode)
        macro.run()
        
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
