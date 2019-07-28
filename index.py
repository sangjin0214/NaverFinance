import requests
import time
import datetime
import pymysql


url = 'https://polling.finance.naver.com/api/realtime.nhn'
params = {
    "query": "SERVICE_ITEM:035420"
}

table = "stock"

result = requests.get(url, params=params).json()

while(True):
    if result["resultCode"] == "success":
        for areas in result["result"]["areas"]:
            for data in areas["datas"]:
                if data["ms"] == "CLOSE":
                    time.sleep(60)
                    continue
                price = data["nv"]
                td = datetime.timedelta(hours=9)
                now = datetime.datetime.now()
                k_now = now + td
                date = k_now.strftime('%y%m%d%H%M')
                try:
                    if date is "" or price is "":
                        raise Exception('no data')
                    db = pymysql.connect(host="remotemysql.com",
                                         port=3306,
                                         user="8lBKDiknZZ",
                                         passwd="mfmlvb3guf",
                                         db="8lBKDiknZZ",
                                         charset="utf8")

                    with db.cursor() as cursor:
                        query = "insert into {0}(date, price) values('{1}', {2});".format(table, date, price)
                        cursor.execute(query)
                        db.commit()
                except Exception as e:
                    print(e)
                finally:
                    db.close()

    time.sleep(60)
