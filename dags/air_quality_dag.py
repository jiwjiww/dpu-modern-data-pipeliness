from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import psycopg2

# กำหนดค่าคอนฟิก
AIRVISUAL_API_KEY = "your_api_key"  # ใส่ API Key ที่ได้จาก AirVisual
CITY = "Bangkok"
COUNTRY = "Thailand"

DB_CONFIG = {
    "host": "your_postgres_host",
    "database": "your_database",
    "user": "your_username",
    "password": "your_password",
    "port": "5432",
}

# ฟังก์ชันดึงข้อมูลจาก AirVisual API
def fetch_aqi_data():
    url = f"http://api.airvisual.com/v2/city?city={CITY}&country={COUNTRY}&key={AIRVISUAL_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "data" in data:
        aqi = data["data"]["current"]["pollution"]["aqius"]
        ts = data["data"]["current"]["pollution"]["ts"]
        return {"timestamp": ts, "aqi": aqi}
    else:
        raise ValueError("API response error")

# ฟังก์ชันบันทึกข้อมูลลง PostgreSQL
def store_aqi_data():
    data = fetch_aqi_data()
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO air_quality (timestamp, aqi) VALUES (%s, %s)
    """
    cursor.execute(insert_query, (data["timestamp"], data["aqi"]))
    
    conn.commit()
    cursor.close()
    conn.close()

# กำหนดค่าเริ่มต้นของ DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# สร้าง DAG
dag = DAG(
    "air_quality_dag",
    default_args=default_args,
    description="DAG for fetching AQI data from AirVisual API",
    schedule_interval=timedelta(days=1),  # รันทุกวัน
    catchup=False,
)

# กำหนด Tasks
fetch_task = PythonOperator(
    task_id="fetch_aqi_data",
    python_callable=fetch_aqi_data,
    dag=dag,
)

store_task = PythonOperator(
    task_id="store_aqi_data",
    python_callable=store_aqi_data,
    dag=dag,
)

# กำหนดลำดับการทำงาน
fetch_task >> store_task
