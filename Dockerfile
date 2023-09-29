# Use an official PostgreSQL as the base image
FROM postgres:16

# Install the PostGIS extension and other required packages
RUN apt-get update && apt-get install -y \
    postgresql-16-postgis-3 \
    postgresql-contrib-16 \
    && rm -rf /var/lib/apt/lists/*
