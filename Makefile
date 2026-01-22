.PHONY: help install dev test clean run lint format

# Default target
help:
	@echo "API Log Viewer - Available Commands"
	@echo "===================================="
	@echo "make install    - Install dependencies"
	@echo "make dev        - Install development dependencies"
	@echo "make run        - Run with example log file"
	@echo "make test       - Run tests"
	@echo "make lint       - Run linters"
	@echo "make format     - Format code with black"
	@echo "make clean      - Clean build artifacts"
	@echo "make setup      - Complete setup (install + dev)"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
dev:
	pip install pytest pytest-cov black flake8 mypy

# Complete setup
setup: install dev
	@echo "Setup complete!"

# Run with example log file
run:
	python main.py examples/sample_json.log

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-cov:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

# Run linters
lint:
	flake8 src/ main.py --max-line-length=100
	mypy src/ main.py --ignore-missing-imports

# Format code
format:
	black src/ main.py tests/

# Clean build artifacts
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/models/__pycache__
	rm -rf src/utils/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Build package
build:
	python setup.py sdist bdist_wheel

# Install package in development mode
install-dev:
	pip install -e .