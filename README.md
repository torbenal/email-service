# Email service

This is a full-stack approach to the email service code challenge utilizing SendGrid, with SparkPost as a fallback. It has a Python backend running Flask, connected to a PostgreSQL database. The frontend is built with React.js.

The entire application is containerized using Docker. Running locally requires the following .env files in the `backend/` directory:

api.env:
 - `POSTGRES_URL`: Follows format `postgresql://{username}:{password}@{container_name}:5432/{database_name}`
 - `SENDGRID_API_KEY`
 - `SPARKPOST_API_KEY`

postgres.env:
 - `POSTGRES_USER`
 - `POSTGRES_PASSWORD`
 - `POSTGRES_DB`

 To run: `docker-compose up --build` \
 Hosted here: http://206.189.12.171/