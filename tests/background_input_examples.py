"""
Example implementations of TRUE background input methods
(These work for regular Windows apps but are BLOCKED by Roblox anti-cheat)
"""

import win32gui
import win32api
import win32con
import time

class BackgroundInputMethods:
    """
    Collection of methods that attempt to send input WITHOUT focusing the window.
    NOTE: These are blocked by Roblox anti-cheat but work for many other applications.
    """
    
    def __init__(self, window_name="Roblox"):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f"Could not find window: {window_name}")
        print(f"Found window: {window_name} (Handle: {self.hwnd})")
    
    # ========================================================================
    # KEYBOARD INPUT - BACKGROUND METHODS
    # ========================================================================
    
    def send_key_with_sendmessage(self, char):
        """
        Send key using SendMessage (WM_KEYDOWN + WM_KEYUP)
        ✅ No focus required
        ❌ Blocked by Roblox
        """
        vk_code = ord(char.upper())
        
        # Calculate lParam (repeat count, scan code, extended key, etc.)
        scan_code = win32api.MapVirtualKey(vk_code, 0)
        lParam = (scan_code << 16) | 1  # Scan code in bits 16-23, repeat count = 1
        
        # Send WM_KEYDOWN
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code, lParam)
        time.sleep(0.05)
        
        # Send WM_KEYUP (bit 30 = previous state, bit 31 = transition state)
        lParam_up = lParam | (0x3 << 30)  # Set bits 30 and 31
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, vk_code, lParam_up)
        
        print(f"✓ SendMessage: Sent '{char}' (VK: 0x{vk_code:02X})")
    
    def send_key_with_postmessage(self, char):
        """
        Send key using PostMessage (WM_KEYDOWN + WM_KEYUP)
        ✅ No focus required
        ✅ Async (doesn't block)
        ❌ Blocked by Roblox
        """
        vk_code = ord(char.upper())
        scan_code = win32api.MapVirtualKey(vk_code, 0)
        lParam = (scan_code << 16) | 1
        
        # Post WM_KEYDOWN
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code, lParam)
        time.sleep(0.05)
        
        # Post WM_KEYUP
        lParam_up = lParam | (0x3 << 30)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, vk_code, lParam_up)
        
        print(f"✓ PostMessage: Sent '{char}' (VK: 0x{vk_code:02X})")
    
    def send_char_with_wm_char(self, char):
        """
        Send character using WM_CHAR message
        ✅ No focus required
        ✅ Good for text input
        ❌ Blocked by Roblox
        """
        char_code = ord(char)
        
        # Send WM_CHAR
        win32api.SendMessage(self.hwnd, win32con.WM_CHAR, char_code, 0)
        
        print(f"✓ WM_CHAR: Sent '{char}' (Code: {char_code})")
    
    def send_text_with_wm_settext(self, text):
        """
        Set text directly using WM_SETTEXT
        ✅ No focus required
        ✅ Sets entire text field
        ❌ Only works for edit controls
        ❌ Not useful for games
        """
        win32api.SendMessage(self.hwnd, win32con.WM_SETTEXT, 0, text)
        print(f"✓ WM_SETTEXT: Set text to '{text}'")
    
    # ========================================================================
    # MOUSE INPUT - BACKGROUND METHODS
    # ========================================================================
    
    def click_with_sendmessage(self, x, y):
        """
        Send click using SendMessage (WM_LBUTTONDOWN + WM_LBUTTONUP)
        ✅ No focus required
        ✅ Uses window-relative coordinates
        ❌ Blocked by Roblox
        
        Args:
            x, y: Coordinates relative to window client area (not screen)
        """
        # Create lParam with x and y coordinates
        lParam = win32api.MAKELONG(x, y)
        
        # Send WM_LBUTTONDOWN
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.05)
        
        # Send WM_LBUTTONUP
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        
        print(f"✓ SendMessage Click: ({x}, {y})")
    
    def click_with_postmessage(self, x, y):
        """
        Send click using PostMessage (WM_LBUTTONDOWN + WM_LBUTTONUP)
        ✅ No focus required
        ✅ Async (doesn't block)
        ❌ Blocked by Roblox
        """
        lParam = win32api.MAKELONG(x, y)
        
        # Post WM_LBUTTONDOWN
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.05)
        
        # Post WM_LBUTTONUP
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        
        print(f"✓ PostMessage Click: ({x}, {y})")
    
    def move_mouse_with_wm_mousemove(self, x, y):
        """
        Move mouse cursor using WM_MOUSEMOVE
        ✅ No focus required
        ❌ Visual only, doesn't trigger hover effects in games
        ❌ Blocked by Roblox
        """
        lParam = win32api.MAKELONG(x, y)
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, lParam)
        print(f"✓ WM_MOUSEMOVE: Moved to ({x}, {y})")
    
    def click_at_center_with_wm_command(self, control_id):
        """
        Click a control using WM_COMMAND
        ✅ No focus required
        ✅ Works for buttons, menus
        ❌ Requires knowing control ID
        ❌ Not useful for games
        """
        # BN_CLICKED notification for buttons
        BN_CLICKED = 0
        wParam = win32api.MAKELONG(control_id, BN_CLICKED)
        win32api.SendMessage(self.hwnd, win32con.WM_COMMAND, wParam, 0)
        print(f"✓ WM_COMMAND: Clicked control {control_id}")
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_window_center(self):
        """Get center coordinates of window client area"""
        rect = win32gui.GetClientRect(self.hwnd)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return width // 2, height // 2
    
    def is_window_visible(self):
        """Check if window is visible"""
        return win32gui.IsWindowVisible(self.hwnd)
    
    def get_window_text(self):
        """Get window title"""
        return win32gui.GetWindowText(self.hwnd)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def demo_background_methods():
    """
    Demonstrate all background input methods
    
    NOTE: These will NOT work with Roblox due to anti-cheat,
    but they work with Notepad, Calculator, and most standard Windows apps.
    """
    
    print("=" * 70)
    print("BACKGROUND INPUT METHODS DEMO")
    print("=" * 70)
    print()
    print("This demo shows methods that work WITHOUT focusing the window.")
    print("These work for most Windows apps but are BLOCKED by Roblox anti-cheat.")
    print()
    
    try:
        # Initialize with Roblox window
        bg_input = BackgroundInputMethods("Roblox")
        
        print(f"Window found: {bg_input.get_window_text()}")
        print(f"Window visible: {bg_input.is_window_visible()}")
        
        center_x, center_y = bg_input.get_window_center()
        print(f"Window center: ({center_x}, {center_y})")
        print()
        
        print("-" * 70)
        print("Testing keyboard input methods...")
        print("-" * 70)
        print()
        
        print("Method 1: SendMessage WM_KEYDOWN/WM_KEYUP")
        bg_input.send_key_with_sendmessage('0')
        time.sleep(1)
        
        print("\nMethod 2: PostMessage WM_KEYDOWN/WM_KEYUP")
        bg_input.send_key_with_postmessage('9')
        time.sleep(1)
        
        print("\nMethod 3: SendMessage WM_CHAR")
        bg_input.send_char_with_wm_char('0')
        time.sleep(1)
        
        print("\n" + "-" * 70)
        print("Testing mouse input methods...")
        print("-" * 70)
        print()
        
        print("Method 4: SendMessage WM_LBUTTONDOWN/WM_LBUTTONUP")
        bg_input.click_with_sendmessage(center_x, center_y)
        time.sleep(1)
        
        print("\nMethod 5: PostMessage WM_LBUTTONDOWN/WM_LBUTTONUP")
        bg_input.click_with_postmessage(center_x, center_y)
        time.sleep(1)
        
        print("\nMethod 6: WM_MOUSEMOVE")
        bg_input.move_mouse_with_wm_mousemove(center_x + 50, center_y + 50)
        time.sleep(1)
        
        print("\n" + "=" * 70)
        print("DEMO COMPLETE")
        print("=" * 70)
        print()
        print("⚠️  IMPORTANT:")
        print("These methods send input to Roblox's window WITHOUT focusing it,")
        print("but Roblox's anti-cheat BLOCKS them from having any effect.")
        print()
        print("This is why our macro uses keybd_event which REQUIRES focus.")
        print()
        print("To test if these methods work, try running this against Notepad:")
        print("  1. Open Notepad")
        print("  2. Change window_name to 'Untitled - Notepad'")
        print("  3. Run this script while Notepad is in background")
        print("  4. You'll see characters appear without Notepad being focused!")
        print()
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nMake sure Roblox window is open with title 'Roblox'")


def test_with_notepad():
    """
    Test background input with Notepad (this WILL work!)
    
    Instructions:
    1. Open Notepad
    2. Keep Notepad in background (don't focus it)
    3. Run this function
    4. Watch text appear in Notepad without it being focused!
    """
    
    print("=" * 70)
    print("TESTING WITH NOTEPAD (This actually works!)")
    print("=" * 70)
    print()
    print("Make sure Notepad is open and in the background...")
    input("Press Enter when ready...")
    print()
    
    try:
        bg_input = BackgroundInputMethods("Untitled - Notepad")
        
        print("Sending keys to Notepad in background...")
        
        # Send some text
        for char in "Hello from background!":
            bg_input.send_char_with_wm_char(char)
            time.sleep(0.1)
        
        print("\n✅ Text should now appear in Notepad!")
        print("This proves the methods work - Roblox just blocks them.")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("Make sure Notepad is open with default title 'Untitled - Notepad'")


# ============================================================================
# ADVANCED: SendMessage with Control-Specific Messages
# ============================================================================

def advanced_control_automation():
    """
    Advanced techniques for automating specific controls
    These work great for standard Windows apps but not for games
    """
    
    # Example: Automate button clicks by control ID
    def click_button_by_id(hwnd, button_id):
        """Click a button using WM_COMMAND"""
        BN_CLICKED = 0
        wParam = win32api.MAKELONG(button_id, BN_CLICKED)
        win32api.SendMessage(hwnd, win32con.WM_COMMAND, wParam, 0)
    
    # Example: Set text in edit control
    def set_edit_text(edit_hwnd, text):
        """Set text in an edit control"""
        win32api.SendMessage(edit_hwnd, win32con.WM_SETTEXT, 0, text)
    
    # Example: Get text from edit control
    def get_edit_text(edit_hwnd):
        """Get text from an edit control"""
        length = win32api.SendMessage(edit_hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
        buffer = win32gui.PyMakeBuffer(length + 1)
        win32api.SendMessage(edit_hwnd, win32con.WM_GETTEXT, length + 1, buffer)
        return buffer[:length]
    
    # Example: Click menu items
    def click_menu_item(hwnd, menu_id):
        """Click a menu item"""
        win32api.SendMessage(hwnd, win32con.WM_COMMAND, menu_id, 0)
    
    print("Advanced control automation examples defined.")
    print("These work for UI automation but not for game automation.")


if __name__ == "__main__":
    print("Select demo to run:")
    print("1. Test with Roblox (will be blocked)")
    print("2. Test with Notepad (will work!)")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        demo_background_methods()
    elif choice == "2":
        test_with_notepad()
    else:
        print("Invalid choice. Running Roblox demo...")
        demo_background_methods()
