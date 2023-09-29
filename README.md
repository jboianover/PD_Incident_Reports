# PD_Incident_Reports
Police Department Incident Reports 2018

This project ingests data from a JSONL file, performs transformations, and inserts it into a PostgreSQL database.

## Prerequisites

- Git: [Git Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Docker: [Docker Installation Guide](https://www.docker.com/get-started)
- Python 3.10
- Any Postgres SQL browser to navigate the database.
   
## Considerations for this project
### Project Goals:
1. Analyze historical crime data from 2018-01-01 to 2018-09-24 (~111K rows).
2. Support analytical queries involving filtering and aggregations.
3. Provide a model design that provides query performance and efficiency.

### Model design decisions:
Since the data volume is moderate, I decided to approach with a flat table structure for initial delivery.
This seems a reasonable choice as it simplifies the process of data loading and its complexity/maintenance.
It is suitable, as well, for straightforward analytical queries like the requested ones for this challenge.

Analyzing the dataset I inferred its volume might evolve over time, so on this approach, I will be applying
some optimization techniques such as indexing by some columns and selecting according data types to improve query performance.

#### Other alternatives   
I've considered creating a star schema but it has some downsides I don't think are worth it in this context:
   - Adds complexity to the database schema.
   - Require more complex logic on the ETL process to load and maintain both the fact and the dimension      tables.
   - May have some overhead in terms of storage and maintenance.
   
Another potential approach to this work, if we had more time and consider it necessary, would be to choose
a hybrid solution:
   Initially, loading the data into the flat table and periodically updating dimensions such as time, location, and incident 
   which would allow us to achieve a balance between simplicity and performance. Over time, when evaluating query performance,
   we might consider transitioning to a star schema if query complexity and dataset size increase significantly.
   
#### Conclusions:
The flat table approach with some optimization techniques provides a well-balanced solution to start with this project considering:
   - time to market
   - data loading complexity, performance, and maintenance
   - initial volume of data which is moderate
   - straightforward queries to solve the requested analytical reports in a performant way
   
### Special considerations:
   - I created indexes such as incident_id, incident_datetime,
     analysis_neighborhood, and a compound by (police_district, resolution) to power up both the          analytical queries of Part 2 and the view of Part 3 which are frequently run.
   - Nevertheless, the logic for the 'nearby_suspicious_activity' column on the view for the Extra           credit, is the most expensive part of the query costs even with using a geospatial index on the         point column because of the cartesian product of joining crimes with itself by incident_id <>          incident_id.
   - I've worked with the query plan to improve as much as possible the query performance with ctes,         avoiding subqueries, EXISTS statements, ensure useful indexes, and even running an ANALYZE table command after data loading to help the table collect statistics and I was able to improve from 
     more than 20 minutes to just one minute and a half (numbers of my local deployment).
   - It's also important to remember this is a domestic PoC deployment and that in real life we should       have much more powerful resources so the performance wouldn't be as much penalized as in my local machine.
   
## Getting Started

1. **Clone this repository:**

   ```bash
   git clone https://github.com/jboianover/PD_Incident_Reports.git
   cd pd_incident_reports

2. **Turn on the Postgres 16 docker container:**
   ```bash
    docker-compose up --build -d
    
*This will also execute the crimes.sql file where the model will be created under PD_Incidents database in public schema.*


3. **Install the needed libraries on your Python 3.10 environment using the requirements.txt attached to the project:**

   ```bash
   pip install -r requirements.txt

4. **Connect to the PostgresSQL in a database browser with the following parameters:**
   - *Database URL*: `postgresql://admin:admin@localhost:5433/PD_Incidents`
   - *Database Host:* `localhost`
   - *Port:* `5433`
   - *Database Name:* `PD_Incidents`
   - *Username:* `admin`
   - *Password:* `admin`
   
## ETL Process Considerations

1. Each time the process run will load the jsonl data in the crimes table, run the analyze table command and drop-create the crimes_summary view.
2. The ETL process is located in python-app/loader.py script and.
3. The JSONL file to be processed has to be located in the same working directory as the python file.
4. The process is designed to append whatever data is found in an sf_crime_reports.jsonl file so be careful to run it always 
   with different source files or ensure to manually delete its data previously. (I didn't choose a delete-insert policy 
   to allow users to just add the desired files with the right naming conventions to append data over time).
5. If we want to use another jsonl file we can locate it in the same working directory and adapting the config.json file accordingly.
6. Each time the loader.py script is run it will create a logging file named *loader_{timestamp}.log* to trace states of the process.