CREATE TABLE simulation_results (
    id SERIAL PRIMARY KEY,
    simulation_date TIMESTAMP NOT NULL,
    station_name VARCHAR(255) NOT NULL,
    hour INTEGER NOT NULL,
    simulated_mean FLOAT NOT NULL,
    lower_confidence FLOAT NOT NULL,
    upper_confidence FLOAT NOT NULL,
    actual_value FLOAT NOT NULL
);