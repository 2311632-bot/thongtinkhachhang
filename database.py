import pymysql


def get_connection():

    conn = pymysql.connect(

        host="mysql-97afee7-dlu-a57b.k.aivencloud.com",

        port=26333,

        user="avnadmin",

        password="AVNS_sJpBYdghqeVECSBW6jM",

        database="quan_ly_khach_hang",

        ssl={
            "ca": "ca.pem"
        }

    )

    return conn
