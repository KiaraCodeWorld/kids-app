# Brain Quest - Desktop Launcher Guide

## Quick Start

You now have a **desktop shortcut** called **"Brain Quest"** that will:
1. ✅ Start the Django development server
2. ✅ Automatically open your browser to http://localhost:8000
3. ✅ Display server logs in a terminal window

### How to Use

**Option 1: Simple (Recommended)**
- Double-click "Brain Quest" on your desktop
- Wait 3-5 seconds for the app to load
- Your browser will automatically open to the app
- A terminal window will show the server running
- Press `Ctrl+C` in the terminal to stop the server

**Option 2: Silent Mode (Alternative)**
- Double-click "Brain Quest (Silent)" on your desktop
- The app runs in the background (no terminal window)
- Browser opens automatically
- You can close the popup message

## What Each File Does

| File | Purpose |
|------|---------|
| `run_app.bat` | Batch script that starts the server and opens the browser |
| `run_app_silent.vbs` | VBScript for silent background execution |
| Desktop Shortcut | Points to run_app.bat for easy access |

## Features Included

- **Automatic Port Cleanup**: Closes any existing process on port 8000
- **Virtual Environment**: Automatically activates the .venv
- **Browser Launch**: Automatically opens http://localhost:8000
- **Server Logs**: Shows all requests and errors in terminal

## Troubleshooting

**Port 8000 Already in Use?**
- The batch file automatically closes any existing process
- If it still fails, manually run: `netstat -ano | find ":8000"` to find the process ID
- Then: `taskkill /PID <id> /F`

**Browser Doesn't Open?**
- Manually go to http://localhost:8000 in your browser
- The server is still running in the terminal

**Virtual Environment Error?**
- Make sure `.venv` folder exists in the Math-Tricks directory
- Run: `python -m venv .venv` to create it if missing

## Available Features

Once the app is running, you can access:

- **🎯 Speed Tests** - Timed math challenges for each trick
- **🔤 Spelling Bee** - Learn spelling with audio pronunciation
- **📚 Vocabulary** - Everyday vocabulary with AI explanations
- **🏆 Lessons** - Math tricks organized by difficulty
- **⚡ Challenges** - Quick mental math puzzles

## Keyboard Shortcuts in App

- **Speed Test**: Press Enter to submit answer
- **Spelling Bee**: Press Enter after typing word
- **Vocabulary**: Click buttons to navigate

## Stopping the Server

1. Find the terminal window running the server
2. Press `Ctrl+C`
3. Type `Y` and press Enter to confirm

Or close the terminal window directly.

## Need Help?

Check that:
1. Python is installed: `python --version`
2. Django is installed: `python -m django --version`
3. You're in the correct directory: `c:\Users\vrajp\CodeFolder\Fun-Projects\Math-Tricks`

---

**Enjoy learning! 🚀**
