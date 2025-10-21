# Windows Input Methods - Complete Reference

## Overview
This document catalogs ALL known methods for sending keyboard and mouse input to Windows applications, with specific notes on which work in the background vs. requiring focus.

---

## 🎯 Methods That Work WITHOUT Focus (True Background)

### 1. **SendMessage** - Window Message Queue (Synchronous)
```python
win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
win32api.SendMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
```
- ✅ **No focus required** - Sends directly to window's message queue
- ✅ Works on minimized/background windows
- ❌ Often blocked by anti-cheat (Roblox, games)
- 💡 Best for: Simple applications, controls, editors

### 2. **PostMessage** - Window Message Queue (Asynchronous)
```python
win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
```
- ✅ **No focus required** - Posts to message queue
- ✅ Non-blocking (returns immediately)
- ❌ Often blocked by anti-cheat
- ❌ Can be dropped if queue is full
- 💡 Best for: Fire-and-forget messages

### 3. **SendMessage WM_CHAR** - Character Input
```python
win32api.SendMessage(hwnd, win32con.WM_CHAR, ord('0'), 0)
```
- ✅ **No focus required** - Direct character message
- ✅ Good for text input
- ❌ Blocked by anti-cheat systems
- 💡 Best for: Text boxes, forms

### 4. **SendMessage Mouse Clicks** - Direct Click Messages
```python
lParam = win32api.MAKELONG(x, y)
win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
```
- ✅ **No focus required** - Direct to window
- ✅ Uses window-relative coordinates
- ❌ Often blocked by games
- 💡 Best for: UI automation, controls

### 5. **PostMessage Mouse Clicks** - Async Click Messages
```python
lParam = win32api.MAKELONG(x, y)
win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
```
- ✅ **No focus required** - Async click messages
- ❌ Blocked by anti-cheat
- 💡 Best for: Background automation

---

## 🔒 Methods That REQUIRE Focus (Foreground Only)

### 6. **SendInput** - Hardware Simulation (Modern)
```python
from ctypes import windll, wintypes, Structure, byref, sizeof

extra = c_ulong(0)
ii = INPUT()
ii.type = INPUT_KEYBOARD
ii.union.ki = KEYBDINPUT(vk_code, 0, 0, 0, ctypes.pointer(extra))
windll.user32.SendInput(1, byref(ii), sizeof(ii))
```
- ❌ **Requires focus** - System-level input injection
- ✅ Simulates real hardware input
- ✅ Bypasses some message filters
- ❌ Blocked by BlockInput() calls
- 💡 Best for: Automation when you can control focus

### 7. **keybd_event** - Legacy Keyboard Simulation
```python
scan_code = win32api.MapVirtualKey(vk_code, 0)
windll.user32.keybd_event(vk_code, scan_code, 0, 0)  # Down
windll.user32.keybd_event(vk_code, scan_code, KEYEVENTF_KEYUP, 0)  # Up
```
- ❌ **Requires focus** - Legacy hardware simulation
- ✅ Lower-level than SendInput
- ✅ Works in many games (including Roblox)
- ✅ **THIS IS WHAT CURRENTLY WORKS** in our macro
- 💡 Best for: Games, when SendMessage is blocked

### 8. **mouse_event** - Legacy Mouse Simulation
```python
windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
```
- ❌ **Requires focus** - Legacy mouse simulation
- ✅ Works with SetCursorPos() for positioning
- ⚠️ Deprecated (use SendInput instead)
- 💡 Best for: Legacy compatibility

### 9. **DirectInput-style Scan Codes**
```python
scan_code = win32api.MapVirtualKey(vk_code, 0)
ii.union.ki = KEYBDINPUT(0, scan_code, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
windll.user32.SendInput(1, byref(ii), sizeof(ii))
```
- ❌ **Requires focus** - Hardware scan code simulation
- ✅ Most "hardware-like" method
- ✅ May bypass some anti-cheat
- 💡 Best for: Games with strict input validation

---

## 🎮 Why Roblox Blocks Background Input

### Anti-Cheat Mechanisms:
1. **Message Filter**: Blocks WM_KEYDOWN, WM_CHAR, WM_LBUTTONDOWN from untrusted sources
2. **Focus Check**: Ignores input when not foreground window
3. **Input Validation**: Requires hardware-level simulation (keybd_event, SendInput)
4. **Timing Analysis**: Detects inhuman input patterns

### What Works for Roblox:
- ✅ `keybd_event` with scan codes (our current method)
- ✅ `SendInput` keyboard/mouse
- ✅ Hardware-level DirectInput simulation
- ⚠️ **BUT ALL REQUIRE WINDOW FOCUS**

### What Doesn't Work:
- ❌ SendMessage/PostMessage (blocked by anti-cheat)
- ❌ Any method without window focus
- ❌ Message-based input (WM_KEYDOWN, etc.)

---

## 💡 Current Solution Analysis

Our macro uses **Method 7 (keybd_event with scan codes)** which:
- ✅ Works reliably in Roblox
- ✅ Bypasses most anti-cheat
- ❌ **REQUIRES bringing window to foreground**
- ⚠️ This is intentional - we capture in background but focus for input

### Why We Focus the Window:
```python
# We bring Roblox to front briefly:
self.bring_to_front()  # Focus window
self.send_key(0x30)     # Press '0' with keybd_event
self.restore_window()   # Return to previous window
```

This is actually **the correct approach** because:
1. Background capture works (PrintWindow API)
2. Background input is blocked by Roblox anti-cheat
3. Brief focus for input is necessary evil
4. We restore focus after input

---

## 🔬 Test All Methods

Run `test_all_input_methods.py` to test every method:

```bash
python test_all_input_methods.py
```

This will:
1. Test all 11 input methods
2. Show which work without focus
3. Identify what Roblox accepts
4. Confirm current method is optimal

---

## 📊 Method Comparison Table

| Method | Focus Required? | Works in Roblox? | Anti-Cheat Bypass | Speed |
|--------|----------------|------------------|-------------------|-------|
| SendMessage | ❌ No | ❌ No | ❌ Blocked | ⚡ Fast |
| PostMessage | ❌ No | ❌ No | ❌ Blocked | ⚡⚡ Very Fast |
| SendInput | ✅ Yes | ✅ Yes | ✅ Good | ⚡ Fast |
| keybd_event | ✅ Yes | ✅ **YES** | ✅ Excellent | ⚡ Fast |
| mouse_event | ✅ Yes | ✅ Yes | ✅ Good | ⚡ Fast |

---

## 🎯 Conclusion: Is True Background Input Possible?

### Short Answer: **NO** (for Roblox)

### Why?
1. **Roblox Anti-Cheat**: Explicitly blocks message-based input
2. **Security Design**: Prevents bot automation
3. **Focus Requirement**: Intentional anti-bot measure

### What We Can Do:
1. ✅ Capture window in background (PrintWindow) - **WORKS**
2. ✅ Process images in background - **WORKS**
3. ✅ Briefly focus for input (keybd_event) - **WORKS**
4. ✅ Immediately restore previous window - **WORKS**

### Our Solution:
**Hybrid approach** - Background monitoring + foreground input bursts
- Detection happens in background (no focus needed)
- Input happens with brief focus (0.05-0.1s)
- Previous window restored immediately
- User barely notices the switch

This is **optimal** and likely **as good as it gets** for Roblox.

---

## 🛠️ Advanced Techniques Not Tested

### Potential Methods (Advanced/Risky):
1. **Kernel Driver Input Injection** - Requires driver development
2. **DirectInput Hook** - Complex, may trigger anti-cheat
3. **Memory Writing** - Directly modify game state (DANGEROUS)
4. **Hardware Emulation** - USB device spoofing (expensive)

### Why Not Use These:
- 🚫 Against Roblox ToS
- 🚫 Risk of account ban
- 🚫 Extremely complex
- 🚫 May not work anyway

---

## ✅ Recommendation

**Stick with current implementation:**
- Background capture ✅
- keybd_event with focus ✅
- Quick window switching ✅
- BlockInput for safety ✅

This is the **best possible solution** for Roblox fishing automation without:
- Breaking ToS (arguably already does, but minimally)
- Requiring kernel drivers
- Complex anti-cheat bypass
- Expensive hardware

**The macro works as well as it possibly can given Roblox's restrictions.**
