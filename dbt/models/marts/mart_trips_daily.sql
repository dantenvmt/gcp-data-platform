Select 
    SUM(trip_count) as total_trips,
    Round(AVG(avg_fare),2) as average_fare,
    Round(AVG(avg_tip_pct),2) as average_tip_percentage, 
    pickup_date
from {{ ref("stg_trips_by_hour") }}
group by pickup_date
order by pickup_date