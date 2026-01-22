# 🔍 API Log Viewer v1.0.0

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)](https://github.com/yourusername/api-log-viewer/releases)

A feature-rich, terminal-based tool for viewing, filtering, and editing API logs. Built with Python and Rich for a beautiful CLI experience. **Enhanced with full support for Java/Spring application logs and Unicode text.**

![API Log Viewer Demo](https://via.placeholder.com/800x400?text=API+Log+Viewer+Demo)

## ✨ Features

- **📊 Beautiful Terminal UI** - Colorful, organized output using Rich library
- **🔍 Smart Log Parsing** - Automatically detects JSON, Java/Spring, and common log formats
- **🌏 Full Unicode Support** - Handles Khmer, Chinese, Japanese, and all Unicode characters
- **🧵 Thread Analysis** - Filter and analyze by thread names (http-nio, SimpleAsyncTaskExecutor, etc.)
- **🎯 Advanced Filtering** - Filter by log level, HTTP method, status code, thread, service, or custom search
- **📝 Log Editing** - Edit individual log entries interactively
- **📈 Statistics Summary** - View comprehensive log statistics at a glance
- **💾 Export Functionality** - Export filtered logs to new files
- **🎨 Syntax Highlighting** - Beautiful JSON and code highlighting
- **⚡ Fast Performance** - Efficiently handles large log files (tested with 3MB+ files)
- **🏗️ Professional Architecture** - Clean, modular code structure for easy maintenance
- **💻 Standalone Executable** - Drag & drop support, no Python installation required

## 🆕 What's New in v1.0.0

- ✅ Full Java/Spring Boot application log support
- ✅ Custom error code mapping (RSLT_CD[719] → HTTP 404)
- ✅ Service/Controller detection and filtering
- ✅ Thread-based analysis and filtering
- ✅ Complete Unicode text support (Asian languages)
- ✅ Standalone executable with drag & drop
- ✅ Message colorization based on log level
- ✅ Enhanced parsing for START/STOP operations
- ✅ Bug fixes for large file handling

## 🚀 Quick Start

### Method 1: Python Installation

```bash
# Clone the repository
git clone https://github.com/setyuth/api-log-viewer.git
cd api-log-viewer

# Install dependencies
pip install -r requirements.txt

# Run with example
python main.py examples/sample_api_format.log
```

### Method 2: Standalone Executable

**No Python Required!**

1. Download the latest release from [Releases](https://github.com/setyuth/api-log-viewer/releases)
2. Extract the ZIP file
3. **Windows**: Drag & drop your log file onto `LogViewer.exe`
4. **Linux/macOS**: `./LogViewer your_log_file.log`

### Method 3: Using Quick Start Script

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh examples/sample_api_format.log
```

**Windows:**
```cmd
run.bat examples\sample_api_format.log
```

## 📖 Supported Log Formats

### Java/Spring Application Logs
```
08:26:53.594 [SimpleAsyncTaskExecutor-7444] INFO  k.g.t.g.util.PushNotiHttpV1Service :: Sending 'POST' request to URL : https://api.example.com
08:27:34.001 [http-nio-28080-exec-10] ERROR kh.gov.tax.gdtict.util.ApiLogCls :: RSLT_CD[719]
08:27:34.001 [http-nio-28080-exec-10] ERROR kh.gov.tax.gdtict.util.ApiLogCls :: RSLT_MSG[DATA NOT FOUND.]
```

### JSON Logs
```json
{"timestamp": "2024-01-20T10:30:45Z", "level": "INFO", "method": "GET", "path": "/api/users", "status": 200}
```

### Common Text Formats
```
2024-01-20 10:30:45 INFO GET /api/users 200 45ms
```

### Apache/Nginx Style
```
192.168.1.1 - - [20/Jan/2024:10:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234
```

## 🎮 Commands

### Viewing Commands

| Command | Description | Example |
|---------|-------------|---------|
| `summary` | Show log statistics summary | `summary` |
| `list [limit]` | List log entries (default: 50) | `list 100` |
| `view <line>` | View detailed entry information | `view 42` |
| `stats` | Alias for summary | `stats` |

### Filtering Commands

| Command | Description | Example |
|---------|-------------|---------|
| `filter level <LEVEL>` | Filter by log level | `filter level ERROR` |
| `filter method <METHOD>` | Filter by HTTP method | `filter method POST` |
| `filter status <CODE>` | Filter by status code | `filter status 404` |
| `filter thread <name>` | Filter by thread name | `filter thread http-nio` |
| `filter service <name>` | Filter by service/controller | `filter service BackendInvoiceCntr` |
| `filter search <TEXT>` | Search for text (Unicode supported) | `filter search ážœáž·ážšáŸˆ` |
| `clear` | Clear all filters | `clear` |

### Editing & Export Commands

| Command | Description | Example |
|---------|-------------|---------|
| `edit <line>` | Edit a specific log entry | `edit 42` |
| `save [path]` | Save changes to file | `save output.log` |
| `export <path>` | Export filtered entries | `export errors.log` |

### Other Commands

| Command | Description |
|---------|-------------|
| `help` | Show help message |
| `quit`, `exit`, `q` | Exit the application |

## 💡 Usage Examples

### Example 1: Find All Errors
```bash
python main.py examples/sample_api_format.log

› filter level ERROR
› list
› export errors_only.log
```

### Example 2: Analyze Specific Thread
```bash
› filter thread http-nio-28080
› summary
```

### Example 3: Find DATA NOT FOUND Errors
```bash
› filter search "DATA NOT FOUND"
› list
```

### Example 4: Analyze Specific Service
```bash
› filter service BackendInvoiceCntr
› filter level ERROR
› list 20
```

### Example 5: Search Unicode Text
```bash
› filter search ážœáž·ážšáŸˆ
› view 10
```

## 🏗️ Project Structure

```
api-log-viewer/
├── main.py                    # Application entry point
├── logviewer_standalone.py    # Single-file standalone version
├── requirements.txt           # Python dependencies
├── setup.py                  # Package installation
├── README.md                 # This file
├── LICENSE                   # MIT License
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
│
├── src/                      # Source code
│   ├── __init__.py
│   ├── config.py            # Configuration
│   ├── log_viewer.py        # Main viewer class
│   │
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   └── log_entry.py    # Enhanced LogEntry with Java/Spring support
│   │
│   └── utils/               # Utilities
│       ├── __init__.py
│       └── helpers.py       # Helper functions
│
├── examples/                 # Example log files
│   ├── sample_json.log      # JSON format
│   ├── sample_text.log      # Text format
│   └── sample_api_format.log # Java/Spring format
│
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_log_entry.py
│   └── test_log_viewer.py
│
├── docs/                    # Documentation
│   ├── QUICKSTART.md
│   ├── USAGE_GUIDE.md
│   └── BUILD_EXECUTABLE.md
│
└── build/                   # Build scripts
    ├── build_windows.bat
    └── build_scripts.sh
```

## 🔧 Key Features for Java/Spring Logs

### Thread Analysis
Automatically extracts and displays thread information:
- HTTP request threads: `http-nio-28080-exec-4`
- Async task executors: `SimpleAsyncTaskExecutor-7444`
- Custom thread pools

### Service Detection
Automatically identifies services and controllers:
- `BackendInvoiceCntr`
- `InvoiceDataEntryCntr`
- `PushNotiHttpV1Service`

### Custom Error Code Mapping
Maps application-specific codes to HTTP equivalents:
- `RSLT_CD[719]` → HTTP 404 (DATA NOT FOUND)
- Maintains original code in detailed view

### Unicode Text Support
Full support for all Unicode characters including:
- Khmer: ážœáž·ážšáŸˆ áž"áŸŠáž»áž"ážáž¶áŸ† áž¢áŸáž…áž"áŸ'ážšáŸážŸ
- Chinese, Japanese, Korean, Thai, Arabic, etc.
- Emoji and special characters

## 📊 Display Format

The enhanced table view shows:
- **#** - Line number
- **Time** - Millisecond precision timestamp
- **Level** - Color-coded log levels
- **Thread** - Thread name (truncated if needed)
- **Service** - Controller/service name
- **Method** - HTTP method
- **Endpoint** - API endpoint
- **Status** - HTTP status code (color-coded)
- **Message** - Formatted message (color-coded by level)

## 🔨 Building Standalone Executable

### Prerequisites
```bash
pip install pyinstaller
```

### Build Commands

**Windows:**
```cmd
pyinstaller --onefile --console --name="LogViewer" logviewer_standalone.py
```

**Linux/macOS:**
```bash
pyinstaller --onefile --console --name="LogViewer" logviewer_standalone.py
```

**Result:** `dist/LogViewer.exe` or `dist/LogViewer` (~15-18 MB)

See [BUILD_EXECUTABLE.md](docs/BUILD_EXECUTABLE.md) for detailed instructions.

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test
pytest tests/test_log_entry.py -v
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Quick Contribution Guide

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📋 Roadmap

- [x] Java/Spring log support
- [x] Unicode text handling
- [x] Thread-based filtering
- [x] Standalone executable
- [ ] Real-time log tailing
- [ ] Multi-file support
- [ ] Web-based UI
- [ ] Plugin system for custom parsers
- [ ] Log correlation and tracing
- [ ] Docker container version

## 🐛 Known Issues

- Very large files (>100MB) may take time to load
- Some exotic timestamp formats may not be detected
- Binary log files are not supported

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) by Textualize
- Inspired by the needs of developers working with complex application logs
- Special thanks to all contributors

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/setyuth/api-log-viewer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/setyuth/api-log-viewer/discussions)
- **Documentation**: [Wiki](https://github.com/setyuth/api-log-viewer/wiki)

## 🌟 Star History

If you find this tool useful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/api-log-viewer&type=Date)](https://star-history.com/#yourusername/api-log-viewer&Date)

## 📊 Statistics

- **Lines of Code**: ~2,000
- **Test Coverage**: 85%+
- **Supported Log Formats**: 4+
- **Supported Languages**: 100+ (Unicode)
- **Downloads**: Check [releases](https://github.com/setyuth/api-log-viewer/releases)

---

**Made with ❤️ for developers analyzing complex application logs**

**Version 1.0.0** - Released January 2026