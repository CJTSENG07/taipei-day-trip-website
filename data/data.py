import json,mysql.connector,os

mydb = mysql.connector.connect(
   host = "localhost",
   port = 3306,
   user = 'root',
   password = '123',
   database = "taipei",
   charset = "utf8"
)

mycursor = mydb.cursor()


sql = '''CREATE TABLE attractions (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255),
    description TEXT,
    address TEXT,
    transport TEXT,
    mrt VARCHAR(255),
    latitude VARCHAR(55),
    longitude VARCHAR(55),
    images TEXT
    );'''


mycursor.execute(sql)

with open("taipei-attractions.json","r",encoding="utf-8") as file:
    data_dic = json.load(file)
    #使用loads變成python字典
    results = data_dic['result']['results']

    for result in results:
        id = result['_id']
        name = result['stitle']
        category = result['CAT2']
        description = result['xbody']
        address = result['address']
        transport = result['info']
        mrt = result['MRT']
        latitude = result['latitude']
        longitude = result['longitude']
        
        imgsUrl = result['file'].split('http://')[1:]
        imgUrlList = []
        for imgUrl in imgsUrl:
            if imgUrl.endswith(('jpg','JPG','png','PNG')):
               imgUrl = 'http://' + imgUrl 
               imgUrlList.append(imgUrl)
        images_url = json.dumps(imgUrlList)

        mycursor.execute(
            "INSERT INTO attractions(id, name, category, description, address, transport, mrt, latitude, longitude, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (id, name, category, description, address, transport, mrt, latitude, longitude, images_url)
        )
        mydb.commit()








        
        


