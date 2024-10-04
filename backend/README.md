# Spokesperson AI Backend

Spokesperson AI is a backend application designed to facilitate interactive AI-generated dating scenarios through a combination of OpenAI's NLP models and Flask-SocketIO for real-time communication. This application manages user sessions, profile generation, and guided conversations, supporting a range of API and WebSocket interactions to enhance user experience.

##  Table of Contents
- [Spokesperson AI Backend](#spokesperson-ai-backend)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [Project Architecture](#project-architecture)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
    - [Running in Production](#running-in-production)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Getting Started
To set up and run the application, follow the instructions below. This guide assumes basic familiarity with Python, Flask, and relational databases.

## Project Architecture
```
Spokesperson/
├── app/
│   ├── __init__.py              # Application initialization
│   ├── main.py                  # Main entry point for running the Flask app
│   ├── models.py                # SQLAlchemy models for database interaction
│   ├── routes.py                # API route handlers for RESTful endpoints
│   ├── services.py              # Service layer for business logic
│   ├── socketio_handlers.py     # Handlers for WebSocket events
│   ├── utils.py                 # Utility functions for the application
├── config/
│   └── config.py                # Configuration settings for different environments
├── scripts/
│   ├── list_engines.py          # Script for listing OpenAI models and engines
│   ├── populate_data.py         # Script for populating database with test data
│   └── setup.sh                 # Environment setup script
├── tests/
│   ├── db_tests.py              # Unit tests for database interactions
│   └── test_openai.py           # Unit tests for OpenAI service
├── data/                        # Directory for storing dataset files
├── instance/
│   └── spokesperson.db          # SQLite database for development and testing
├── logs/
│   └── app.log                  # Log files for tracking application events
├── static/                      # Static assets (CSS, JavaScript, images)
├── templates/                   # HTML templates for rendering dynamic content
├── .env.example                 # Example environment variables
├── Makefile                     # Makefile for common commands and automation
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
└── flask_session/               # Directory for Flask session data
```

## Features

- User Profile Management: Create, update, and manage AI-generated user profiles.
- Real-Time Communication: Interactive WebSocket-based conversations with dynamic AI responses.
- Session Management: Persistent sessions using Flask-Session and SQLite.
- AI Integration: Supports OpenAI's GPT models for generating context-aware responses.
- API and WebSocket Support: RESTful API and WebSocket endpoints for various interactions.
- Logging & Monitoring: Centralized logging for error tracking and application health.
- Database Interaction: SQLAlchemy ORM for data handling.

## Prerequisites
Ensure that the following software is installed:

- Python 3.12+
- Node.js 16+ (for frontend or API integrations)
- OpenAI API Key

## Installation
1. Clone the Repository:
   ```
   git clone https://github.com/tyler-pritchard/spokesperson.git
   ```
2. Navigate to the project directory:
   ```
   cd spokesperson
   ```
3. Create and Activate a Virtual Environment:
   - On macOS/Linux: 
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
   - On Windows:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Install Frontend Dependencies: Navigate to the frontend directory (if applicable) and install the necessary Node.js packages:
   ```
   npm install
   ```
## Configuration

1. Environment Variables: Create a ```.env``` file from the provided ```.env.example``` file and configure the required variables:
   ```
   cp .env.example .env
   ```
  Example ```.env``` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   FLASK_ENV=development
   SECRET_KEY=your_flask_secret_key
   ```
2. Database Setup: By default, the application uses an SQLite database (```spokesperson.db```). To populate the database with initial data, run:
   ```
   python scripts/populate_data.py
   ```
3. Logging Configuration: Adjust logging levels and log file paths in ```config/config.py``` as needed.

## Running the Application
Start the Flask development server:
   ```
   python app/main.py
   ```
Or use the Makefile for additional commands:
   ```
   make run
   ```
### Running in Production
For production, consider using ```gunicorn``` or another WSGI server. Example:
   ```
   gunicorn --bind 0.0.0.0:5000 app.main:app
   ```

## Testing
Unit tests are provided for core functionality, including database interactions and OpenAI integration. To run the test suite:
   ```
   pytest
   ```
Test-specific configurations can be adjusted in the tests directory.

## Contributing
To contribute, follow these steps:

Fork the repository.
Create a new branch (```git checkout -b feature-branch```).
Make your changes and commit them (```git commit -m 'Add new feature'```).
Push to the branch (```git push origin feature-branch```).
Open a pull request.
For detailed contribution guidelines, see the ```CONTRIBUTING.md``` (if applicable).

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.