from flask import Flask , request,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_restplus import Api, fields , Resource 



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
app.config['SECRET_KEY']=True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api()
api.init_app(app)

#Table

class Fruit(db.Model):
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	fruit_name = db.Column(db.String)
	quantity = db.Column(db.Integer)
	price = db.Column(db.Integer)

class FruitSchema(ma.Schema):
    class Meta:
        fields = ('id','fruit_name','quantity','price')

model = api.model('demo',{
    'fruit_name':fields.String('Enter Fruit Name'),
    'quantity':fields.Integer('Enter Quantity'),
    'price':fields.Integer('Enter Price')
})

fruit_schema = FruitSchema()
fruits_schema = FruitSchema(many=True)

@api.route('/get')
class getdata(Resource):
    def get(self):
        return jsonify(fruits_schema.dump(Fruit.query.all()))

@api.route('/post')
class postdata(Resource):
    @api.expect(model)
    def post(self):
        fruit = Fruit(fruit_name=request.json['fruit_name'],quantity=request.json['quantity'],price=request.json['price'])
        db.session.add(fruit)
        db.session.commit()
        return {'message':'data added to database'}

@api.route('/put/<int:id>')
class putdata(Resource):
    @api.expect(model)
    def put(self,id):
        fruit = Fruit.query.get(id)
        fruit.fruit_name = request.json['fruit_name']
        fruit.quantity = request.json['quantity']
        fruit.price = request.json['price']
        db.session.commit()
        return {'message':'data updated'}

@api.route('/delete/<int:id>')
class deletedata(Resource):
    def delete(self,id):
        fruit = Fruit.query.get(id)
        db.session.delete(fruit)
        db.session.commit()
        return {'message':'data deleted successfully'}

# @name_space.route("/")
# class LogList(Resource):
#     def get(self):  # will be used to fetch all record from log later
#         return {
#             "status": "List all log"
#         }

#     def post(self):  # will be used to create a new log record
#         return {
#             "status": "Create new log"
#         }



# @name_space.route("/<int:id>")
# class LogList(Resource):
# 	def get(self,id):
# 		return {
# 			"status":"See detail for log with id " + str(id)
# 		}
	
# 	def put(self,id):
# 		return {
# 			"status":"Updated details from log with id" + str(id)
# 		}

# 	def delete(self,id):
# 		return {
# 			"status":"Deleted detaiils from log with id" + str(id)
# 		}




if __name__=="__main__":
	app.run()



	