--How many burglaries occurred in the South of Market neighborhood between 2018-05-01 and 2018-05-31 inclusive?
select 
COUNT(DISTINCT incident_number) 
from crimes 
where 
incident_category = 'Burglary' 
and analysis_neighborhood = 'South of Market' 
and incident_date between '2018-05-01' and '2018-05-31' ;

--Across the entire dataset, what are the top five neighborhoods with the fewest number of reported incidents? 
--(Note: ignoring null/unknown neighborhood)
select 
analysis_neighborhood,
count(distinct incident_number) 
from crimes 
where analysis_neighborhood is not null 
group by 1 
order by 2 asc 
limit 5;

--Which police district has the most open/active incidents? Which has the fewest?
with last_incident_resolution AS (
    SELECT incident_number, resolution, police_district,
           ROW_NUMBER() OVER (PARTITION BY incident_number ORDER BY incident_datetime DESC) AS row_num
    FROM crimes
), police_district_counts AS (
SELECT
        police_district,
        count(incident_number) AS open_or_active_count,
        ROW_NUMBER() OVER (ORDER BY count(incident_number) DESC) AS rank_max,
        ROW_NUMBER() OVER (ORDER BY count(incident_number) ASC) AS rank_min
    FROM last_incident_resolution
    WHERE resolution = 'Open or Active' AND row_num = 1
    GROUP BY police_district)
    SELECT
    police_district,
    open_or_active_count
FROM police_district_counts where rank_max = 1 or rank_min = 1 order by open_or_active_count desc;