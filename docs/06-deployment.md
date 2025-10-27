# Deployment & Environment

[Previous: API Endpoints](./05-api.md) | [Next: Contribution Guide](./07-contributing.md)

---

## Deployment

### Local Development
- Use `python manage.py runserver` for local testing.
- Media files are stored in the `media/` directory.

### Production Deployment
- Use `docker-compose.yml` for containerized deployment.
- Run `deploy.sh` for automated deployment steps.
- Configure environment variables in `realestate/settings/` as needed.

## Environment Variables
- `DJANGO_SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `MEDIA_ROOT`: Path for media files

---

[Previous: API Endpoints](./05-api.md) | [Next: Faq Guide](./07-faq.md)
