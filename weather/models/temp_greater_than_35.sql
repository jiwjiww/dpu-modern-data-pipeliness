SELECT 
    dt,
    temp,
    feels_like

FROM {{ source('dpu','weathers') }}
where temp > 30