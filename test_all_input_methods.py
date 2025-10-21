"""
Test ALL possible Windows API methods for sending input to background windows
This comprehensive test will try every known technique for background input
"""

import time
import ctypes
from ctypes import windll, wintypes, c_ulong, Structure, sizeof, byref, POINTER
import win32gui
import win32con
import win32api
import win32ui

# Virtual key codes
VK_0 = 0x30
VK_9 = 0x39

# Mouse button constants
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_MOVE = 0x0001

# Input types
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

# Keyboard flags
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

class MOUSEINPUT(Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", POINTER(c_ulong))
    ]

class KEYBDINPUT(Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", POINTER(c_ulong))
    ]

class HARDWAREINPUT(Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUT_UNION)
    ]

def find_roblox_window():
    """Find the Roblox window handle"""
    hwnd = win32gui.FindWindow(None, "Roblox")
    if not hwnd:
        print("[ERROR] Could not find Roblox window!")
        print("Make sure Roblox is running and the window title is 'Roblox'")
        return None
    
    print(f"[SUCCESS] Found Roblox window - Handle: {hwnd}")
    return hwnd

def get_window_center(hwnd):
    """Get the center coordinates of the window"""
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    center_x = x + w // 2
    center_y = y + h // 2
    return center_x, center_y, w, h

# ============================================================================
# METHOD 1: SendMessage with WM_KEYDOWN/WM_KEYUP (Pure message queue)
# ============================================================================
def method1_sendmessage_key(hwnd, vk_code):
    """Method 1: SendMessage - Direct window messages (NO FOCUS REQUIRED)"""
    print("\n[METHOD 1] Testing SendMessage WM_KEYDOWN/WM_KEYUP...")
    try:
        # Send WM_KEYDOWN
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
        time.sleep(0.05)
        # Send WM_KEYUP
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
        print("  ✓ SendMessage key press sent")
        return True
    except Exception as e:
        print(f"  ✗ SendMessage failed: {e}")
        return False

# ============================================================================
# METHOD 2: PostMessage with WM_KEYDOWN/WM_KEYUP (Async message queue)
# ============================================================================
def method2_postmessage_key(hwnd, vk_code):
    """Method 2: PostMessage - Async messages (NO FOCUS REQUIRED)"""
    print("\n[METHOD 2] Testing PostMessage WM_KEYDOWN/WM_KEYUP...")
    try:
        # Post WM_KEYDOWN
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
        time.sleep(0.05)
        # Post WM_KEYUP
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
        print("  ✓ PostMessage key press sent")
        return True
    except Exception as e:
        print(f"  ✗ PostMessage failed: {e}")
        return False

# ============================================================================
# METHOD 3: SendMessage with WM_CHAR (Character message)
# ============================================================================
def method3_sendmessage_char(hwnd, char):
    """Method 3: SendMessage WM_CHAR - Character input (NO FOCUS REQUIRED)"""
    print("\n[METHOD 3] Testing SendMessage WM_CHAR...")
    try:
        win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(char), 0)
        print(f"  ✓ SendMessage WM_CHAR '{char}' sent")
        return True
    except Exception as e:
        print(f"  ✗ SendMessage WM_CHAR failed: {e}")
        return False

# ============================================================================
# METHOD 4: SendInput with keyboard (Global input with focus)
# ============================================================================
def method4_sendinput_key(vk_code, needs_focus=True):
    """Method 4: SendInput keyboard - Hardware simulation (NEEDS FOCUS)"""
    print(f"\n[METHOD 4] Testing SendInput keyboard (needs_focus={needs_focus})...")
    try:
        extra = c_ulong(0)
        ii = INPUT()
        ii.type = INPUT_KEYBOARD
        
        # Key down
        ii.union.ki = KEYBDINPUT(vk_code, 0, 0, 0, ctypes.pointer(extra))
        ctypes.windll.user32.SendInput(1, byref(ii), sizeof(ii))
        time.sleep(0.05)
        
        # Key up
        ii.union.ki = KEYBDINPUT(vk_code, 0, KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
        ctypes.windll.user32.SendInput(1, byref(ii), sizeof(ii))
        print("  ✓ SendInput key press sent")
        return True
    except Exception as e:
        print(f"  ✗ SendInput failed: {e}")
        return False

# ============================================================================
# METHOD 5: keybd_event (Legacy hardware simulation)
# ============================================================================
def method5_keybd_event(vk_code, needs_focus=True):
    """Method 5: keybd_event - Legacy hardware simulation (NEEDS FOCUS)"""
    print(f"\n[METHOD 5] Testing keybd_event (needs_focus={needs_focus})...")
    try:
        # Get scan code
        scan_code = win32api.MapVirtualKey(vk_code, 0)
        
        # Key down
        windll.user32.keybd_event(vk_code, scan_code, 0, 0)
        time.sleep(0.05)
        
        # Key up
        windll.user32.keybd_event(vk_code, scan_code, KEYEVENTF_KEYUP, 0)
        print("  ✓ keybd_event key press sent")
        return True
    except Exception as e:
        print(f"  ✗ keybd_event failed: {e}")
        return False

# ============================================================================
# METHOD 6: SendMessage with WM_LBUTTONDOWN/WM_LBUTTONUP (Click messages)
# ============================================================================
def method6_sendmessage_click(hwnd):
    """Method 6: SendMessage mouse click - Direct messages (NO FOCUS REQUIRED)"""
    print("\n[METHOD 6] Testing SendMessage WM_LBUTTONDOWN/WM_LBUTTONUP...")
    try:
        # Get window dimensions
        rect = win32gui.GetWindowRect(hwnd)
        client_rect = win32gui.GetClientRect(hwnd)
        w = client_rect[2]
        h = client_rect[3]
        
        # Click at center
        x = w // 2
        y = h // 2
        lParam = win32api.MAKELONG(x, y)
        
        # Send mouse down
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.05)
        # Send mouse up
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        print(f"  ✓ SendMessage click at ({x}, {y}) sent")
        return True
    except Exception as e:
        print(f"  ✗ SendMessage click failed: {e}")
        return False

# ============================================================================
# METHOD 7: PostMessage with WM_LBUTTONDOWN/WM_LBUTTONUP (Async click)
# ============================================================================
def method7_postmessage_click(hwnd):
    """Method 7: PostMessage mouse click - Async messages (NO FOCUS REQUIRED)"""
    print("\n[METHOD 7] Testing PostMessage WM_LBUTTONDOWN/WM_LBUTTONUP...")
    try:
        # Get window dimensions
        client_rect = win32gui.GetClientRect(hwnd)
        w = client_rect[2]
        h = client_rect[3]
        
        # Click at center
        x = w // 2
        y = h // 2
        lParam = win32api.MAKELONG(x, y)
        
        # Post mouse down
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.05)
        # Post mouse up
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        print(f"  ✓ PostMessage click at ({x}, {y}) sent")
        return True
    except Exception as e:
        print(f"  ✗ PostMessage click failed: {e}")
        return False

# ============================================================================
# METHOD 8: SendInput with mouse (Global mouse input)
# ============================================================================
def method8_sendinput_click(screen_x, screen_y, needs_focus=True):
    """Method 8: SendInput mouse - Hardware simulation (NEEDS FOCUS)"""
    print(f"\n[METHOD 8] Testing SendInput mouse click (needs_focus={needs_focus})...")
    try:
        # Save cursor position
        original_pos = win32api.GetCursorPos()
        
        # Move cursor
        win32api.SetCursorPos((screen_x, screen_y))
        time.sleep(0.02)
        
        extra = c_ulong(0)
        ii = INPUT()
        ii.type = INPUT_MOUSE
        
        # Mouse down
        ii.union.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra))
        ctypes.windll.user32.SendInput(1, byref(ii), sizeof(ii))
        time.sleep(0.05)
        
        # Mouse up
        ii.union.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra))
        ctypes.windll.user32.SendInput(1, byref(ii), sizeof(ii))
        
        # Restore cursor
        win32api.SetCursorPos(original_pos)
        print(f"  ✓ SendInput click at ({screen_x}, {screen_y}) sent")
        return True
    except Exception as e:
        print(f"  ✗ SendInput click failed: {e}")
        return False

# ============================================================================
# METHOD 9: SetCursorPos + mouse_event (Legacy mouse simulation)
# ============================================================================
def method9_mouse_event(screen_x, screen_y, needs_focus=True):
    """Method 9: mouse_event - Legacy hardware simulation (NEEDS FOCUS)"""
    print(f"\n[METHOD 9] Testing mouse_event (needs_focus={needs_focus})...")
    try:
        # Save cursor position
        original_pos = win32api.GetCursorPos()
        
        # Move cursor
        win32api.SetCursorPos((screen_x, screen_y))
        time.sleep(0.02)
        
        # Click using mouse_event
        windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.05)
        windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        
        # Restore cursor
        win32api.SetCursorPos(original_pos)
        print(f"  ✓ mouse_event click at ({screen_x}, {screen_y}) sent")
        return True
    except Exception as e:
        print(f"  ✗ mouse_event failed: {e}")
        return False

# ============================================================================
# METHOD 10: DirectInput simulation (Hardware-level)
# ============================================================================
def method10_directinput_key(vk_code, needs_focus=True):
    """Method 10: DirectInput-style - Scan code hardware simulation (NEEDS FOCUS)"""
    print(f"\n[METHOD 10] Testing DirectInput-style keyboard (needs_focus={needs_focus})...")
    try:
        # Get scan code
        scan_code = win32api.MapVirtualKey(vk_code, 0)
        
        extra = c_ulong(0)
        ii = INPUT()
        ii.type = INPUT_KEYBOARD
        
        # Key down with scan code
        ii.union.ki = KEYBDINPUT(0, scan_code, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
        ctypes.windll.user32.SendInput(1, byref(ii), sizeof(ii))
        time.sleep(0.05)
        
        # Key up with scan code
        ii.union.ki = KEYBDINPUT(0, scan_code, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
        ctypes.windll.user32.SendInput(1, byref(ii), sizeof(ii))
        print("  ✓ DirectInput-style key press sent")
        return True
    except Exception as e:
        print(f"  ✗ DirectInput-style failed: {e}")
        return False

# ============================================================================
# METHOD 11: Combined scan code with keybd_event (Current working method)
# ============================================================================
def method11_keybd_event_scancode(vk_code, needs_focus=True):
    """Method 11: keybd_event with scan codes - What currently works (NEEDS FOCUS)"""
    print(f"\n[METHOD 11] Testing keybd_event with scan codes (needs_focus={needs_focus})...")
    try:
        scan_code = win32api.MapVirtualKey(vk_code, 0)
        
        # Key down
        windll.user32.keybd_event(vk_code, scan_code, 0, 0)
        time.sleep(0.05)
        # Key up
        windll.user32.keybd_event(vk_code, scan_code, KEYEVENTF_KEYUP, 0)
        print("  ✓ keybd_event with scan code sent")
        return True
    except Exception as e:
        print(f"  ✗ keybd_event with scan code failed: {e}")
        return False

def bring_window_to_front(hwnd):
    """Bring window to foreground"""
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)
        return True
    except Exception as e:
        print(f"[ERROR] Could not bring window to front: {e}")
        return False

def main():
    print("=" * 70)
    print("COMPREHENSIVE WINDOWS INPUT METHOD TEST")
    print("=" * 70)
    print()
    print("This script will test ALL known methods for sending input to windows.")
    print("Some methods work WITHOUT FOCUS, others REQUIRE FOCUS.")
    print()
    
    # Find Roblox window
    hwnd = find_roblox_window()
    if not hwnd:
        return
    
    center_x, center_y, w, h = get_window_center(hwnd)
    print(f"Window dimensions: {w}x{h}")
    print(f"Window center (screen coords): ({center_x}, {center_y})")
    print()
    
    print("=" * 70)
    print("PART 1: KEYBOARD INPUT METHODS (WITHOUT FOCUS)")
    print("=" * 70)
    print("Testing methods that should work WITHOUT bringing window to front...")
    print("Press Enter to start testing...")
    input()
    
    # Test keyboard methods that don't need focus
    method1_sendmessage_key(hwnd, VK_0)
    time.sleep(1)
    
    method2_postmessage_key(hwnd, VK_0)
    time.sleep(1)
    
    method3_sendmessage_char(hwnd, '0')
    time.sleep(1)
    
    print("\n" + "=" * 70)
    print("PART 2: MOUSE CLICK METHODS (WITHOUT FOCUS)")
    print("=" * 70)
    print("Testing click methods that should work WITHOUT bringing window to front...")
    print("Press Enter to continue...")
    input()
    
    method6_sendmessage_click(hwnd)
    time.sleep(1)
    
    method7_postmessage_click(hwnd)
    time.sleep(1)
    
    print("\n" + "=" * 70)
    print("PART 3: KEYBOARD INPUT METHODS (WITH FOCUS)")
    print("=" * 70)
    print("Testing methods that REQUIRE window focus...")
    print("The Roblox window will be brought to front.")
    print("Press Enter to continue...")
    input()
    
    # Bring window to front
    bring_window_to_front(hwnd)
    
    method4_sendinput_key(VK_0, needs_focus=True)
    time.sleep(1)
    
    method5_keybd_event(VK_0, needs_focus=True)
    time.sleep(1)
    
    method10_directinput_key(VK_0, needs_focus=True)
    time.sleep(1)
    
    method11_keybd_event_scancode(VK_0, needs_focus=True)
    time.sleep(1)
    
    print("\n" + "=" * 70)
    print("PART 4: MOUSE CLICK METHODS (WITH FOCUS)")
    print("=" * 70)
    print("Testing click methods with window focus...")
    print("Press Enter to continue...")
    input()
    
    method8_sendinput_click(center_x, center_y, needs_focus=True)
    time.sleep(1)
    
    method9_mouse_event(center_x, center_y, needs_focus=True)
    time.sleep(1)
    
    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)
    print()
    print("SUMMARY:")
    print("--------")
    print("Methods that should work WITHOUT FOCUS (background):")
    print("  1. SendMessage WM_KEYDOWN/WM_KEYUP")
    print("  2. PostMessage WM_KEYDOWN/WM_KEYUP")
    print("  3. SendMessage WM_CHAR")
    print("  6. SendMessage WM_LBUTTONDOWN/WM_LBUTTONUP")
    print("  7. PostMessage WM_LBUTTONDOWN/WM_LBUTTONUP")
    print()
    print("Methods that REQUIRE FOCUS (foreground):")
    print("  4. SendInput keyboard")
    print("  5. keybd_event")
    print("  8. SendInput mouse")
    print("  9. mouse_event")
    print(" 10. DirectInput-style (scan codes)")
    print(" 11. keybd_event with scan codes (CURRENTLY USED)")
    print()
    print("ROBLOX ANTI-CHEAT NOTE:")
    print("Roblox may block message-based methods (1-3, 6-7) to prevent bots.")
    print("Hardware simulation methods (4-5, 8-11) may work better but need focus.")
    print()
    print("Check in Roblox if any of the '0' keypresses or clicks worked!")

if __name__ == "__main__":
    main()
