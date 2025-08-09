# Lag Switch Executable

## What was created:

1. **LagSwitch.exe** - Your compiled lag switch program in the `dist` folder
2. **Run_LagSwitch_as_Admin.bat** - A batch file to easily run the program

## How to use:

### Option 1: Direct execution
- Navigate to the `dist` folder
- Double-click `LagSwitch.exe`
- When prompted for admin privileges, click "Yes"

### Option 2: Using the batch file
- Double-click `Run_LagSwitch_as_Admin.bat`
- This will guide you through running the program with admin rights

## Features:
- **Mouse5 (side mouse button)** toggles the lag switch on/off
- **Audio feedback** with beep sounds when toggling
- **Console display** showing current state
- **Automatic admin privilege handling**

## What the lag switch does:
- **ON**: Blocks internet traffic while allowing local network traffic
- **OFF**: Restores normal internet connectivity

## Notes:
- The executable is standalone and doesn't require Python to be installed
- It will automatically request administrator privileges when needed
- The console window will stay open so you can see the status
- Press Enter in the console to quit the program

## Troubleshooting:
- If the program doesn't work, make sure you clicked "Yes" on the UAC prompt
- The program requires administrator privileges to modify Windows Firewall rules
- Make sure your mouse has a Mouse5 button (usually a side button)

The executable is about 17MB and contains all necessary dependencies.
