# Tool Lending Library - Backend

The backend of our Tool Lending Library project is organized as follows:

The root directory contains the 'app' folder, which houses the main application code, a 'sql' folder for database-related scripts, and a 'requirements.txt' file listing all project dependencies.

Within the 'app' folder, you'll find several key files and subdirectories. The '__init__.py' file marks this as a Python package. 'main.py' serves as the entry point for our application. 'config.py' manages configuration settings, while 'database.py' handles database connection management.

The 'app' folder also contains several subdirectories, each with a specific purpose:
- 'models': Contains data models and database schemas.
- 'routers': Holds API route handlers.
- 'services': Manages business logic and database operations.
- 'core': Includes core functionalities like security and dependencies.
- 'utils': Houses utility functions.

## Design Decisions

1. **FastAPI Framework**: Chosen for its high performance, easy-to-use async capabilities, and automatic OpenAPI documentation.

2. **Direct SQL Usage**: Instead of an ORM, we're using SQL queries directly for more control over database operations and to leverage the full power of SQL.

3. **Modular Structure**: The project is organized into modules (models, routers, services) for better maintainability and scalability.

4. **SQL Scripts**: Separate SQL files for different entities to keep queries organized and easily maintainable.

5. **Separation of Concerns**:
   - `models/`: Data models and database schema definitions
   - `routers/`: API route handlers
   - `services/`: Business logic and database operations
   - `core/`: Core functionalities like security

6. **Configuration Management**: Using `config.py` for centralized configuration, supporting environment variables for flexibility across different deployment environments.

7. **Authentication**: JWT-based authentication implemented in `core/security.py` and `routers/auth.py`.

## API Endpoints

- `/users/`: User management
- `/tools/`: Tool catalog and management
- `/reservations/`: Reservation system
- `/auth/`: Authentication endpoints

For detailed API documentation, refer to the Swagger UI at `/docs` endpoint when the server is running.

## Development Workflow

1. Create new features in separate branches
2. Write unit tests for new features
3. Use `black` for code formatting
4. Run `pytest` for testing before committing changes
5. When adding new database operations, create corresponding SQL queries in the appropriate SQL file

## Future Improvements

- Implement more advanced search and filtering for tools using complex SQL queries
- Implement notifications system for reservations and due dates
