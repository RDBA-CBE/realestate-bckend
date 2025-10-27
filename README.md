# Real Estate API

This is a Django-based REST API for a real estate platform. It provides functionalities for user authentication, profile management, and other real estate-related operations.

## Project Structure

The project is organized into two main Django apps:

-   `authapp`: Handles user authentication, registration, and profile management.
-   `common`: Contains common models and utilities shared across the project.

## Features

-   **User Authentication:**
    -   User registration with email and password.
    -   JWT-based authentication for secure API access.
    -   Login and logout functionality.
-   **User Profiles:**
    -   Different user roles: Admin, Agent, Buyer, and Seller.
    -   Separate profile models for each user role to store relevant information.
-   **API Endpoints:**
    -   `/api/auth/register/`: User registration.
    -   `/api/auth/login/`: User login.
    -   `/api/auth/profile/`: View and update user profile.
    -   `/api/auth/admin/users/`: Admin access to manage users.

## Getting Started

### Prerequisites

-   Python 3.x
-   Django
-   Django REST Framework
-   Simple JWT

### Installation

1.  **Clone the repository:**
    pip install -r requirements.txt
    ```

3.  **Run the database migrations:**
    python manage.py migrate
    ```
4.  **Start the development server:**

    ```bash
    ```


## API Documentation

For detailed information about the API endpoints, please refer to the Postman collection or use the browsable API provided by Django REST Framework.

## User Roles

The platform supports the following user roles:

-   **Admin:** Has full access to the system and can manage all users and data.
-   **Agent:** A real estate agent who can list and manage properties.
-   **Buyer:** A user who is looking to buy or rent a property.
-   **Seller:** A user who wants to sell a property.

Each user role has a specific profile with fields tailored to their needs.
