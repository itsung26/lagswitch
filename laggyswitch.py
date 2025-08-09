import subprocess
import sys
import ctypes
import os
from pynput import mouse
import threading
import pygame

# Global state variable
firewall_state = False  # False = off (allow), True = on (block)

# Initialize pygame mixer for sound
def init_audio():
    """Initialize pygame mixer for audio playback."""
    try:
        pygame.mixer.init()
        return True
    except:
        print("Warning: Could not initialize audio system")
        return False

def play_sound(sound_type):
    """Play sound based on state change."""
    try:
        if sound_type == "on":
            # You can replace this with a custom sound file path
            # Example: pygame.mixer.Sound("sounds/lag_on.wav").play()
            
            # Generate a simple beep sound programmatically
            duration = 200  # milliseconds
            frequency = 800  # Hz
            import winsound
            winsound.Beep(frequency, duration)
            
        elif sound_type == "off":
            # You can replace this with a custom sound file path
            # Example: pygame.mixer.Sound("sounds/lag_off.wav").play()
            
            # Generate a different beep sound
            duration = 150  # milliseconds
            frequency = 400  # Hz
            import winsound
            winsound.Beep(frequency, duration)
            
    except Exception as e:
        print(f"Could not play sound: {e}")

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Restart the script with administrator privileges."""
    if is_admin():
        # Already running as admin
        return True
    else:
        # Re-run the program with admin rights
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable,  # This will be the .exe path when compiled
                " ".join(sys.argv[1:]),  # Skip the first argument (exe path)
                None, 
                1  # SW_SHOWNORMAL - shows the window normally
            )
        else:
            # Running as Python script
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                " ".join(sys.argv), 
                None, 
                1  # SW_SHOWNORMAL - shows the window normally
            )
        return False
    
def execute_cmd_command(command, run_as_administrator=True):
    """
    Execute a command in Windows Command Prompt.
    
    Args:
        command (str): The command to execute
        run_as_administrator (bool): Whether to run with admin privileges
    
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    
    if run_as_administrator and not is_admin():
        print("This operation requires administrator privileges.")
        print("Attempting to restart with elevated privileges...")
        run_as_admin()
        sys.exit()
    
    try:
        # Execute the command using subprocess
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        
        return result.returncode, result.stdout, result.stderr
        
    except Exception as e:
        return -1, "", str(e)

def execute_firewall_commands(commands, state_description):
    """Execute firewall commands in a separate thread."""
    def run_commands():
        success_count = 0
        for command in commands:
            return_code, stdout, stderr = execute_cmd_command(command, run_as_administrator=True)
            if return_code == 0:
                success_count += 1
        
        if success_count == len(commands):
            print("✓ All commands executed successfully!")
        else:
            print(f"⚠ {success_count}/{len(commands)} commands executed successfully")
    
    # Run commands in separate thread to prevent blocking
    thread = threading.Thread(target=run_commands, daemon=True)
    thread.start()

def on_mouse_click(x, y, button, pressed):
    """Handle mouse click events."""
    global firewall_state
    
    if pressed and button == mouse.Button.x2:  # Mouse5 button
        firewall_state = not firewall_state  # Toggle state
        
        if firewall_state:
            # State is ON - block internet traffic but allow local
            commands = [
                'netsh advfirewall firewall add rule name="Block_Internet_Out" dir=out action=block remoteip=0.0.0.0-223.255.255.255',
                'netsh advfirewall firewall add rule name="Block_Internet_Out2" dir=out action=block remoteip=224.0.0.0-255.255.255.255',
                'netsh advfirewall firewall add rule name="Block_Internet_In" dir=in action=block remoteip=0.0.0.0-223.255.255.255',
                'netsh advfirewall firewall add rule name="Block_Internet_In2" dir=in action=block remoteip=224.0.0.0-255.255.255.255'
            ]
            print("🔴 LAG SWITCH ON - Blocking internet traffic...")
            play_sound("on")
            execute_firewall_commands(commands, "blocking")
        else:
            # State is OFF - remove blocking rules
            commands = [
                'netsh advfirewall firewall delete rule name="Block_Internet_Out"',
                'netsh advfirewall firewall delete rule name="Block_Internet_Out2"',
                'netsh advfirewall firewall delete rule name="Block_Internet_In"',
                'netsh advfirewall firewall delete rule name="Block_Internet_In2"'
            ]
            print("🟢 LAG SWITCH OFF - Allowing internet traffic...")
            play_sound("off")
            execute_firewall_commands(commands, "allowing")

def start_mouse_listener():
    """Start the mouse listener in a separate thread."""
    listener = mouse.Listener(on_click=on_mouse_click)
    listener.start()
    return listener

def set_console_title(title):
    """Set the console window title."""
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    except:
        pass

def main():
    """Main function to demonstrate usage."""
    global firewall_state
    
    # Set console window title
    set_console_title("Lag Switch ALPHA")
    
    # Check if running as admin, if not, restart with elevated privileges
    if not is_admin():
        print("This script requires administrator privileges.")
        print("Attempting to restart with elevated privileges...")
        if not run_as_admin():
            # Only exit if we successfully launched the elevated version
            sys.exit()
    
    # Initialize audio system
    audio_initialized = init_audio()
    if audio_initialized:
        print("✓ Audio system initialized")
    
    # Example usage
    print("Lag Switch - Internet Traffic Blocker")
    print("=" * 40)
    print("✓ Running with administrator privileges")
    
    # Start mouse listener
    print("Starting mouse listener for Mouse5 button...")
    print(f"Current state: {'🔴 ON (blocking internet)' if firewall_state else '🟢 OFF (allowing internet)'}")
    print("Press Mouse5 to toggle lag switch...")
    mouse_listener = start_mouse_listener()

    # Example commands (optional - you can remove this section)
    commands_to_test = [
        "echo Hello from CMD!",
    ]
    
    for cmd in commands_to_test:
        print(f"\nExecuting: {cmd}")
        print("-" * 40)
        
        return_code, stdout, stderr = execute_cmd_command(cmd, run_as_administrator=True)
        
        print(f"Return Code: {return_code}")
        if stdout:
            print("Output:")
            print(stdout)
        if stderr:
            print("Error:")
            print(stderr)

    # keep terminal open and listen for mouse events
    print("\n" + "=" * 50)
    print("Press ENTER to quit")
    print("Mouse5 listener is active. Press Mouse5 to toggle lag switch.")
    print(f"Current state: {'🔴 ON (blocking internet)' if firewall_state else '🟢 OFF (allowing internet)'}")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    # Stop the mouse listener
    mouse_listener.stop()
    print("Lag switch stopped.")


if __name__ == "__main__":
    main()