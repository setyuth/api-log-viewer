# 🏗️ Building Standalone Executable

Guide to create a standalone executable that supports drag & drop functionality.

## 📋 Prerequisites

Install PyInstaller:
```bash
pip install pyinstaller
```

## 🔨 Build Methods

### Method 1: Simple Executable (Recommended)

```bash
# Build single executable file
pyinstaller --onefile --name="LogViewer" --icon=icon.ico logviewer_standalone.py
```

**Output:** `dist/LogViewer.exe` (Windows) or `dist/LogViewer` (Linux/macOS)

### Method 2: With Console Window

```bash
# Build with visible console (better for debugging)
pyinstaller --onefile --console --name="LogViewer" logviewer_standalone.py
```

### Method 3: Windows Only - No Console

```bash
# Build without console window (Windows GUI mode)
pyinstaller --onefile --noconsole --name="LogViewer" --icon=icon.ico logviewer_standalone.py
```

**Note:** `--noconsole` is NOT recommended for this terminal-based app!

## 📦 Complete Build Script

### Windows (build_windows.bat)

```batch
@echo off
echo ========================================
echo Building API Log Viewer for Windows
echo ========================================

REM Install/upgrade PyInstaller
pip install --upgrade pyinstaller

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist LogViewer.spec del LogViewer.spec

REM Build executable
pyinstaller --onefile ^
    --console ^
    --name="LogViewer" ^
    --add-data "README.md;." ^
    logviewer_standalone.py

echo.
echo ========================================
echo Build complete!
echo Executable: dist\LogViewer.exe
echo ========================================
echo.
echo Usage:
echo 1. Double-click LogViewer.exe
echo 2. Drag and drop a log file onto it
echo 3. Or run: LogViewer.exe your_log_file.log
echo.
pause
```

### Linux/macOS (build_unix.sh)

```bash
#!/bin/bash

echo "========================================"
echo "Building API Log Viewer for Unix"
echo "========================================"

# Install/upgrade PyInstaller
pip3 install --upgrade pyinstaller

# Clean previous builds
rm -rf build dist LogViewer.spec

# Build executable
pyinstaller --onefile \
    --console \
    --name="LogViewer" \
    --add-data "README.md:." \
    logviewer_standalone.py

echo ""
echo "========================================"
echo "Build complete!"
echo "Executable: dist/LogViewer"
echo "========================================"
echo ""
echo "Usage:"
echo "1. Run: ./dist/LogViewer"
echo "2. Or: ./dist/LogViewer your_log_file.log"
echo ""

# Make executable
chmod +x dist/LogViewer
```

## 🎯 Using the Executable

### Windows

#### Option 1: Drag & Drop
1. Locate `dist/LogViewer.exe`
2. Drag your `.log` file onto `LogViewer.exe`
3. The viewer opens automatically with your log loaded

#### Option 2: Command Line
```cmd
LogViewer.exe path\to\your\logfile.log
```

#### Option 3: Create Desktop Shortcut
1. Right-click `LogViewer.exe` → Create Shortcut
2. Move shortcut to Desktop
3. Drag log files onto the shortcut

### Linux/macOS

#### Option 1: Command Line
```bash
./LogViewer /path/to/your/logfile.log
```

#### Option 2: File Manager
- Set `LogViewer` as default application for `.log` files
- Double-click log files to open with LogViewer

## 📝 Advanced Build Options

### Optimize Size

```bash
# Build with UPX compression (requires UPX installed)
pyinstaller --onefile --upx-dir=/path/to/upx logviewer_standalone.py
```

### Include Icon

```bash
# Windows with custom icon
pyinstaller --onefile --icon=logviewer.ico --name="LogViewer" logviewer_standalone.py
```

### Hide Imports (Security)

```bash
# Obfuscate imports
pyinstaller --onefile --key="your-secret-key" logviewer_standalone.py
```

### Add Version Info (Windows)

Create `version_info.txt`:
```ini
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
        StringStruct(u'FileDescription', u'API Log Viewer'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'ProductName', u'LogViewer'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Build with version info:
```bash
pyinstaller --onefile --version-file=version_info.txt logviewer_standalone.py
```

## 🚀 Distribution

### Create Installer (Windows)

Use Inno Setup to create installer:

**installer_script.iss:**
```ini
[Setup]
AppName=API Log Viewer
AppVersion=1.0
DefaultDirName={pf}\LogViewer
DefaultGroupName=LogViewer
OutputDir=output
OutputBaseFilename=LogViewerSetup

[Files]
Source: "dist\LogViewer.exe"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"

[Icons]
Name: "{group}\Log Viewer"; Filename: "{app}\LogViewer.exe"
Name: "{commondesktop}\Log Viewer"; Filename: "{app}\LogViewer.exe"

[Registry]
Root: HKCR; Subkey: ".log"; ValueType: string; ValueName: ""; ValueData: "LogFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "LogFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\LogViewer.exe"" ""%1"""
```

Compile with Inno Setup Compiler.

### Create DMG (macOS)

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "LogViewer" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "LogViewer.app" 200 190 \
  --hide-extension "LogViewer.app" \
  --app-drop-link 600 185 \
  "LogViewer-1.0.dmg" \
  "dist/"
```

## ✅ Testing the Executable

### Test Checklist

- [ ] Runs without Python installed
- [ ] Accepts drag & drop files
- [ ] Accepts command-line arguments
- [ ] Displays Unicode text correctly
- [ ] All features work (filter, view, export)
- [ ] No console errors
- [ ] Reasonable file size (< 20MB)

### Test Commands

```bash
# Test basic run
./LogViewer

# Test with file
./LogViewer test.log

# Test non-existent file
./LogViewer nonexistent.log

# Test with Unicode filename
./LogViewer test_ážœáž·ážšáŸˆ.log
```

## 🐛 Troubleshooting

### Issue: "Failed to execute script"

**Solution:** Build with `--console` flag to see errors:
```bash
pyinstaller --onefile --console logviewer_standalone.py
```

### Issue: Large file size (>50MB)

**Solution:** Exclude unnecessary packages:
```bash
pyinstaller --onefile --exclude-module matplotlib --exclude-module numpy logviewer_standalone.py
```

### Issue: Antivirus blocks executable

**Solution:** 
1. Sign the executable with a code signing certificate
2. Or add exception in antivirus
3. Or distribute as Python script

### Issue: Slow startup

**Solution:** Use `--onedir` instead of `--onefile`:
```bash
pyinstaller --onedir --name="LogViewer" logviewer_standalone.py
```

## 📊 Build Comparison

| Method | Size | Speed | Distribution |
|--------|------|-------|--------------|
| --onefile | ~15MB | Slower startup | Single file |
| --onedir | ~30MB | Fast startup | Folder with DLLs |
| Python script | 50KB | Fastest | Requires Python |

## 🎁 Final Distribution Package

Create a release package:

```
LogViewer-v1.0/
├── LogViewer.exe (or LogViewer)
├── README.md
├── USAGE_GUIDE.md
├── examples/
│   ├── sample_json.log
│   ├── sample_text.log
│   └── sample_api_format.log
└── LICENSE
```

Zip and distribute!

---

**You now have a standalone executable that users can run without installing Python!**