CREATE TABLE crimes (
    row_id INT PRIMARY KEY,  -- Unique identifier for each row
    incident_id INT,           -- System-generated identifier for incident reports
    incident_number INT,       -- Case number for the incident
    cad_number INT,            -- Computer Aided Dispatch number
    incident_datetime TIMESTAMP,  -- Date and time when the incident occurred
    incident_date DATE,        -- Date of the incident
    incident_time TIME,        -- Time of the incident
    incident_year INT,         -- Year of the incident
    incident_day_of_week TEXT, -- Day of the week when the incident occurred
    report_datetime TIMESTAMP, -- Date and time when the report was filed
    report_type_code TEXT,     -- Code for report types
    report_type_description TEXT,  -- Description of the report type
    filed_online BOOLEAN,      -- Indicates if the report was filed online
    incident_code TEXT,        -- System code to describe the type of incident
    incident_category TEXT,    -- Category mapped to the incident code
    incident_subcategory TEXT, -- Subcategory mapped to the incident code
    incident_description TEXT, -- Description of the incident
    resolution TEXT,           -- Resolution of the incident
    intersection TEXT,         -- Street intersection where the incident occurred
    cnn TEXT,                  -- Unique identifier of the intersection
    police_district TEXT,      -- Police district reflecting current boundaries
    analysis_neighborhood TEXT,  -- Analysis neighborhood
    supervisor_district INT,   -- Supervisor district number
    latitude FLOAT,            -- Latitude coordinate
    longitude FLOAT,           -- Longitude coordinate
    point TEXT                 -- Point geometry for mapping features
);

-- Index for incident_id (Primary Key)
CREATE UNIQUE INDEX idx_incident_id ON crimes (incident_id);

-- Index for incident_datetime
CREATE INDEX idx_incident_datetime ON crimes (incident_datetime);

-- Compound Index for police_district and resolution
CREATE INDEX idx_analysis_neighborhood_resolution ON crimes (police_district, resolution);

-- Compound Index for analysis_neighborhood and incident_datetime for the neighborhood_incidents view column
CREATE INDEX idx_neighborhood_datetime ON crimes (analysis_neighborhood, incident_datetime);


--Optionals:

-- Install pg_trgm extension (if not already installed)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- GIN Index for incident_categories (only if frequently queried)
CREATE INDEX idx_gin_incident_categories ON crimes USING GIN (incident_category gin_trgm_ops);

-- Install PostGIS extension (if not already installed)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create a geospatial index on the point column
CREATE INDEX idx_geospatial_point ON crimes USING GIST (point gist_trgm_ops);