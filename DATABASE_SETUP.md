# Database Setup

This project now uses SQLite instead of PostgreSQL for simplicity.

## Setup Instructions

1. **Initialize the database:**
   ```bash
   python init_sqlite.py
   ```

2. **Start the FastAPI server:**
   ```bash
   python -m uvicorn api:app --reload --port 8000
   ```

3. **Start the frontend:**
   ```bash
   cd tutor
   npm run dev
   ```

## Database File

The SQLite database is stored as `tutor.db` in the project root. This file will be created automatically when you run the initialization script.

## Schema

The database contains the same schema as the previous PostgreSQL setup:

- **lessons**: Stores lesson content and metadata
- **questions**: Stores questions associated with each lesson

## Migration from PostgreSQL

If you have existing data in PostgreSQL that you want to migrate, you'll need to:
1. Export the data from PostgreSQL
2. Transform UUID fields to strings
3. Import into the new SQLite database

For most use cases, starting fresh with the sample data is recommended.
