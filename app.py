from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snippets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(25), nullable=False)
    code = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Snippet(language={language}, code={code})"

# Create database within app context 
with app.app_context():
    db.create_all()

snippet_put_args = reqparse.RequestParser()
snippet_put_args.add_argument("language", type=str, help="Name of the programming language is required", required=True)
snippet_put_args.add_argument("code", type=str, help="Code snippet is required", required=True)

resource_fields = {
    'id' : fields.Integer,
    'language' : fields.String,
    'code' : fields.String
}

class Hello(Resource):
    def get(self):
        return {"data": "Hello To My First API"}

class Snipnets(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = Snippet.query.order_by(Snippet.id).all()
        return result, 200
    
    @marshal_with(resource_fields)
    def post(self):
        args = snippet_put_args.parse_args()
        codeAdd = Snipnets(language=args['language'], code=args['code'])
        db.session.add(codeAdd)
        db.session.commit()
        return codeAdd, 201
    
class SnipnetsID(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        result = Snippet.query.get_or_404(id)
        return result, 200
  
api.add_resource(Hello, "/")
api.add_resource(Snipnets, "/snippet")
api.add_resource(SnipnetsID, "/snippet/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)