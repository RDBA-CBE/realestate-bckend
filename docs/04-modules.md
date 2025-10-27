# Main Modules

[Previous: Architecture & Folder Structure](./03-architecture.md) | [Next: API Endpoints](./05-api.md)

---

## AuthApp
Handles user authentication, registration, and profile management.
- **models/**: Custom user, agent, buyer, seller profiles
- **serializers/**: Data validation and transformation
- **viewsets/**: API logic for user actions
- **filters/**: Query filtering for user lists

## Common
Shared utilities and models used across apps.
- **models.py**: Common data models
- **serializers.py**: Shared serializers
- **viewset.py**: Shared viewsets

## Property
Manages property listings and related data.
- **models/**: Property, address, types
- **serializers/**: Property data serialization
- **viewsets/**: CRUD operations for properties

## Media
Handles media uploads and storage.
- **media/**: Images, videos, floor plans
- **static/**: Static assets

---

[Previous: Architecture & Folder Structure](./03-architecture.md) | [Next: API Endpoints](./05-api.md)
