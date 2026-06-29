select
    pickup_hour,
    round(avg(trip_count), 0) as avg_trips,
    round(avg(avg_fare), 2)   as avg_fare,
    round(avg(avg_tip_pct), 2) as avg_tip_pct
from {{ ref('stg_trips_by_hour') }}
group by pickup_hour
order by pickup_hour