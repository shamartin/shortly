from . import db

class UrlModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_url = db.Column(db.Text, unique= True, nullable=False)
    short_code = db.Column(db.Text, unique= True, nullable=True)
    #future features - timestamp, usage counter, expiration

    def __repr__(self):
        return f"url(full_url = {self.full_url}, short_code = {self.short_code},)"