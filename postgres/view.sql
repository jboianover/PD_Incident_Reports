DROP VIEW IF EXISTS crimes_summary;
CREATE VIEW crimes_summary AS
with incident_ts as (
SELECT
    distinct
    DATE_TRUNC('hour', c.incident_datetime) + 
        INTERVAL '15 minutes' * FLOOR(EXTRACT(MINUTE FROM c.incident_datetime) / 15) AS incident_ts,
    c.incident_id,
    coalesce(c.analysis_neighborhood, '') analysis_neighborhood,
    c.point
    from crimes c
    ) 
, incident_cat as (
SELECT
    incident_id,
    STRING_AGG(DISTINCT incident_category, '||') AS incident_categories,
    MIN(incident_datetime) AS first_incident_datetime,
    MIN(report_datetime) AS first_report_datetime
    from crimes
    group by incident_id
    )
 , neigh_incidents as (
 select 
        count(incident_id) neighborhood_incidents, 
        coalesce(analysis_neighborhood, '') analysis_neighborhood,
        DATE_TRUNC('hour', incident_datetime) + 
        INTERVAL '15 minutes' * FLOOR(EXTRACT(MINUTE FROM incident_datetime) / 15) lower_limit,
        DATE_TRUNC('hour', incident_datetime) + 
        INTERVAL '15 minutes' * FLOOR(EXTRACT(MINUTE FROM incident_datetime) / 15) +
        INTERVAL '15 minutes' upper_limit
        from crimes
        group by
        analysis_neighborhood,
        lower_limit,
        upper_limit
        )
, distinct_incidents as 
(
        select distinct incident_id, DATE_TRUNC('hour', incident_datetime) + INTERVAL '15 minutes' * FLOOR(EXTRACT(MINUTE FROM incident_datetime) / 15) AS incident_ts, point 
        from crimes where point is not null)       
, final_query as (
select 
        c.incident_id,
        c.incident_ts,
        e.incident_categories,
        e.first_incident_datetime,
        e.first_report_datetime,
        f.neighborhood_incidents,
         CASE WHEN c2.point is not null THEN TRUE ELSE FALSE END AS nearby_suspicious_activity
from incident_ts c
inner join incident_cat e on c.incident_id = e.incident_id
inner join neigh_incidents f on c.analysis_neighborhood = f.analysis_neighborhood and c.incident_ts >= f.lower_limit and c.incident_ts < f.upper_limit
left join distinct_incidents c2 on c.incident_id <> c2.incident_id and c.incident_ts = c2.incident_ts and ST_DWithin(c.point, c2.point, 1000)
)
select 
distinct 
    incident_ts, 
    incident_id, 
    incident_categories, 
    first_incident_datetime, 
    first_report_datetime, 
    neighborhood_incidents, 
    nearby_suspicious_activity
from final_query;