from flask import *
from flask_restplus import Api, Resource, fields
import sqlite3
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
# api_app = Api(app = app, 
#               version = "1.0", 
#         	  title = "Name Recorder",
#               description = "Manage names of various users of the application")

# name_space = api_app.namespace('main', description='Main APIs')
"""
Template for Swagger

@name_space.route("/")

class MainClass(Resource):

	def get(self):

		return {

			"status": "Got new data"

		}

	def post(self):

		return {

			"status": "Posted new data"

		}
"""


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model.save()
        # Failure to return a redirect or render_template
    else:
        return render_template('index.html')

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        model.save()
    else:
        return render_template("add.html")



@app.route("/savedetails",methods=['POST','GET'])
def savedetails():
    msg = "Added"  
    if request.method == "POST":  
        try:  
            fruit_name = request.form["fruit_name"]  
            quantity = request.form["quantity"]  
            price = request.form["price"]  
            with sqlite3.connect("fruits.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into fruit (fruit_name, quantity, price) values (?,?,?)",(fruit_name,quantity,price))  
                con.commit()  
                msg = "Fruit Added"
                # resp = jsonify('Fruit added successfully!')
                # resp.status_code = 200
                # return resp
        except:  
            con.rollback()  
            msg = "Cannot add fruit to the list"  
        finally:  
            return render_template("success.html",msg = msg)  
            con.close()
    # else:
    #     return  page_not_found()

@app.route("/view")  
def view():  
    con = sqlite3.connect("fruits.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from fruit")  
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows)  

# @app.route("/update", methods = ['GET','POST'])
# def update():
#     if request.method == 'POST':
#         model.save()
#     else:
#         return render_template("update.html")
     

# @app.route("/updaterecord",methods = ["POST"])
# def updaterecord():
#     msg = "Enter Data"
#     id = request.form["id"]
#     with sqlite3.connect("fruits.db") as con:
#         try:
#             cur = con.cursor()
#             fruit_name = request.form["fruit_name"]
#             quantity = request.form["quantity"]
#             price = request.form["price"]
#             cur.execute(" update fruit set fruit_name = ?, quantity = ?, price =? where id = ?;", id, fruit_name,quantity,price)
#             msg = "Item Updated"
#         except:
#             msg = "Item cannot be updated"
#         finally:
#             return render_template("update_record.html")

 
@app.route("/delete")  
def delete():  
    return render_template("delete.html")  
 

@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id = request.form["id"]  
    with sqlite3.connect("fruits.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from fruit where id = ?",id)  
            msg = "Item successfully deleted"
            # resp = jsonify('Fruit deleted successfully!')
            # resp.status_code = 200
            # return resp 
        except:  
            msg = "Item can't be deleted"  
        finally:  
            return render_template("delete_record.html",msg = msg)  

@app.errorhandler(404)
def page_not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/api/v1/resources/fruits/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('fruits.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_fruits = cur.execute('SELECT * FROM fruit;').fetchall()

    return jsonify(all_fruits)

@app.route('/api/v1/resources/fruits', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    fruit_name = query_parameters.get('fruit_name')
    quantity = query_parameters.get('quantity')
    price = query_parameters.get('price')

    query = "SELECT * FROM fruit WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if fruit_name:
        query += ' fruit_name=? AND'
        to_filter.append(fruit_name)
    if quantity:
        query += ' quantity=? AND'
        to_filter.append(quantity)
    if price:
        query += ' price=? AND'
        to_filter.append(price)
    if not (id or fruit_name or quantity or price):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('fruits.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

if __name__ == "__main__":  
    app.run(debug = True)  