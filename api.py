from flask import Flask, jsonify, make_response, request
from flask_mysqldb import MySQL


app = Flask(__name__)

# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "winee"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data =cur.fetchall()
    cur.close()
    return data

# get all wine 
@app.route("/wines", methods=["GET"])
def get_wines():
    data = data_fetch("""
                      SELECT * FROM wine 
                      """)
    return make_response(jsonify(data), 200)

# get wine by id
@app.route("/wines/<int:id>", methods=["GET"])
def get_wine_by_id(id):
    data = data_fetch("""
                      SELECT * FROM wine WHERE wine_id = {}
                      """.format(id))
    return make_response(jsonify(data), 200)

# get top 10 wine
@app.route("/wines/top_10_expensive_wine", methods=["GET"])
def get_top_10_wine():
    cur = mysql.connection.cursor()
    cur.execute("""
                     select wine.wine_name, wine.color, winemaker.winemaker_name, wine.price_bottle 
	                from wine inner join winemaker on wine.winemaker_id = winemaker.winemaker_id 
                    order by wine.price_bottle desc limit 10
                      """)
    top_wines = cur.fetchall()
    cur.close()
    return make_response(jsonify(top_wines), 200)

# get food name w wine name
@app.route("/wines/food_paired_with_wine", methods=["GET"])
def get_food_with_wine():
    cur = mysql.connection.cursor()
    cur.execute("""
                    select wine_goes_with_food.food_name, wine.wine_name 
	                from wine_goes_with_food inner join wine on wine_goes_with_food.wine_id = wine.wine_id
                      """)
    food_with_wine = cur.fetchall()
    cur.close()
    return make_response(jsonify(food_with_wine), 200)

# wine name and winemaker name and country name
@app.route("/wines/winemaker_and_country", methods=["GET"])
def get_winemaker_and_country():
    cur = mysql.connection.cursor()
    cur.execute("""
                    select wine.wine_name, winemaker.winemaker_name, countries.country_name 
	                from winemaker inner join countries on winemaker.country_code = countries.country_code 
	                inner join wine on winemaker.winemaker_id = wine.winemaker_id
                      """)
    winemaker_and_country = cur.fetchall()
    cur.close()
    return make_response(jsonify(winemaker_and_country), 200)

# add winemaker
@app.route("/wines", methods=["POST"])
def add_winemaker():
    cur = mysql.connection.cursor()
    info = request.get_json()
    country_code = info["country_code"]
    winemaker_name = info["winemaker_name"]
    cur.execute("""
                INSERT INTO winemaker (country_code, winemaker_name)
                VALUES (%s, %s)
                """, (country_code, winemaker_name),)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message" : "winemaker added successfully", "rows_affected": rows_affected}), 201)

# update winemaker
@app.route("/wines/<int:id>", methods=["PUT"])
def update_winemaker(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    country_code = info["country_code"]
    winemaker_name = info["winemaker_name"]
    cur.execute("""
                UPDATE winemaker SET country_code = %s, winemaker_name = %s
                WHERE winemaker_id = %s
                """, (country_code, winemaker_name, id),)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message" : "winemaker updated successfully", "rows_affected": rows_affected}), 200)

# delete winemaker
@app.route("/wines/<int:id>", methods=["DELETE"])
def delete_winemaker(id):
    cur = mysql.connection.cursor()
    cur.execute("""
                DELETE FROM winemaker where winemaker_id = %s
                """,(id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message" : "winemaker deleted successfully", "rows_affected": rows_affected}), 200)


if __name__ == "__main__":
    app.run(debug=True)