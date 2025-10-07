.PHONY: help install install-dev build clean test lint format

help:
	@echo "Linear CLI - Makefile commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install the package"
	@echo "  make install-dev  - Install in development mode"
	@echo "  make build        - Build wheel package"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make test         - Run tests (when available)"
	@echo "  make lint         - Run linting"
	@echo "  make format       - Format code"

install:
	pip install .

install-dev:
	pip install -e .

build:
	pip install build wheel
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete

test:
	@echo "Tests not yet implemented"
	# pytest tests/

lint:
	@echo "Running linting..."
	@command -v pylint >/dev/null 2>&1 || { echo "Installing pylint..."; pip install pylint; }
	pylint src/

format:
	@echo "Formatting code..."
	@command -v black >/dev/null 2>&1 || { echo "Installing black..."; pip install black; }
	black src/
