import json,mysql.connector,os

mydb = mysql.connector.connect(
   host = "localhost",
   user = os.environ.get('DB_USER'),
   password = os.environ.get('DB_PASS'),
   database = "taipei",
   charset = "utf8"
)

mycursor = mydb.cursor()


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

        cursor.execute(
            "INSERT INTO attractions(id, name, category, description, address, transport, mrt, latitude, longitude, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (id, name, category, description, address, transport, mrt, latitude, longitude, images_url)
        )
        mydb.commit()








        
        


