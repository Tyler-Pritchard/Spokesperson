# Spokesperson - Mobile Client

## Table of Contents
- [Spokesperson - Mobile Client](#spokesperson---mobile-client)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Features](#features)
  - [Project Architecture](#project-architecture)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Project Details](#project-details)
    - [Navigation](#navigation)
    - [Dependencies](#dependencies)
    - [Backend Integration](#backend-integration)
  - [Development](#development)
    - [WebSocket Integration](#websocket-integration)
  - [Navigation Setup](#navigation-setup)
    - [Expo Configuration](#expo-configuration)
  - [Future Improvements](#future-improvements)
  - [License](#license)


## Overview

This repository contains the mobile client for the AI-powered dating application. The mobile app enables users to create virtual dating profiles ("Spokespersons"), interact with the profiles through a conversational interface, and receive AI-generated date summaries and results. The mobile frontend is built using React Native and Expo, and the backend services are written in Python and hosted in the /backend directory.

The mobile app is responsible for facilitating user interactions with the backend and rendering the UI for:

- Spokesperson creation.
- Date selection.
- Displaying AI-generated results.

### Features

- Spokesperson Creation: Users communicate with an AI to define the traits and personality of their spokesperson.
- Date Selection: After creating a spokesperson, users select various date scenarios.
- AI-Generated Results: Based on the interactions and selected dates, the AI generates a summary, which is displayed on the results page.

## Project Architecture
```
├── assets/                   # Images and other static assets.
├── screens/                  # All app screens (UI components).
│   ├── DateSelection.js      # Screen to select a date scenario.
│   ├── ResultsPage.js        # Screen that displays AI-generated date results.
│   └── SpokespersonCreation.js # Screen to interact with the AI and create a spokesperson.
├── App.js                    # Entry point of the app, integrates navigation.
├── app.json                  # Expo configuration for the app.
├── babel.config.js           # Babel configuration for Expo.
├── metro.config.cjs          # Metro bundler configuration for Expo.
├── navigation.js             # Navigation setup between different screens.
├── package.json              # Project dependencies and scripts.
└── yarn.lock                 # Dependency lock file.

```

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Node.js](https://nodejs.org/) (v16 or later)
- [Yarn](https://yarnpkg.com/) (or npm)
- [Expo CLI](https://expo.io)

### Installation

1. Clone the repository:
```
git clone https://github.com/tyler-pritchard/mobile-ai-dating-app.git
```

2. Navigate into the project directory:
```
cd mobile-ai-dating-app
```

3. Install the project dependencies:
```
yarn install
```

## Running the Application
To run the app on a local emulator or connected device, use the following commands:

- iOS:
```
yarn ios
```

- Android:
```
yarn android
```

- Web:
```
yarn web
```

## Project Details

### Navigation
The application uses React Navigation for screen management. The following screens are available:

- SpokespersonCreation: This screen allows users to interact with the AI using WebSockets to define their virtual spokesperson. WebSocket integration enables real-time communication between the app and the AI backend.
- DateSelection: After creating a spokesperson, users can choose date options, which will guide the AI in generating results.
- ResultsPage: Displays the AI-generated outcome of the date, summarizing the experience based on the selected options and conversations.

### Dependencies
Key dependencies for the mobile application are:

- React Native: Framework for building native apps using React.
- Expo: Development platform and framework for building and deploying React Native applications.
- React Navigation: Navigation management between screens.
- Socket.io Client: Enables real-time, bidirectional communication with the backend server using WebSockets.
  
Check the full list of dependencies in the ```package.json``` file.
```
{
  "dependencies": {
    "@react-navigation/native": "^6.1.18",
    "@react-navigation/stack": "^6.3.16",
    "expo": "~51.0.28",
    "react-native": "^0.75.3",
    "socket.io-client": "^4.8.0"
  }
}
```

### Backend Integration
This mobile app connects to a backend service built with Python, which handles the AI logic. The app communicates with the backend using WebSocket for real-time interactions. The backend service is hosted separately and must be running for full functionality.

## Development

### WebSocket Integration
The app uses ```socket.io-client``` to establish a WebSocket connection with the backend. In the SpokespersonCreation screen, the app sends messages to the AI backend and receives responses, which are displayed to the user in real-time.

The WebSocket is configured to reconnect on failure, with adjustable timeout settings:
```
const socket = io("http://10.0.0.50:5000", {
  transports: ["websocket"],
  reconnectionAttempts: 5,
  timeout: 20000,
  reconnectionDelayMax: 10000,
});
```

## Navigation Setup
The ```navigation.js``` file defines the main navigation flow between the different screens. It uses a stack navigator to allow users to transition between:

- SpokespersonCreation -> DateSelection -> ResultsPage

### Expo Configuration
The ```app.json``` file contains the configuration for Expo, including:

- App name and version
- Platform-specific icons
- Splash screen settings

Example configuration for Android:
```
{
  "expo": {
    "name": "mobile",
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      }
    }
  }
}
```

## Future Improvements
- Enhance AI responses: Further integrate NLP capabilities in the backend to provide richer conversations.
- User Authentication: Implement user login and profile management.
- Multiplayer functionality: Allow users to collaborate or compete in shared AI-generated experiences.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

