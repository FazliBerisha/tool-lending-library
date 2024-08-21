# Tool Lending Library

A community-driven platform for lending and borrowing tools.

## Project Structure
- `frontend/`: Contains the React frontend application
- `backend/`: Contains the FastAPI backend application

## Setup

### Backend
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `uvicorn app.main:app --reload`

### Frontend
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm start`

## Contributing
Please create a new branch for each feature and submit a pull request for review.

## License
[MIT License](https://opensource.org/licenses/MIT)