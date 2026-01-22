# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-22

### 🎉 Initial Release

First stable release of API Log Viewer with full Java/Spring application log support.

### ✨ Added

#### Core Features
- Terminal-based log viewer with Rich UI library
- Smart log parsing for multiple formats (JSON, Java/Spring, Apache/Nginx, generic text)
- Interactive command-line interface with auto-completion hints
- Real-time filtering and searching
- Log entry editing and saving
- Export filtered results to new files

#### Java/Spring Log Support
- Thread name extraction and filtering (`http-nio-*`, `SimpleAsyncTaskExecutor-*`)
- Service/Controller name detection (`BackendInvoiceCntr`, `InvoiceDataEntryCntr`)
- START/STOP operation lifecycle tracking
- Custom error code mapping (RSLT_CD[719] → HTTP 404)
- Logger class path extraction

#### Filtering Capabilities
- Filter by log level (DEBUG, INFO, WARN, ERROR, FATAL, CRITICAL)
- Filter by HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
- Filter by HTTP status code (200, 404, 500, etc.)
- Filter by thread name (partial match support)
- Filter by service/controller name (partial match support)
- Full-text search with Unicode support

#### Display Features
- Color-coded log levels (DEBUG=cyan, INFO=green, WARN=yellow, ERROR=red)
- Color-coded HTTP status codes (2xx=green, 3xx=blue, 4xx=yellow, 5xx=red)
- Color-coded messages based on log level
- Millisecond-precision timestamps
- Truncated field display with overflow handling
- Statistics summary with top threads and services

#### Unicode Support
- Full UTF-8 encoding support
- Display of Khmer, Chinese, Japanese, Korean, Thai, Arabic text
- Unicode-safe searching and filtering
- Proper text truncation for multi-byte characters

#### Standalone Executable
- Single-file executable generation with PyInstaller
- Drag & drop file support (Windows)
- Command-line argument support
- Interactive file path input
- No Python installation required for end users

#### Documentation
- Comprehensive README with examples
- Quick start guide
- Usage guide with detailed examples
- Build instructions for standalone executable
- Contributing guidelines
- Code of conduct

#### Examples
- Sample JSON log file
- Sample text log file  
- Sample Java/Spring application log file (real-world format)

### 🔧 Technical Details

#### Architecture
- Modular code structure with separation of concerns
- `LogEntry` model for log parsing and data storage
- `LogViewer` class for display and filtering logic
- Clean helper utilities
- Configuration-driven design

#### Performance
- Efficient parsing with regex and JSON libraries
- Progress tracking for large file loads
- Tested with files up to 3.34 MB (6,871+ entries)
- Memory-efficient filtering

#### Parsing Capabilities
- **Timestamps**: ISO 8601, time-only, various custom formats
- **Log Levels**: Case-insensitive detection
- **HTTP Methods**: All standard methods
- **Endpoints**: Path extraction from multiple patterns
- **Status Codes**: 3-digit codes and custom application codes
- **Response Times**: Milliseconds and seconds with auto-conversion

### 🐛 Bug Fixes

- Fixed `'dict' object has no attribute 'startswith'` error when message field contains nested JSON
- Added type checking in `get_display_message()` method
- Ensured message field is always converted to string
- Safe handling of malformed JSON in log lines
- Proper error handling for missing files
- Graceful handling of encoding errors with `errors='replace'`

### 🔒 Security

- No external network calls
- File path validation
- Input sanitization for user commands
- Safe file operations with proper exception handling

### 📦 Dependencies

- `rich >= 13.7.0` - Terminal UI library (only production dependency)
- `pyinstaller` - For building standalone executables (optional)
- `pytest` - For running tests (dev dependency)
- `pytest-cov` - For coverage reports (dev dependency)

### 🎯 Tested On

- **Windows**: Windows 10, Windows 11
- **Linux**: Ubuntu 20.04, Ubuntu 22.04
- **macOS**: macOS 12 (Monterey), macOS 13 (Ventura)
- **Python**: 3.7, 3.8, 3.9, 3.10, 3.11

### 📝 Known Limitations

- Very large files (>100MB) may take significant time to load
- Some exotic timestamp formats may not be auto-detected
- Binary log files are not supported
- Browser storage APIs (localStorage) not available in artifacts

### 🔜 Future Plans

See roadmap in README.md for upcoming features.

---

## Release Notes

This is the first stable release suitable for production use. The tool has been tested with real-world Java/Spring application logs and handles various edge cases including:

- Mixed log formats in the same file
- Embedded JSON in text logs
- Multi-threaded application logs
- Unicode text in messages
- Large log files (3MB+, 6000+ entries)
- Custom error codes and messages

### Migration Guide

This is the initial release, no migration needed.

### Download

- **Source Code**: [v1.0.0.zip](https://github.com/setyuth/api-log-viewer/archive/refs/tags/v1.0.0.zip)
- **Standalone Executable (Windows)**: [LogViewer-v1.0.0-windows.zip](https://github.com/setyuth/api-log-viewer/releases/download/v1.0.0/LogViewer-v1.0.0-windows.zip)
- **Standalone Executable (Linux)**: [LogViewer-v1.0.0-linux.tar.gz](hhttps://github.com/setyuth/api-log-viewer/releases/download/v1.0.0/LogViewer-v1.0.0-linux.tar.gz)
- **Standalone Executable (macOS)**: [LogViewer-v1.0.0-macos.tar.gz](hhttps://github.com/setyuth/api-log-viewer/releases/download/v1.0.0/LogViewer-v1.0.0-macos.tar.gz)

### Checksums

```
SHA256 checksums will be provided with release binaries
```

---

**Full Changelog**: hhttps://github.com/setyuth/api-log-viewer/commits/v1.0.0