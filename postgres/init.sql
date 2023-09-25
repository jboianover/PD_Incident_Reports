-- Create a sample table
CREATE TABLE IF NOT EXISTS sample_data (
    id serial PRIMARY KEY,
    name VARCHAR(255)
);

-- Insert some initial data
INSERT INTO sample_data (name) VALUES ('Item 1'), ('Item 2');
