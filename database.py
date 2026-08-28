import pymysql

try:
    conn = pymysql.connect(
        host="mysql-97afee7-d1u-a57b.k.aivencloud.com",
        port=26333,
        user="avnadmin",
        password="AVNS_sJpBYdghqeVECSBW6jM",
        database="quan_ly_khach_hang",
        ssl={"ca":"ca.pem"}
    )
    print("Connected")
except Exception as e:
    print(e)
