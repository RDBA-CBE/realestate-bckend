# Troubleshooting & FAQ

[Previous: Contribution Guide](./07-contributing.md)

---

## Common Issues

### 1. Migrations Not Applying
- Ensure the database is running and accessible.
- Run `python manage.py makemigrations` and `python manage.py migrate`.

### 2. Media Files Not Uploading
- Check `MEDIA_ROOT` and directory permissions.
- Verify file size limits in Django settings.

### 3. Docker Build Fails
- Ensure Docker is installed and running.
- Check for missing environment variables in `docker-compose.yml`.

## FAQ

**Q: How do I create a superuser?**
A: Run `python manage.py createsuperuser` and follow the prompts.

**Q: Where are logs stored?**
A: By default, Django logs to the console. Configure logging in `realestate/settings/` for file-based logs.

---

[Previous: Deployment Guide](./06-deployment.md)
