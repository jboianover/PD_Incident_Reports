# Use an official PostgreSQL as the base image
FROM postgres:16

# Install the PostGIS extension and other required packages
RUN apt-get update && apt-get install -y \
    postgresql-16-postgis-3 \
    postgresql-contrib-16 \ # Add postgresql-contrib package \
    # Add any other packages you need here
    && rm -rf /var/lib/apt/lists/*

# Enable the pg_trgm extension
RUN echo "CREATE EXTENSION IF NOT EXISTS pg_trgm;" >> /docker-entrypoint-initdb.d/init.sql
