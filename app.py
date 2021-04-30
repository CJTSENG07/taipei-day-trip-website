from flask import *
import json
import mysql.connector
import os

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSON_SORT_KEYS"] = False

# MySQL連線
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='c5vvbq123',
    database='taipei',
    charset='utf8'
)
mycursor = mydb.cursor()


# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# APIs


@app.route("/api/attractions", methods=['GET'])
def getAttractions():

    try:
        page = request.args.get("page", type=int)
        keyword = request.args.get("keyword")

        if keyword == None:
            spotRangeStart = 1+page*12
            spotRangeEnd = 12+page*12
            sql = "SELECT * FROM attractions WHERE id BETWEEN '%s' AND '%s';"
            val = (spotRangeStart, spotRangeEnd, )
            mycursor.execute(sql, val)
            spotResult = mycursor.fetchall()

            spotLists12 = []
            for i in range(len(spotResult)):
                id = spotResult[i][0]
                name = spotResult[i][1]
                category = spotResult[i][2]
                description = spotResult[i][3]
                address = spotResult[i][4]
                transport = spotResult[i][5]
                mrt = spotResult[i][6]
                latitude = spotResult[i][7]
                longitude = spotResult[i][8]
                images = spotResult[i][9]
                spotLists = {
                    "id": id,
                    "name": name,
                    "category": category,
                    "description": description,
                    "address": address,
                    "transport": transport,
                    "mrt": mrt,
                    "latitude": latitude,
                    "longitude": longitude,
                    "images": images
                }
                spotLists12.append(spotLists)

                if page < 27:
                    nextPage = page+1
                else:
                    nextPage = None

        elif keyword != None:

            sql = "SELECT * FROM attractions WHERE (name LIKE %s OR category LIKE %s OR description LIKE %s OR address LIKE %s OR mrt LIKE %s) LIMIT %s, 13 ;"

            keyword = "%"+keyword+"%"
            offset = page * 12
            val = (keyword, keyword, keyword, keyword, keyword, offset)
            mycursor.execute(sql, val)
            spotResult = mycursor.fetchall()

            spotLists12 = []
            for i in range(len(spotResult)):
                id = spotResult[i][0]
                name = spotResult[i][1]
                category = spotResult[i][2]
                description = spotResult[i][3]
                address = spotResult[i][4]
                transport = spotResult[i][5]
                mrt = spotResult[i][6]
                latitude = spotResult[i][7]
                longitude = spotResult[i][8]
                images = spotResult[i][9]
                spotLists = {
                    "id": id,
                    "name": name,
                    "category": category,
                    "description": description,
                    "address": address,
                    "transport": transport,
                    "mrt": mrt,
                    "latitude": latitude,
                    "longitude": longitude,
                    "images": images
                }
                spotLists12.append(spotLists)

            if len(spotResult) == 13:
                nextPage = page+1
                spotLists12.pop()
            else:
                nextPage = None

        searchResult = {
            "nextPage": nextPage,
            "data": spotLists12
        }
        return jsonify(searchResult)

    except:
        errormsg = {
            "error": True,
            "message": "伺服器錯誤"
        }
        return jsonify(errormsg)


@app.route("/api/attraction/<attractionId>")
def get_attractionById(attractionId):
    try:
        sql = "SELECT * FROM attractions WHERE id = %s ;"
        val = (attractionId, )
        mycursor.execute(sql, val)
        attractionIDResult = mycursor.fetchone()

        id = attractionIDResult[0]
        name = attractionIDResult[1]
        category = attractionIDResult[2]
        description = attractionIDResult[3]
        address = attractionIDResult[4]
        transport = attractionIDResult[5]
        mrt = attractionIDResult[6]
        latitude = attractionIDResult[7]
        longitude = attractionIDResult[8]
        images = attractionIDResult[9]
        spotList = {
            "id": id,
            "name": name,
            "category": category,
            "description": description,
            "address": address,
            "transport": transport,
            "mrt": mrt,
            "latitude": latitude,
            "longitude": longitude,
            "images": images
        }

        searchResult = {
            "data": spotList
        }
        return jsonify(searchResult)

    except:
        errormsg = {
            "error": True,
            "message": "網頁伺服器錯誤"
        }
        return jsonify(errormsg)


# app.run(host="0.0.0.0",port=3000)
app.run(port=3000,debug=True)