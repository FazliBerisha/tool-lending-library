# README.md for SQL-Based Backend   

backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point of the application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection management
│   │
│   ├── models/              # Data models and database schemas
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic and database operations
│   ├── core/                # Core functionalities (security, dependencies)
│   └── utils/               # Utility functions
│
├── sql/                     # SQL scripts for database setup and queries
│   ├── init.sql             # Database initialization script
│   ├── users.sql            # User-related queries
│   ├── tools.sql            # Tool-related queries
│   └── reservations.sql     # Reservation-related queries
│
└── requirements.txt         # Project dependencies
```

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
- Add a rating and review system for tools and users
- Implement notifications system for reservations and due dates

## Contributors

- [Fazli]
- [Farrukh]
- [Anna]
