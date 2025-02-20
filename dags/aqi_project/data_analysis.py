import pandas as pd
import matplotlib.pyplot as plt

# อ่านข้อมูล
df = pd.read_csv('data/aqi_data.csv')

# วิเคราะห์ข้อมูล
def analyze_aqi():
    # ค่าเฉลี่ย AQI รายเมือง
    city_avg_aqi = df.groupby('city')['value'].mean()

    # กราฟค่าเฉลี่ย AQI
    plt.figure(figsize=(10,6))
    city_avg_aqi.plot(kind='bar')
    plt.title('Average AQI by City')
    plt.xlabel('City')
    plt.ylabel('Average AQI')
    plt.tight_layout()
    plt.savefig('docs/city_aqi.png')

# เรียกฟังก์ชัน
analyze_aqi()