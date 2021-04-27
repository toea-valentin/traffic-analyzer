from subprocess import Popen, PIPE
import time
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

    def init_table(self):
      self.cursor.execute('CREATE TABLE IF NOT EXISTS traffic (id INT AUTO_INCREMENT PRIMARY KEY, timestamp VARCHAR(255), ip VARCHAR(20), port VARCHAR(10))')
       
    
    def add_entry(self, timestamp, ip, port):
        self.cursor.execute(f"INSERT INTO traffic (timestamp, ip, port) VALUES ('{timestamp}', '{ip}', '{port}')")
        self.connection.commit()
#End of DBManager Class


# try to connect to the mysql database
while True:
    try:
        conn = DBManager()
        conn.init_table()
        break
    except:
        time.sleep(2) 


#runs the producer script
Popen(["/bin/bash", "./producer.sh"])

#runs the tcpdump process and binds its output to process.stdout
command = 'tcpdump -l -nn -i any port 80'
process = Popen(command, bufsize=1, universal_newlines=True, shell=True, stdout=PIPE, stderr=PIPE)

#while still receiving valid data from tcdump
while True:
    line = process.stdout.readline()
    words = line.split()
    if len(words) < 7: break
    
    timestamp = words[0] 
    destination = words[6]
    ip = '.'.join(destination.split('.')[0:4])
    port = destination.replace(':','.').split('.')[4]
    
    conn.add_entry(timestamp, ip, port)
