from sqlalchemy import update
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Float, BigInteger

# Database connection string (update these credentials)
DB_URL = "postgresql+psycopg2://postgres:test1@localhost:5432/air_pollution"

# Initialize SQLAlchemy base and engine
Base = declarative_base()
engine = create_engine(DB_URL, connect_args={"options": "-c client_encoding=utf8"})
Session = sessionmaker(bind=engine)
session = Session()

# Define the table using SQLAlchemy ORM
class AirPollutionPrediction(Base):
    __tablename__ = 'air_pollution_predictions'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    station_name = Column(String(255))
    station_code_pl = Column(String(50))
    station_code_global = Column(String(20))
    pm10_predicted = Column(Float, default=0)
    pm10_real = Column(Float, default=0)
    pm25_predicted = Column(Float, default=0)
    pm25_real = Column(Float, default=0)
    o3_predicted = Column(Float, default=0)
    o3_real = Column(Float, default=0)
    co_predicted = Column(Float, default=0)
    co_real = Column(Float, default=0)
    so2_predicted = Column(Float, default=0)
    so2_real = Column(Float, default=0)
    no2_predicted = Column(Float, default=0)
    no2_real = Column(Float, default=0)

def save_pollution_data(station_code, pollution_name, predicted_value, real_value):
    try:
        # Dynamically construct column names based on pollution_name
        station_code = station_code.encode("utf-8", errors="ignore").decode("utf-8")
        pollution_name = pollution_name.encode("utf-8", errors="ignore").decode("utf-8")

        pollution_predicted = pollution_name + "_predicted"
        pollution_real = pollution_name + "_real"

        # Check if the station already exists in the database
        existing_station = session.query(AirPollutionPrediction).filter(
            AirPollutionPrediction.station_code_pl == station_code
        ).first()

        if existing_station:
            # Update the relevant pollution columns
            stmt = (
                update(AirPollutionPrediction)
                .where(AirPollutionPrediction.station_code_pl == station_code)
                .values(
                    {pollution_predicted: float(predicted_value), pollution_real: float(real_value)}
                )
            )
            session.execute(stmt)
            session.commit()
            print(f"Updated {pollution_name} data for station: {station_code}")
        else:
            # Add a new record if the station does not exist
            new_station = AirPollutionPrediction(
                station_code_pl=station_code,
                station_name=station_code,
                station_code_global=station_code,
                **{pollution_predicted: float(predicted_value), pollution_real: float(real_value)}
            )
            session.add(new_station)
            session.commit()
            print(f"Added new station and {pollution_name} data for station: {station_code}")

    except Exception as e:
        session.rollback()
        print(f"Error while updating or adding pollution data: {e}")

def fetch_max_AQI_values_for_station(station_code):
    try:
        # Query the database for the record of the given station
        record = (
            session.query(AirPollutionPrediction)
            .filter(AirPollutionPrediction.station_code_pl == station_code)
            .first()
        )

        if record:
            # Define relevant columns for pollution data
            pollution_columns = [
                ("pm10_predicted", "pm10_real"),
                ("pm25_predicted", "pm25_real"),
                ("o3_predicted", "o3_real"),
                ("co_predicted", "co_real"),
                ("so2_predicted", "so2_real"),
                ("no2_predicted", "no2_real"),
            ]

            # Initialize variables to track the maximum values and their respective columns
            max_predicted = -float('inf')
            max_real = -float('inf')
            max_predicted_column = None
            max_real_column = None

            # Iterate through the columns and find the maximum values
            for predicted_col, real_col in pollution_columns:
                predicted_value = getattr(record, predicted_col, None)
                real_value = getattr(record, real_col, None)

                # Update the maximum predicted value
                if predicted_value is not None and predicted_value > max_predicted:
                    max_predicted = predicted_value
                    max_predicted_column = predicted_col

                # Update the maximum real value
                if real_value is not None and real_value > max_real:
                    max_real = real_value
                    max_real_column = real_col

            # Return the results as a dictionary
            return max_predicted,max_predicted_column,max_real,max_real_column

        else:
            print(f"No data found for station: {station_code}")
            return None
    except Exception as e:
        print(f"Error fetching max values for station: {e}")
        return None
