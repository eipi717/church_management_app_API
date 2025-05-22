# Church Management App

## Overview

This project is a FastAPI-based booking system that provides endpoints for managing announcements, bookings, rooms, and user authentication. It follows a modular structure using Data Transfer Objects (DTOs), services, models, and routes.

## Features

- User authentication (login, password change, user creation)
- Booking management (create, cancel, get bookings by user or room)
- Announcement management (create, update, delete, get announcements)
- Room management (get rooms, deactivate rooms)
- Logging and error handling

## Testing

### ✅ Unit Tests

All core backend functions (services, helpers, DTOs, models) are covered by unit tests using `pytest`. This includes:
- Service logic for announcements, bookings, rooms, and users
- DTO validation and transformation
- Helper functions like password hashing and data updates
- Model method coverage such as `transform_to_dict()`

Logs are enabled to trace behavior and outputs during test execution.

To run unit tests:
```bash
pytest --log-cli-level=INFO tests/unit/
```

Ideally you may see:
```bash
==================== 51 passed in 0.24s ====================
```

### 🔄 Integration Tests (Coming Soon)
Integration tests will validate the interaction between FastAPI routes, service layers, and the database.

These will run against a dedicated **MySQL** test database with the same schema and mock data for realistic validation.

### 🧪 End-to-End (E2E) Tests (Coming Soon)
E2E tests will simulate real user flows by interacting with the API and frontend (if available).

These tests will be automated using **Selenium**, verifying complete workflows from request to response.
