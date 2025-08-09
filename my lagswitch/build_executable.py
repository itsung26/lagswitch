"""
Build script to create executable for the lag switch program.
This script will compile laggyswitch.py into a standalone executable.
"""

import subprocess
import os
import sys

def build_executable():
    """Build the executable using PyInstaller."""
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "laggyswitch.py")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window (we'll handle this ourselves)
        "--name", "LagSwitch",  # Name of the executable
        "--icon", "NONE",  # No icon for now
        "--clean",  # Clean before building
        script_path
    ]
    
    print("Building executable...")
    print("Command:", " ".join(cmd))
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build successful!")
        print("\nOutput:")
        print(result.stdout)
        
        # Check if executable was created
        exe_path = os.path.join(current_dir, "dist", "LagSwitch.exe")
        if os.path.exists(exe_path):
            print(f"\n✓ Executable created: {exe_path}")
            print("\nYou can now run the executable directly!")
            print("It will automatically request admin privileges when needed.")
        else:
            print("\n⚠ Executable not found in expected location")
            
    except subprocess.CalledProcessError as e:
        print("✗ Build failed!")
        print("Error output:")
        print(e.stderr)
        return False
    
    return True

if __name__ == "__main__":
    build_executable()
