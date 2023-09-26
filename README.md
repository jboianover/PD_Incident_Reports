# PD_Incident_Reports
Police Department Incident Reports 2018 to Present

This project ingests data from a JSONL file, performs transformations, and inserts it into a PostgreSQL database.

## Prerequisites

- Docker: [Docker Installation Guide](https://www.docker.com/get-started)
- Git: [Git Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Python 3.10

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/jboianover/PD_Incident_Reports.git)https://github.com/jboianover/PD_Incident_Reports.git
   cd pd_incident_reports
   docker-compose up -d


## Considerations for this project

### Project Goals:
1. Analyze historical crime data from 2018-01-01 to 2018-09-24 (~111K rows).
2. Support analytical queries involving filtering and aggregations.
3. Optimize query performance to ensure they execute efficiently, even as the dataset grows.

### Model design decisions:
Since the data volume is moderate, I decided to start with a flat table structure approach as an MVP for initial delivery.
This seems a reasonable choice as it simplifies the process of data loading and its complexity and maintenance.
It is suitable, as well, for straightforward analytical queries like the requested ones for this challenge.

Analyzing the dataset I inferred its volume might evolve over time, so on this approach, I will be applying
some optimization techniques such as indexing by some columns and selecting according data types to improve query performance.

#### Other alternatives   
I've considered creating a star schema but it has some downsides I don't think are worth it in this context:
   - Adds complexity to the database schema.
   - Require more complex logic on ETL processes to load and maintain dimension tables.
   - May have some overhead in terms of storage and maintenance.
   
Another potential approach to this work, if we had some more time and consider it necessary, would be to choose
a hybrid solution:
   Initially, loading the data into the flat table and periodically updating dimensions such as time, location, and incident 
   which would allow us to achieve a balance between simplicity and performance. Over time, when evaluating query performance,
   we might consider transitioning to a star schema if query complexity and dataset size increase significantly.
   
#### Conclusions:
The flat table approach with some optimization techniques provide a well-balanced solution as an MVP considering:
   - delivery time of the project
   - data loading complexity, performance and maintenance
   - initial volume of data which is moderate
   - straightforward queries to solve the requested analytical reports in a performant way