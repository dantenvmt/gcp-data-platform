select
    pickup_date, pickup_hour, trip_count, avg_fare, avg_tip, avg_distance, avg_tip_pct
from
    {{
        source("raw", 'trips_by_hour')
    }}