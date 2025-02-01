with source as (
    select
        coordinates,
        time,
        parameter,
        value
    FROM {{ source('fmi', 'fmi_air_quality') }}
),

transformed as (
    select
        to_double(SPLIT(coordinates, ' ')[0]) as latitude,
        to_double(SPLIT(coordinates, ' ')[1]) as longitude,
        to_timestamp(time) as timestamp,
        TRIM(SPLIT(parameter, '_')[0]) as parameter,
        to_double(value) as value
    from source
    where
        TRY_TO_DOUBLE(value) != 'NaN'
)

select
    *
from transformed