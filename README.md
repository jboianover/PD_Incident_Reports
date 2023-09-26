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

### Project Goales:
1. Analyze historical crime data from 2018-01-01 to 2018-09-24 (~111K rows).
2. Support analytical queries involving filtering and aggregations.
3. Optimize query performance to ensure they execute efficiently, even as the dataset grows.

### Model design approach:
1. Since the data volume is moderate, starting with a flat table structure seems a reasonable choice because it simplifies
   data loading and mantainance and is suitable for straightforward queries like the requested ones for this challenge.

2. Analyzing the dataset I could infer its volume would be evolving over time, so I'm applying some optimization techniques
   such as indexing to improve query performance.
   
3. I've considered creating a star schema but it has some downsides I think are not worth to carry with on this context:
   - Adds complexity to the database schema.
   - Require more complex logic on ETL processes to load and mantain dimension tables.
   - May have some overhead in terms of storage and mantainance.
   
3. A potential approach for this work would be to choose a hybrid solution:
   Initially, load the data into the flat table and periodically update dimensions such as time, location, incident 
   which would allow us to strike a balance between simplicity and performance. Over time, assesing query performance
   we could consider transitioning to a star schema if query complexity and dataset size increase significantly.
   
#### Conclusions:
The flat table approach with some optimization techniques, overall, provides a well balanced solution with:
   - delivery time
   - data loading complexity
   - initial volume of data
   - straightforward queries to solve the requested analytical reports
   - performant data loading and querying