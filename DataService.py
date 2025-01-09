import DataRepository as dr
import numpy as np
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from datetime import datetime

def save_simulation_to_db(
    simulated_means, lower_conf_intervals, upper_conf_intervals, actual_values, hours, station_name="Station 1"
):
    # Połączenie z bazą danych (dostosuj dane logowania)
    engine = create_engine("postgresql+psycopg2://postgres:test1@localhost/air_pollution")
    connection = engine.connect()
    metadata = MetaData()

    # Definicja tabeli w kodzie (powinna odpowiadać tabeli w bazie)
    simulation_table = Table(
        'simulation_results', metadata,
        Column('id', Integer, primary_key=True),
        Column('simulation_date', DateTime, nullable=False),
        Column('station_name', String(255), nullable=False),
        Column('hour', Integer, nullable=False),
        Column('simulated_mean', Float, nullable=False),
        Column('lower_confidence', Float, nullable=False),
        Column('upper_confidence', Float, nullable=False),
        Column('actual_value', Float, nullable=False)
    )

    metadata.create_all(engine)  # Tworzy tabelę, jeśli nie istnieje

    # Data symulacji
    simulation_date = datetime.now()

    # Przygotowanie danych do zapisu
    insert_data = []
    for hour, mean, lower, upper, actual in zip(hours, simulated_means, lower_conf_intervals, upper_conf_intervals, actual_values):
        insert_data.append({
            'simulation_date': simulation_date,
            'station_name': station_name,
            'hour': hour,
            'simulated_mean': mean,
            'lower_confidence': lower,
            'upper_confidence': upper,
            'actual_value': actual
        })

    # Zapis do bazy
    connection.execute(simulation_table.insert(), insert_data)
    print(f"Saved {len(insert_data)} rows to the database.")


save_simulation_to_db(
    simulated_means=simulated_means,
    lower_conf_intervals=lower_conf_intervals,
    upper_conf_intervals=upper_conf_intervals,
    actual_values=actual_values,
    hours=hours,
    station_name="Example Station"
)