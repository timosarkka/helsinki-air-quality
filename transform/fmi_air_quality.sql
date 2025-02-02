-- Select the data from source
with source as (
    select
        coordinates,
        time,
        parameter,
        value
    FROM {{ source('fmi', 'fmi_air_quality') }}
),

-- Main transformations
-- Split the coords to lat and long floats
-- Convert time to timestamp
transformed as (
    select
        to_double(split(coordinates, ' ')[0]) as latitude,
        to_double(split(coordinates, ' ')[1]) as longitude,
        to_timestamp(time) as timestamp,
        trim(split(parameter, '_')[0]) as parameter,
        to_double(value) as value
    from source
    where
        try_to_double(value) != 'NaN'
),

-- Make sure no duplicate rows are passed through to analytics layer
deduplicated as (
    select *,
    row_number() over (
        partition by latitude, longitude, parameter, timestamp
        order by timestamp desc
    ) as rn
    from transformed
)

-- Final select
select
    latitude,
    longitude,
    timestamp,
    parameter,
    value
from deduplicated
where rn = 1