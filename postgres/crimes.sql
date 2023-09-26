CREATE TABLE crimes (
    row_id PRIMARY KEY,  -- Unique identifier for each row
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
