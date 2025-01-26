
CREATE TABLE IF NOT EXISTS public.air_pollution_predictions
(
    id bigint NOT NULL,
    station_name character varying(255) COLLATE pg_catalog."default",
    station_code_pl character varying(50) COLLATE pg_catalog."default",
    station_code_global character varying(20) COLLATE pg_catalog."default",
    pm10_predicted double precision DEFAULT 0,
    pm10_real double precision DEFAULT 0,
    pm25_predicted double precision DEFAULT 0,
    pm25_real double precision DEFAULT 0,
    o3_predicted double precision DEFAULT 0,
    o3_real double precision DEFAULT 0,
    co_predicted double precision DEFAULT 0,
    co_real double precision DEFAULT 0,
    so2_predicted double precision DEFAULT 0,
    so2_real double precision DEFAULT 0,
    no2_predicted double precision DEFAULT 0,
    no2_real double precision DEFAULT 0,
    CONSTRAINT air_pollution_predictions_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.air_pollution_predictions
    OWNER to postgres;