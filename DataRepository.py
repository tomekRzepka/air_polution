import psycopg2
import pandas as pd


# API endpoint and token (not used for actual values but could be useful for future reference)
url = "https://api.waqi.info/feed/here/?token=853cea3387dc974cf970e30ae0e64ba50e3dface"
file_path = "pm10pomiaryCopy.csv"

DB_HOST = "localhost"
DB_NAME = "air_pollution"
DB_USER = "postgres"
DB_PASS = "test1"


def callDatabase(query, params=None):
    connection = None
    cursor = None
    try:
        # Establish connection
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = connection.cursor()

        # Execute query with parameters
        cursor.execute(query, params)

        # Fetch records
        records = cursor.fetchall()
        return connection, cursor, records
    except psycopg2.Error as e:
        print(f"Error executing database query: {e}")
        return None, None, None
    finally:
        if connection:
            connection.commit()


def getHourlyPM10Values(day):

    hourly_data = {}
    query = """
        SELECT pm10 
        FROM test_pollution 
        WHERE EXTRACT(DAY FROM date) IN (%s,%s,%s) AND EXTRACT(HOUR FROM date) = %s
    """

    try:
        # Iteracja po każdej godzinie (1-24)
        for hour in range(0, 24):  # Zakres od 1 do 24
            _, _, records = callDatabase(query, (day-3,day-2,day-1,hour,))
            if records:
                # Pobieramy tylko wartości PM10
                hourly_data[hour] = [row[0] for row in records]
            else:
                # Jeśli brak danych dla danej godziny
                hourly_data[hour] = []

        print("Dane PM10 dla każdej godziny zostały pobrane.")
        return hourly_data

    except psycopg2.Error as e:
        print(f"Błąd podczas przetwarzania danych: {e}")
        return None

def getPM10Values(day):

    # Queries
    selectPM10BorderValuesQuery = """
        SELECT MIN(pm10), MAX(pm10) 
        FROM test_pollution 
        WHERE EXTRACT(DAY FROM date) = %s
    """
    selectPM10Query = """
        SELECT date, pm10
        FROM test_pollution 
        ORDER BY date;
    """

    try:
        # Fetch border values
        _, _, border_records = callDatabase(selectPM10BorderValuesQuery, (day,))
        if not border_records or len(border_records) == 0:
            print("No border values found.")
            return None, None, None

        min_pm10, max_pm10 = border_records[0]

        # Fetch PM10 data
        connection, cursor, records = callDatabase(selectPM10Query,(day,))
        if not records or len(records) == 0:
            print("No PM10 data found.")
            return None, min_pm10, max_pm10

        column_names = [desc[0] for desc in cursor.description]
        data = pd.DataFrame(records, columns=column_names)

        print("Pollutant data successfully retrieved from the database.")
        return data, min_pm10, max_pm10

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None, None, None

    finally:
        # Ensure the connection is closed
        if cursor:
            cursor.close()
        if connection:
            connection.close()

