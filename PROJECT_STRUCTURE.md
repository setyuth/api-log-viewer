# 📋 Project Structure Documentation

Complete overview of the API Log Viewer project architecture and organization.

## 📁 Directory Structure

```
api-log-viewer/
│
├── 📄 main.py                    # Application entry point - CLI interface
├── 📄 requirements.txt           # Python dependencies (rich>=13.7.0)
├── 📄 setup.py                   # Package installation configuration
├── 📄 Makefile                   # Development task automation
├── 📄 run.sh                     # Quick start script (Linux/macOS)
├── 📄 run.bat                    # Quick start script (Windows)
│
├── 📘 README.md                  # Main project documentation
├── 📘 QUICKSTART.md              # Quick start guide
├── 📘 CONTRIBUTING.md            # Contribution guidelines
├── 📘 LICENSE                    # MIT License
├── 📘 PROJECT_STRUCTURE.md       # This file
│
├── 🔧 .gitignore                 # Git ignore rules
│
├── 📦 src/                       # Source code package
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration and settings
│   ├── log_viewer.py            # Main LogViewer class
│   │
│   ├── 📦 models/               # Data models
│   │   ├── __init__.py
│   │   └── log_entry.py         # LogEntry model - parsing & data
│   │
│   └── 📦 utils/                # Utility functions
│       ├── __init__.py
│       └── helpers.py           # Helper functions
│
├── 📂 examples/                  # Example log files
│   ├── sample_json.log          # JSON format examples
│   └── sample_text.log          # Text format examples
│
└── 🧪 tests/                     # Test suite
    ├── __init__.py
    ├── conftest.py              # Pytest configuration
    ├── test_log_entry.py        # LogEntry model tests
    └── test_log_viewer.py       # LogViewer class tests
```

## 📚 File Descriptions

### Core Application Files

#### `main.py`
**Purpose**: Application entry point and CLI interface  
**Responsibilities**:
- Command-line argument parsing
- Interactive command loop
- User input handling
- Command routing
- Application lifecycle management

**Key Functions**:
- `main()` - Entry point, initializes viewer and command loop
- Command handlers for: filter, view, edit, export, etc.

#### `src/log_viewer.py`
**Purpose**: Main application logic  
**Responsibilities**:
- File loading and parsing
- Log entry management
- Filtering and searching
- Display formatting
- Export functionality
- Edit and save operations

**Key Methods**:
- `load()` - Load and parse log file
- `display_summary()` - Show statistics
- `display_entries()` - Render log table
- `filter_logs()` - Apply filters
- `export_filtered()` - Export to file
- `edit_entry()` - Modify log entries
- `save()` - Save changes

### Models

#### `src/models/log_entry.py`
**Purpose**: Log entry data model and parser  
**Responsibilities**:
- Parse raw log lines
- Extract structured data
- Support multiple log formats
- Provide data accessors
- Handle color coding

**Key Methods**:
- `_parse()` - Main parsing dispatcher
- `_parse_common_format()` - Text log parsing
- `_extract_from_json()` - JSON log parsing
- `_parse_timestamp()` - Timestamp parsing
- `get_level_color()` - Log level colors
- `get_status_color()` - Status code colors

**Attributes**:
- `timestamp` - Parsed datetime
- `level` - Log level (INFO, ERROR, etc.)
- `method` - HTTP method
- `endpoint` - API endpoint
- `status_code` - HTTP status
- `response_time` - Request duration
- `message` - Log message
- `json_data` - Original JSON data

### Configuration

#### `src/config.py`
**Purpose**: Centralized configuration  
**Contains**:
- Display settings (limits, lengths)
- Color schemes
- Regex patterns
- Timestamp formats
- JSON field mappings

### Utilities

#### `src/utils/helpers.py`
**Purpose**: Reusable utility functions  
**Functions**:
- `show_help()` - Display help text
- `format_file_size()` - Human-readable sizes
- `truncate_text()` - Text truncation

### Examples

#### `examples/sample_json.log`
- 25 JSON-formatted log entries
- Various log levels and HTTP methods
- Includes errors, warnings, info
- Demonstrates all parseable fields

#### `examples/sample_text.log`
- 40+ text-formatted log entries
- Multiple text formats
- Apache/Nginx style logs
- Mixed timestamp formats

### Tests

#### `tests/test_log_entry.py`
**Tests for LogEntry model**:
- JSON parsing
- Text parsing
- Timestamp handling
- Color coding
- Edge cases

#### `tests/test_log_viewer.py`
**Tests for LogViewer class**:
- File loading
- Filtering (level, method, status)
- Export functionality
- Edit operations

#### `tests/conftest.py`
- Pytest fixtures
- Test data
- Configuration

### Documentation

#### `README.md`
- Project overview
- Features list
- Installation guide
- Command reference
- Usage examples
- Architecture overview

#### `QUICKSTART.md`
- 5-minute setup guide
- Installation methods
- First steps
- Common use cases
- Troubleshooting

#### `CONTRIBUTING.md`
- Contribution guidelines
- Development setup
- Coding standards
- Testing guidelines
- Git workflow

### Build & Run Scripts

#### `setup.py`
- Package metadata
- Dependencies
- Entry points
- Installation configuration

#### `Makefile`
- Development tasks
- Testing commands
- Linting and formatting
- Build automation

#### `run.sh` / `run.bat`
- Quick start scripts
- Dependency installation
- Virtual environment setup
- Application launch

## 🔄 Data Flow

```
1. User runs: python main.py logfile.log
   ↓
2. main.py creates LogViewer instance
   ↓
3. LogViewer.load() reads file
   ↓
4. For each line: create LogEntry
   ↓
5. LogEntry._parse() extracts data
   ↓
6. Data stored in viewer.entries[]
   ↓
7. User enters commands
   ↓
8. Commands modify viewer.filtered_entries[]
   ↓
9. Display methods render to terminal
```

## 🎨 Design Patterns

### 1. **Model-View Separation**
- **Model**: `LogEntry` - data and parsing
- **View**: `LogViewer` - display and interaction
- **Controller**: `main.py` - user commands

### 2. **Single Responsibility**
- Each module has one clear purpose
- LogEntry: parse and store
- LogViewer: manage and display
- helpers: reusable utilities

### 3. **Configuration-Driven**
- Settings in `config.py`
- Easy to modify behavior
- No hardcoded values

### 4. **Extensible Architecture**
- Easy to add parsers
- Simple to add commands
- Pluggable filters

## 🔌 Extension Points

### Adding New Features

#### New Log Format
**File**: `src/models/log_entry.py`
```python
def _parse_custom_format(self):
    # Add parsing logic
    pass
```

#### New Command
**File**: `main.py`
```python
elif cmd == 'newcommand':
    # Add command handler
    pass
```

#### New Filter Type
**File**: `src/log_viewer.py`
```python
def filter_logs(self, custom_field=None):
    if custom_field:
        # Add filter logic
        pass
```

#### New Configuration
**File**: `src/config.py`
```python
NEW_SETTING = 'value'
```

## 📊 Dependencies

### Production
- **rich** (>=13.7.0): Terminal UI library
  - Tables, colors, syntax highlighting
  - Progress bars, panels

### Development (Optional)
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatter
- **flake8**: Linter
- **mypy**: Type checker

## 🚀 Build & Release Process

### Development
```bash
make setup      # Install all dependencies
make test       # Run tests
make lint       # Check code quality
make format     # Format code
```

### Release
```bash
make clean      # Clean artifacts
make build      # Build package
# Upload to PyPI
```

## 🎯 Future Enhancements

### Planned Features
1. Real-time log tailing
2. Multi-file support
3. Custom format config files
4. Regex search
5. Web UI
6. Plugin system
7. Log correlation
8. Charts and graphs

### Architecture Improvements
1. Async log loading
2. Caching layer
3. Database backend option
4. Stream processing
5. Performance optimization

## 📝 Code Statistics

- **Total Files**: 20+
- **Lines of Code**: ~1,500
- **Test Coverage**: Target 80%+
- **Documentation**: Comprehensive

## 🔒 Security Considerations

- File path validation
- Input sanitization
- No external network calls
- Safe file operations
- Error handling

---

**This structure provides a solid foundation for a professional, maintainable log viewer tool.**