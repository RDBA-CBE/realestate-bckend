# Project Setup & Installation

[Previous: Introduction & Overview](./01-introduction.md) | [Next: Architecture & Folder Structure](./03-architecture.md)

---

## Prerequisites
- Python 3.10+
- pip
- Docker (optional, for containerized deployment)

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd realestate-backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirments.txt
   ```

3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

4. **Run the development server**
   ```bash
   python manage.py runserver
   ```

5. **(Optional) Run with Docker**
   ```bash
   docker-compose up --build
   ```

---

[Previous: Introduction & Overview](./01-introduction.md) | [Next: Architecture & Folder Structure](./03-architecture.md)
