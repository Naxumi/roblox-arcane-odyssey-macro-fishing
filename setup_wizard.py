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
