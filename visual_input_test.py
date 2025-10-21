"""
Visual validation test - Makes it OBVIOUS if input is working
This will repeatedly send '0' and '9' keys so you can see if they register
"""

import win32gui
import win32api
import win32con
import time

def find_roblox():
    hwnd = win32gui.FindWindow(None, "Roblox")
    if not hwnd:
        print("[ERROR] Roblox window not found!")
        return None
    print(f"[SUCCESS] Found Roblox - Handle: {hwnd}")
    return hwnd

def test_background_input(hwnd):
    """Test if background input (SendMessage/PostMessage) works"""
    print("\n" + "=" * 70)
    print("TEST 1: BACKGROUND INPUT (SendMessage)")
    print("=" * 70)
    print()
    print("This will send '0' and '9' keys WITHOUT focusing Roblox.")
    print("Watch your Roblox inventory/hotbar for changes!")
    print()
    print("Instructions:")
    print("  1. Look at your Roblox character")
    print("  2. Watch inventory slots 0 and 9")
    print("  3. I'll send keys every second for 10 seconds")
    print("  4. Tell me if you see ANY changes")
    print()
    input("Press Enter when ready...")
    print()
    
    for i in range(10):
        # Try SendMessage
        print(f"[{i+1}/10] Sending '0' via SendMessage (background)...")
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, 0x30, 0)
        time.sleep(0.05)
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, 0x30, 0)
        time.sleep(0.5)
        
        print(f"[{i+1}/10] Sending '9' via SendMessage (background)...")
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, 0x39, 0)
        time.sleep(0.05)
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, 0x39, 0)
        time.sleep(0.5)
    
    print()
    print("✓ Sent 10x '0' and 10x '9' keys via SendMessage (background)")
    print()
    worked = input("Did ANYTHING happen in Roblox? (y/n): ").strip().lower()
    return worked == 'y'

def test_background_postmessage(hwnd):
    """Test PostMessage variant"""
    print("\n" + "=" * 70)
    print("TEST 2: BACKGROUND INPUT (PostMessage)")
    print("=" * 70)
    print()
    print("This will send '0' and '9' via PostMessage (async).")
    print("Watch for any changes!")
    print()
    input("Press Enter when ready...")
    print()
    
    for i in range(10):
        print(f"[{i+1}/10] Sending '0' via PostMessage (background)...")
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x30, 0)
        time.sleep(0.05)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x30, 0)
        time.sleep(0.5)
        
        print(f"[{i+1}/10] Sending '9' via PostMessage (background)...")
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x39, 0)
        time.sleep(0.05)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x39, 0)
        time.sleep(0.5)
    
    print()
    print("✓ Sent 10x '0' and 10x '9' keys via PostMessage (background)")
    print()
    worked = input("Did ANYTHING happen in Roblox? (y/n): ").strip().lower()
    return worked == 'y'

def test_foreground_input(hwnd):
    """Test with window focus (keybd_event)"""
    print("\n" + "=" * 70)
    print("TEST 3: FOREGROUND INPUT (keybd_event with focus)")
    print("=" * 70)
    print()
    print("This will bring Roblox to front and send '0' and '9' with keybd_event.")
    print("This is our CURRENT method - should work!")
    print()
    input("Press Enter when ready...")
    print()
    
    # Bring to front
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.3)
        print("✓ Brought Roblox to foreground")
    except Exception as e:
        print(f"⚠️ Could not focus window: {e}")
        print("Continuing anyway...")
    
    time.sleep(0.5)
    
    from ctypes import windll
    
    for i in range(10):
        print(f"[{i+1}/10] Sending '0' via keybd_event (foreground)...")
        scan_code = win32api.MapVirtualKey(0x30, 0)
        windll.user32.keybd_event(0x30, scan_code, 0, 0)
        time.sleep(0.05)
        windll.user32.keybd_event(0x30, scan_code, 2, 0)  # KEYEVENTF_KEYUP = 2
        time.sleep(0.5)
        
        print(f"[{i+1}/10] Sending '9' via keybd_event (foreground)...")
        scan_code = win32api.MapVirtualKey(0x39, 0)
        windll.user32.keybd_event(0x39, scan_code, 0, 0)
        time.sleep(0.05)
        windll.user32.keybd_event(0x39, scan_code, 2, 0)
        time.sleep(0.5)
    
    print()
    print("✓ Sent 10x '0' and 10x '9' keys via keybd_event (foreground)")
    print()
    worked = input("Did this work? You should see inventory switching! (y/n): ").strip().lower()
    return worked == 'y'

def main():
    print("=" * 70)
    print("VISUAL INPUT VALIDATION TEST")
    print("=" * 70)
    print()
    print("This test makes it OBVIOUS if input methods work.")
    print("You'll see '0' and '9' being sent repeatedly.")
    print()
    print("⚠️ SETUP:")
    print("  1. Make sure Roblox is running")
    print("  2. Make sure you're in-game (not menu)")
    print("  3. Have items in inventory slots 0 and 9")
    print("  4. Stand still and watch your character")
    print()
    
    hwnd = find_roblox()
    if not hwnd:
        return
    
    print()
    print("Ready to test!")
    print()
    
    # Track results
    results = {
        'sendmessage': False,
        'postmessage': False,
        'keybd_event': False
    }
    
    # Test 1: SendMessage (background)
    results['sendmessage'] = test_background_input(hwnd)
    
    # Test 2: PostMessage (background)
    results['postmessage'] = test_background_postmessage(hwnd)
    
    # Test 3: keybd_event (foreground)
    results['keybd_event'] = test_foreground_input(hwnd)
    
    # Results
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print()
    print(f"SendMessage (background):  {'✅ WORKED' if results['sendmessage'] else '❌ BLOCKED'}")
    print(f"PostMessage (background):  {'✅ WORKED' if results['postmessage'] else '❌ BLOCKED'}")
    print(f"keybd_event (foreground):  {'✅ WORKED' if results['keybd_event'] else '❌ BLOCKED'}")
    print()
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print()
    
    if results['sendmessage'] or results['postmessage']:
        print("🎉 AMAZING NEWS!")
        print()
        print("Background input WORKS with Roblox!")
        print("We can remove the focus requirement from the macro!")
        print()
        if results['sendmessage']:
            print("✅ Use SendMessage method")
        if results['postmessage']:
            print("✅ Use PostMessage method")
        print()
        print("The macro can be improved to NOT focus the window!")
    
    elif results['keybd_event']:
        print("✅ Expected result:")
        print()
        print("Only keybd_event (with focus) works.")
        print("This confirms current macro implementation is OPTIMAL.")
        print()
        print("Background input (SendMessage/PostMessage) is BLOCKED by Roblox.")
        print("We MUST focus the window briefly for input to work.")
        print()
        print("Current approach is the best possible solution! 🎯")
    
    else:
        print("⚠️ UNEXPECTED: Nothing worked!")
        print()
        print("Possible issues:")
        print("  - Roblox window not properly focused")
        print("  - Game in menu (not in-game)")
        print("  - Window handle changed")
        print("  - Additional anti-cheat measures")
        print()
        print("Try running the test again while actively in-game.")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
