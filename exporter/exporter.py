import time
from prometheus_client import start_http_server, Gauge
import mysql.connector

class DBManager:
    def __init__(self):
        config = {
            'user': 'root',
            'password': 'password',
            'host': 'db',
            'port': '3306',
            'database': 'stack'
        }
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def get_endpoints_requests(self):
        self.cursor.execute("SELECT ip, count(*) AS counter FROM traffic GROUP BY ip")
        result = self.cursor.fetchall()
        return result
    
    def count_all(self):
        self.cursor.execute("SELECT count(*) FROM traffic")
        result = self.cursor.fetchall()
        return result
    
    def close(self):
        self.cursor.close()
        self.connection.close()
#End of DBManager Class

endpoints_gauge = Gauge('endpoints_requests', 'Displays the number of requests for each endpoint', ['endpoint'])
count_all_gauge = Gauge('database_table_count', 'Display the number of rows in table')

def update_endpoints():
    retries = 10
    try:
        conn = DBManager()
        data = conn.get_endpoints_requests()
        for d in data:
            endpoints_gauge.labels(d[0]).set(int(d[1]))
    except:
        if retries == 0: return
        retries -= 1
        time.sleep(1)

def update_count_all():
    retries = 10
    try:
        conn = DBManager()
        data = conn.count_all()
        count_all_gauge.set(int(data[0][0]))
    except:
        if retries == 0: return
        retries -= 1
        time.sleep(1)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)

while True:
    update_endpoints()
    update_count_all()
    time.sleep(5)