# Makefile for Spokesperson Application

# Create and set up environment
setup:
	@bash setup.sh

# Run the application
run:
	@python app.py

# Run tests
test:
	@pytest tests/

# Install dependencies
install:
	@pip install -r requirements.txt

# Clean build files and logs
clean:
	@rm -rf logs/venv
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
