Select 
    FORMAT_DATE('%A', pickup_date) as  weekday,
    EXTRACT(DAYOFWEEK from pickup_date) as weekday_num,
    pickup_hour,
    round(avg(trip_count), 0) as avg_trips
from
    {{ref('stg_trips_by_hour')}}
group by weekday, weekday_num, pickup_hour
order by weekday_num, pickup_hour