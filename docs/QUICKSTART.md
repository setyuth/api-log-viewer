# 🚀 Quick Start Guide

Get started with API Log Viewer in 5 minutes!

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## Installation Methods

### Method 1: Quick Start Script (Recommended)

#### Linux/macOS
```bash
# Clone the repository
git clone https://github.com/setyuth/api-log-viewer.git
cd api-log-viewer

# Make script executable
chmod +x run.sh

# Run with example file
./run.sh

# Or run with your own log file
./run.sh /path/to/your/logfile.log
```

#### Windows
```batch
# Clone the repository
git clone https://github.com/setyuth/api-log-viewer.git
cd api-log-viewer

# Run with example file
run.bat

# Or run with your own log file
run.bat C:\path\to\your\logfile.log
```

### Method 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/setyuth/api-log-viewer.git
cd api-log-viewer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py examples/sample_json.log
```

### Method 3: Using Make (Linux/macOS)

```bash
# Complete setup
make setup

# Run with example file
make run

# Or run directly
python main.py examples/sample_json.log
```

### Method 4: Install as Package

```bash
# Install in development mode
pip install -e .

# Run from anywhere
logviewer examples/sample_json.log
```

## First Steps

Once the application is running, try these commands:

```
# View summary statistics
› summary

# List first 20 log entries
› list 20

# Filter by error level
› filter level ERROR

# View detailed information about entry #5
› view 5

# Search for specific text
› filter search timeout

# Export filtered results
› export my_errors.log

# Get help
› help

# Exit
› quit
```

## Common Use Cases

### 1. Finding Errors Quickly
```
› filter level ERROR
› list
› view 1
```

### 2. Analyzing Failed API Calls
```
› filter status 500
› summary
› export server_errors.log
```

### 3. Debugging Specific Endpoint
```
› filter search /api/payment
› list
› view 10
```

### 4. Finding Slow Requests
```
› filter search timeout
› list
› export timeouts.log
```

## Working with Your Own Logs

### Supported Formats

The tool automatically detects and parses:

1. **JSON logs**
```json
{"timestamp": "2024-01-20T10:30:45Z", "level": "INFO", "method": "GET", "path": "/api/users", "status": 200}
```

2. **Text logs**
```
2024-01-20 10:30:45 INFO GET /api/users 200 45ms
```

3. **Apache/Nginx logs**
```
192.168.1.1 - - [20/Jan/2024:10:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234
```

### Tips for Best Results

- **JSON logs**: Ensure each line is valid JSON
- **Text logs**: Include timestamp, level, and method for best parsing
- **Large files**: The tool handles large files well, but may take a moment to load
- **Mixed formats**: You can have different formats in the same file

## Troubleshooting

### Issue: "File not found"
**Solution**: Make sure the file path is correct
```bash
# Use absolute path
python main.py /full/path/to/logfile.log

# Or relative path
python main.py ./logs/api.log
```

### Issue: "Command not found"
**Solution**: Make sure you're in the project directory
```bash
cd api-log-viewer
python main.py examples/sample_json.log
```

### Issue: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Virtual environment not activating
**Solution**: 
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate.bat
```

## Next Steps

1. **Read the full documentation**: Check [README.md](../README.md)
2. **Try the examples**: Explore files in the `examples/` directory
3. **Learn all commands**: Type `help` in the application
4. **Contribute**: See [CONTRIBUTING.md](../CONTRIBUTING.md)

## Getting Help

- Type `help` inside the application
- Check [README.md](../README.md) for detailed documentation
- Open an issue on GitHub
- Read [CONTRIBUTING.md](../CONTRIBUTING.md) for development help

## Pro Tips

1. **Combine filters**: You can apply multiple filters (though currently you need to do one at a time)
2. **Export often**: Save filtered results for later analysis
3. **Use list limits**: `list 100` shows more entries at once
4. **Learn patterns**: Common issues often have similar log patterns
5. **Keep backups**: The tool can edit logs - save originals!

---

**Happy log viewing! 📊**