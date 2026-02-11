.PHONY: help setup run test format lint clean

help:
	@echo "CricSim - Cricket League Simulator"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup      - Install development dependencies"
	@echo "  make run        - Run the simulator"
	@echo "  make test       - Run tests"
	@echo "  make format     - Format code with black"
	@echo "  make lint       - Check code style with flake8"
	@echo "  make clean      - Remove generated files and cache"

setup:
	python -m venv venv
	pip install -e ".[dev,rich]"
	@echo "✅ Development environment ready!"

run:
	python main.py

test:
	pytest -v

format:
	black *.py

lint:
	flake8 *.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf build dist *.egg-info
	@echo "✅ Cleaned up!"
