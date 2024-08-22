# Tool Lending Library - Frontend

This is the frontend application for the Tool Lending Library project, a platform that allows users to lend and borrow tools within a community.

## Technologies Used

- React.js
- React Router for navigation
- Axios for API requests
- Material-UI for styling

## Prerequisites

- Node.js (v14.0.0 or later)
- npm (v6.0.0 or later)

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/FazliBerisha/tool-lending-library.git
   cd tool-lending-library/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables:
   - Create a `.env` file in the root of the frontend directory
   - Add the following line (adjust the URL if your backend is hosted elsewhere):
     ```
     REACT_APP_API_URL=http://localhost:8000
     ```

4. Start the development server:
   ```
   npm start
   ```

The application should now be running on [http://localhost:3000](http://localhost:3000).

## Available Scripts

- `npm start`: Runs the app in development mode
- `npm test`: Launches the test runner
- `npm run build`: Builds the app for production
- `npm run eject`: Ejects from Create React App (use with caution)

## Features

- User authentication (login/register)
- Browse and search tools
- Tool reservation system
- User profile management
- Admin dashboard for tool management and reporting

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request