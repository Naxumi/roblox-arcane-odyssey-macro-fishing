"""
Setup wizard for first-time configuration
Guides users through setting up the fishing macro
"""

import os
import sys
import shutil

def setup_wizard():
    """Interactive setup wizard for first-time users"""
    print("=" * 60)
    print("🎣 Roblox Arcane Odyssey - Fishing Macro Setup Wizard")
    print("=" * 60)
    print()
    print("This wizard will help you configure the fishing macro.")
    print("You can change these settings later in config.py")
    print()
    
    # Check if config.example.py exists
    if not os.path.exists("config.example.py"):
        print("❌ ERROR: config.example.py not found!")
        print("Please make sure you have all files from the repository.")
        input("\nPress Enter to exit...")
        return False
    
    # Check if config.py already exists
    if os.path.exists("config.py"):
        print("⚠️  config.py already exists!")
        overwrite = input("Do you want to reconfigure? This will backup your current config. (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled. Your existing config.py was not modified.")
            input("\nPress Enter to exit...")
            return False
        else:
            # Backup existing config
            backup_name = "config.py.backup"
            shutil.copy("config.py", backup_name)
            print(f"✅ Backed up existing config to {backup_name}")
            print()
    
    # Copy example to config.py
    shutil.copy("config.example.py", "config.py")
    print("✅ Created config.py from template")
    print()
    
    config_updates = {}
    
    # Discord webhook setup
    print("-" * 60)
    print("📱 DISCORD NOTIFICATIONS SETUP")
    print("-" * 60)
    print()
    print("Would you like to receive Discord notifications when fish are caught?")
    print("This requires a Discord webhook URL.")
    print()
    print("To get a webhook URL:")
    print("1. Go to your Discord server")
    print("2. Server Settings > Integrations > Webhooks")
    print("3. Create New Webhook > Copy Webhook URL")
    print()
    
    enable_discord = input("Enable Discord notifications? (y/n, default=n): ").strip().lower()
    
    if enable_discord == 'y':
        webhook_url = input("Paste your Discord webhook URL: ").strip()
        if webhook_url:
            config_updates['DISCORD_WEBHOOK_URL'] = webhook_url
            config_updates['ENABLE_DISCORD_NOTIFICATIONS'] = 'True'
            print("✅ Discord notifications enabled!")
            
            # Ask for Discord User ID for mentions
            print()
            print("To receive @mentions in Discord notifications:")
            print("1. Enable Developer Mode: User Settings > Advanced > Developer Mode")
            print("2. Right-click your profile > Copy User ID")
            print()
            user_id = input("Enter your Discord User ID (leave empty to skip): ").strip()
            if user_id:
                config_updates['DISCORD_MENTION_USER_ID'] = user_id
                print("✅ Discord mentions enabled - you'll be tagged for important alerts!")
            else:
                print("ℹ️  Discord mentions disabled")
        else:
            print("⚠️  No webhook URL provided - Discord notifications disabled")
            config_updates['ENABLE_DISCORD_NOTIFICATIONS'] = 'False'
    else:
        config_updates['ENABLE_DISCORD_NOTIFICATIONS'] = 'False'
        print("ℹ️  Discord notifications disabled")
    
    print()
    
    # Detection confidence setup
    print("-" * 60)
    print("🎯 DETECTION SENSITIVITY SETUP")
    print("-" * 60)
    print()
    print("⚠️  IMPORTANT: Detection accuracy depends heavily on your monitor resolution!")
    print()
    print("Detection confidence determines how similar images must be to trigger.")
    print("Range: 0.0 (very sensitive) to 1.0 (very strict)")
    print()
    print("Recommended values:")
    print("- Point detection (fishing bite): 0.65-0.75")
    print("- Catch detection: 0.75-0.85")
    print()
    print("⚠️  You may need to retake screenshots at YOUR resolution for best results!")
    print()
    
    use_defaults = input("Use default detection values? (y/n, default=y): ").strip().lower()
    
    if use_defaults != 'n':
        print("✅ Using default detection values")
    else:
        print()
        try:
            point_conf = float(input("Point detection confidence (default=0.65): ") or "0.65")
            catch_conf = float(input("Catch detection confidence (default=0.75): ") or "0.75")
            config_updates['POINT_CONFIDENCE'] = str(point_conf)
            config_updates['FISH_CONFIDENCE'] = str(catch_conf)
            config_updates['TREASURE_CONFIDENCE'] = str(catch_conf)
            config_updates['SUNKEN_CONFIDENCE'] = str(catch_conf)
            print("✅ Custom detection values set!")
        except ValueError:
            print("⚠️  Invalid input - using default values")
    
    print()
    
    # Eating setup
    print("-" * 60)
    print("🍖 EATING SCHEDULE SETUP")
    print("-" * 60)
    print()
    print("The macro will automatically eat food at regular intervals.")
    print("This prevents hunger from affecting fishing.")
    print()
    print("You'll be prompted for eating settings each time you run the macro,")
    print("but you can set defaults here.")
    print()
    
    try:
        eating_count = int(input("Default number of food items per eating session (default=3): ") or "3")
        eating_interval = int(input("Default eating interval in seconds (default=300): ") or "300")
        config_updates['DEFAULT_EATING_COUNT'] = str(eating_count)
        config_updates['DEFAULT_EATING_INTERVAL'] = str(eating_interval)
        print(f"✅ Default: Eat {eating_count} food items every {eating_interval}s ({eating_interval//60}m) continuously")
    except ValueError:
        print("⚠️  Invalid input - using default values (3 items, 300s)")
    
    print()
    
    # Screenshot settings
    print("-" * 60)
    print("📸 SCREENSHOT SETTINGS")
    print("-" * 60)
    print()
    print("The macro can save screenshots when fish are caught.")
    print("These are sent to Discord (if enabled) and then deleted to save space.")
    print()
    
    save_screenshots = input("Save detection screenshots? (y/n, default=y): ").strip().lower()
    config_updates['SAVE_DETECTION_SCREENSHOTS'] = 'True' if save_screenshots != 'n' else 'False'
    
    if save_screenshots != 'n':
        delete_after = input("Delete screenshots after sending to Discord? (y/n, default=y): ").strip().lower()
        config_updates['DELETE_SCREENSHOTS_AFTER_DISCORD'] = 'True' if delete_after != 'n' else 'False'
    
    print()
    
    # Video recording settings
    print("-" * 60)
    print("🎥 VIDEO RECORDING SETTINGS")
    print("-" * 60)
    print()
    print("The macro can record videos when fishing issues are detected.")
    print("Videos provide better context than screenshots for debugging detection problems.")
    print()
    print("Default video settings:")
    print("- Duration: 5 seconds")
    print("- FPS: 15 (smooth + small file size, ~1-3MB per video)")
    print("- Quality: 23 (H.264 CRF - balanced quality/size)")
    print("- Codec: H.264 MP4 (compressed, plays in Discord)")
    print()
    print("⚠️ Note: Recording uses ~10-15% more CPU during the recording period")
    print()
    
    record_video = input("Enable video recording for fishing issues? (y/n, default=y): ").strip().lower()
    config_updates['RECORD_DETECTION_VIDEO'] = 'True' if record_video != 'n' else 'False'
    
    if record_video != 'n':
        print()
        
        # Delete videos after Discord
        delete_videos = input("Delete videos after sending to Discord? (y/n, default=y): ").strip().lower()
        config_updates['DELETE_VIDEOS_AFTER_DISCORD'] = 'True' if delete_videos != 'n' else 'False'
        
        # Optional: Custom duration
        print()
        print("Video duration options:")
        print("- 3 seconds: Short, quick captures")
        print("- 5 seconds: Standard, good balance [RECOMMENDED]")
        print("- 10 seconds: Long, full context")
        custom_duration = input("Use custom duration? (leave empty for default 5s): ").strip()
        if custom_duration and custom_duration.isdigit():
            duration = int(custom_duration)
            if 1 <= duration <= 30:
                config_updates['VIDEO_DURATION'] = custom_duration
                print(f"✅ Video duration set to {duration} seconds")
            else:
                print("⚠️  Invalid duration (must be 1-30s) - using default (5s)")
        
        # Optional: Custom FPS
        print()
        print("Video FPS (frames per second) options:")
        print("- 10 FPS: Lower quality, smallest files (~0.5-1MB)")
        print("- 15 FPS: Smooth, small files (~1-2MB) [RECOMMENDED]")
        print("- 30 FPS: Very smooth, larger files (~2-4MB)")
        custom_fps = input("Use custom FPS? (leave empty for default 15 FPS): ").strip()
        if custom_fps and custom_fps.isdigit():
            fps = int(custom_fps)
            if 5 <= fps <= 60:
                config_updates['VIDEO_FPS'] = custom_fps
                print(f"✅ Video FPS set to {fps}")
            else:
                print("⚠️  Invalid FPS (must be 5-60) - using default (15)")
        
        # Optional: Custom quality
        print()
        print("Video quality (H.264 CRF) options:")
        print("- 18: High quality, larger files (~3-5MB)")
        print("- 23: Balanced quality/size (~1-3MB) [RECOMMENDED]")
        print("- 28: Lower quality, smaller files (~0.5-1.5MB)")
        print()
        print("Note: Lower CRF = better quality but larger file size")
        custom_quality = input("Use custom quality? (leave empty for default 23): ").strip()
        if custom_quality and custom_quality.isdigit():
            quality = int(custom_quality)
            if 0 <= quality <= 51:
                config_updates['VIDEO_QUALITY'] = custom_quality
                print(f"✅ Video quality set to CRF {quality}")
            else:
                print("⚠️  Invalid quality (must be 0-51) - using default (23)")
    
    print()
    
    # Combat detection settings
    print("-" * 60)
    print("⚔️  COMBAT DETECTION SETTINGS")
    print("-" * 60)
    print()
    print("The macro can monitor for combat and alert you via Discord.")
    print("This helps prevent being attacked while AFK fishing.")
    print()
    print("How it works:")
    print("1. Continuously monitors for combat_arcane_odyssey.png")
    print("2. If detected: Sends Discord alert with @mention (3 times)")
    print("3. After 10 seconds: Can optionally close Roblox (leave the game)")
    print()
    
    enable_combat = input("Enable combat detection? (y/n, default=y): ").strip().lower()
    config_updates['ENABLE_COMBAT_DETECTION'] = 'True' if enable_combat != 'n' else 'False'
    
    if enable_combat != 'n':
        print()
        print("⚠️  AUTO-KILL OPTION:")
        print("If combat is detected and you don't respond,")
        print("the macro can automatically close Roblox (leave the game).")
        print()
        auto_kill = input("Enable auto-kill Roblox when combat detected? (y/n, default=n): ").strip().lower()
        config_updates['COMBAT_AUTO_KILL_ROBLOX'] = 'True' if auto_kill == 'y' else 'False'
        
        if auto_kill == 'y':
            print()
            print("⚡ INSTANT KILL OPTION:")
            print("Choose kill timing:")
            print("  - INSTANT: Kill Roblox immediately when combat detected (no delay)")
            print("  - DELAYED: Wait X seconds before killing (gives you time to respond)")
            print()
            instant_kill = input("Use instant kill? (y/n, default=n): ").strip().lower()
            config_updates['COMBAT_INSTANT_KILL'] = 'True' if instant_kill == 'y' else 'False'
            
            if instant_kill == 'y':
                print("✅ Instant kill enabled - Roblox will close IMMEDIATELY when combat detected")
            else:
                print()
                print("⏱️  KILL DELAY CONFIGURATION:")
                print("How many seconds to wait before killing Roblox after combat detected?")
                print("This gives you time to respond and cancel if it's a false positive.")
                print()
                try:
                    kill_delay = int(input("Kill delay in seconds (default=10): ") or "10")
                    if kill_delay < 1:
                        print("⚠️  Invalid delay - using default (10 seconds)")
                        kill_delay = 10
                    config_updates['COMBAT_KILL_DELAY'] = str(kill_delay)
                    print(f"✅ Delayed kill enabled - Roblox will close {kill_delay}s after combat detection")
                except ValueError:
                    print("⚠️  Invalid input - using default (10 seconds)")
                    config_updates['COMBAT_KILL_DELAY'] = '10'
                    print("✅ Delayed kill enabled - Roblox will close 10s after combat detection")
        else:
            config_updates['COMBAT_INSTANT_KILL'] = 'False'
            print("ℹ️  Auto-kill disabled - you'll be notified but game won't close")
    else:
        print("ℹ️  Combat detection disabled")
    
    print()
    
    # Moderator detection settings
    print("-" * 60)
    print("👮 MODERATOR DETECTION SETTINGS")
    print("-" * 60)
    print()
    print("The macro can monitor for game moderators and alert you via Discord.")
    print("This helps avoid being caught macro fishing by moderators.")
    print()
    print("How it works:")
    print("1. Continuously monitors for moderator_arcane_odyssey.png icon")
    print("2. If detected: Sends immediate Discord alert with @mention (3 times)")
    print("3. Screenshot sent to show moderator presence")
    print()
    print("⚠️  IMPORTANT: You must take a screenshot of the moderator icon at YOUR resolution!")
    print("Save it as: assets/images/detection/moderator_arcane_odyssey.png")
    print()
    
    enable_moderator = input("Enable moderator detection? (y/n, default=y): ").strip().lower()
    config_updates['ENABLE_MODERATOR_DETECTION'] = 'True' if enable_moderator != 'n' else 'False'
    
    if enable_moderator != 'n':
        print("✅ Moderator detection enabled - you'll be @mentioned when moderators are nearby")
        config_updates['MENTION_ON_MODERATOR_DETECTED'] = 'True'
        
        print()
        print("⚠️  AUTO-LEAVE OPTION:")
        print("If a moderator is detected and you don't respond,")
        print("the macro can automatically close Roblox (leave the game).")
        print("This only works when script is NOT paused.")
        print()
        print("💡 SMART INTERACTION: If delay >= 5 seconds, the macro will:")
        print("   1. Jump once (spacebar)")
        print("   2. Type '/hi' in chat and send it")
        print("   3. Take a screenshot")
        print("   4. Then close Roblox after the delay")
        print("   This makes you appear active to the moderator!")
        print()
        auto_leave = input("Enable auto-leave when moderator detected? (y/n, default=n): ").strip().lower()
        config_updates['MODERATOR_AUTO_LEAVE'] = 'True' if auto_leave == 'y' else 'False'
        
        if auto_leave == 'y':
            print()
            print("⏱️ LEAVE DELAY:")
            print("How long to wait before automatically closing Roblox?")
            print("This gives you time to respond if you're at the computer.")
            print()
            print("Recommended: 5-10 seconds")
            try:
                leave_delay = int(input("Enter delay in seconds (default=5): ") or "5")
                if 1 <= leave_delay <= 60:
                    config_updates['MODERATOR_LEAVE_DELAY'] = str(leave_delay)
                    print(f"✅ Auto-leave enabled - Roblox will close {leave_delay}s after moderator detection")
                else:
                    print("⚠️  Invalid delay (must be 1-60) - using default (5 seconds)")
                    config_updates['MODERATOR_LEAVE_DELAY'] = '5'
            except ValueError:
                print("⚠️  Invalid input - using default (5 seconds)")
                config_updates['MODERATOR_LEAVE_DELAY'] = '5'
        else:
            print("ℹ️  Auto-leave disabled - you'll be notified but game won't close")
    else:
        print("ℹ️  Moderator detection disabled")
    
    print()
    
    # Update config.py
    print("-" * 60)
    print("💾 SAVING CONFIGURATION")
    print("-" * 60)
    print()
    
    try:
        # Read current config
        with open("config.py", "r", encoding="utf-8") as f:
            config_content = f.read()
        
        # Update values
        for key, value in config_updates.items():
            if key == 'DISCORD_WEBHOOK_URL':
                # Special handling for webhook URL (keep quotes)
                config_content = config_content.replace(
                    f'{key} = ""',
                    f'{key} = "{value}"'
                )
            else:
                # For other values, use regex to replace the line
                import re
                pattern = rf'^{key} = .*$'
                replacement = f'{key} = {value}'
                config_content = re.sub(pattern, replacement, config_content, flags=re.MULTILINE)
        
        # Write updated config
        with open("config.py", "w", encoding="utf-8") as f:
            f.write(config_content)
        
        print("✅ Configuration saved to config.py")
        print()
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        print("You may need to edit config.py manually.")
        print()
    
    # Final instructions
    print("=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("⚠️  CRITICAL: RESOLUTION-DEPENDENT DETECTION")
    print("-" * 60)
    print("The provided detection images may NOT work for your resolution!")
    print()
    print("Next steps:")
    print()
    print("1. TEST the macro with provided images first")
    print("   - Run: python background_fishing_macro.py")
    print("   - Watch if it detects fishing bites correctly")
    print()
    print("2. If detection FAILS, you MUST retake screenshots:")
    print("   a. Launch Roblox Arcane Odyssey at YOUR resolution")
    print("   b. Take screenshot of fishing bite indicator:")
    print("      - Use Snipping Tool (Win + Shift + S)")
    print("      - Save as: assets/images/detection/point.png")
    print("   c. (Optional) Take screenshots of caught screens")
    print("   d. Adjust POINT_CONFIDENCE in config.py if needed")
    print()
    print("3. Set up your inventory:")
    print("   - Slot 0: Food items")
    print("   - Slot 9: Fishing rod")
    print()
    print("4. Run the macro:")
    print("   - python background_fishing_macro.py")
    print()
    print("5. Press Ctrl+Alt+M anytime to emergency stop")
    print()
    print("For more help, read README.md")
    print()
    
    input("Press Enter to exit setup wizard...")
    return True


if __name__ == "__main__":
    setup_wizard()
