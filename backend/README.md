# Spokesperson AI

## Getting Started
Follow the steps below to set up and run the project.

### Prerequisites
- Python 3.12+
- Node.js 16+
- OpenAI API Key

## Project Structure
```
Spokesperson/
├── venv/                  # Virtual environment directory (not tracked in version control)
├── .env.example           # Example environment configuration
├── .gitignore             # Git ignore file
├── README.md              # Existing README file
├── requirements.txt       # Python dependencies
├── Makefile               # Makefile for common commands
├── app.py                 # Main application script
├── config.py              # Centralized configuration management
├── logs/                  # Directory for storing application logs
│   └── app.log
├── tests/                 # Test cases for the application
│   ├── __init__.py
│   └── test_app.py        # Example test case
├── templates/             # Flask HTML templates
│   └── index.html
├── static/                # Static files (CSS, JavaScript)
├── docs/                  # Additional documentation files
├── src/                   # Source files for additional modules
│   └── ai_module.py       # AI integration logic
└── setup.sh               # Setup script to automate environment configuration
```


### Installation
1. Clone the repository: 
   ```
   git clone https://github.com/tyler-pritchard/spokesperson.git
   ```
2. Navigate to the project directory:
   ```
   cd spokesperson
   ```
3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
- On macOS/Linux:
  ```
  source venv/bin/activate
  ```
- On Windows:
  ```
  venv\Scripts\activate
  ```
5. Install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Create a `.env` file from the provided `.env.example` and add your OpenAI API Key.

  .env.example:
  ```
  Example .env file for Spokesperson App
  Copy this code to .env and replace the placeholder values
  
  OPENAI_API_KEY=your_openai_api_key_here
  FLASK_ENV=development
  SECRET_KEY=your_flask_secret_key
  ```


7. Run the application:
  ```
  python app.py
  ```


### Running Tests
To run the test suite, execute the following command:
  ```
  pytest
  ```

### Additional Notes
For more detailed documentation, refer to the `docs` directory.
