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


    

if __name__ == "__main__":
    app.run(debug=True)