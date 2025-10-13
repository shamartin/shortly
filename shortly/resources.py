from flask_restful import Resource, reqparse, fields, marshal_with,abort
from .models import UrlModel
from . import db
from .utils import create_shortcode
from flask import current_app

user_args = reqparse.RequestParser()
user_args.add_argument('full_url', type=str, required=True, help="full url cannot be blank")

urlFields = {
    'id' : fields.Integer,
    'full_url' : fields.String,
    'short_code' : fields.String,
}

class Urls(Resource):
    @marshal_with(urlFields)
    def get(self, short_code=None):
        if short_code is not None:
            url = UrlModel.query.filter_by(short_code=short_code).first()
            if not url or not url.full_url or url.full_url.strip() == "":
                abort(404, message= "The requested URL could not be found")
            return url
        else:
            urls = UrlModel.query.all()
            return urls
    
    @marshal_with(urlFields)
    def post(self):
        args = user_args.parse_args()

        #validate 
        #TODO: create helper function with stricter validation to ensure no one blows up the db
        full_url = args["full_url"].strip()
        if not full_url.startswith(("http://", "https://")):
            full_url = "https://" + full_url

        #check for duplicates
        duplicate_url = UrlModel.query.filter_by(full_url=full_url).first()
        if duplicate_url:
            abort(409, message= f"The requested URL has already beeen shortened. Please use this URL: {current_app.config['BASE_URL']}/{duplicate_url.short_code}")
        else:
            url = UrlModel(full_url=full_url)
            #create new url entry with the full url and id -> generate shortcode from id 
            db.session.add(url)
            db.session.flush() #do not save until we are done
            #come up with the shortened url and assign to database
            url.short_code = create_shortcode(int(url.id))
            db.session.commit()

            return url, 201