# Architecture & Folder Structure

[Previous: Project Setup & Installation](./02-setup.md) | [Next: Main Modules](./04-modules.md)

---

## Overview
The project follows a modular Django architecture. Each major feature is organized into its own app.

### Top-Level Structure
```
realestate-backend/
├── authapp/         # User authentication & profiles
├── common/          # Shared utilities & models
├── property/        # Property management
├── media/           # Media files (images, videos)
├── realestate/      # Django project settings & URLs
├── static/          # Static files
├── manage.py        # Django management script
├── requirments.txt  # Python dependencies
├── deploy.sh        # Deployment script
├── docker-compose.yml
├── README.md
```

### App Structure Example
```
authapp/
├── models/          # Data models
├── serializers/     # DRF serializers
├── viewsets/        # DRF viewsets
├── filters/         # Query filters
├── migrations/      # DB migrations
├── urls.py          # App URLs
```

---

[Previous: Project Setup & Installation](./02-setup.md) | [Next: Main Modules](./04-modules.md)
