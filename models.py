from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Admin(db.Model):
    A_id = db.Column(db.Integer, primary_key=True)
    A_username = db.Column(db.String(64),unique= True, nullable=False)
    A_password = db.Column(db.String(128), nullable = False)

class Influencer(db.Model):
    I_id = db.Column(db.Integer, primary_key=True)
    I_username = db.Column(db.String(64), unique=True, nullable=False)
    I_password = db.Column(db.String(128), nullable=False)
    I_platform = db.Column(db.String(64), nullable=False)
    ad_inf = db.relationship('Ad_request', backref='influencer',lazy=True)
    review_I = db.relationship('Reviews', backref='influencer' ,lazy=True)
    flag_I = db.relationship('Flagged_user', backref='influencer', lazy=True,cascade='all,delete-orphan')

class Sponsor(db.Model):
    S_id = db.Column(db.Integer,primary_key=True)
    S_username = db.Column(db.String(64), unique=True, nullable=False)
    S_password = db.Column(db.String(128), nullable=False)
    S_industry = db.Column(db.String(128), nullable=False)
    review_S =db.relationship('Reviews', backref='sponsor', lazy=True,cascade='all,delete-orphan')
    campaign = db.relationship('Campaign', backref ='sponsor',lazy=True,cascade='all,delete-orphan')
    flag_s =db.relationship('Flagged_user', backref='sponsor', lazy=True,cascade='all,delete-orphan')

class Flagged_user(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    F_sponsor = db.Column(db.Integer,db.ForeignKey('sponsor.S_id'),nullable=True)
    F_influencer = db.Column(db.Integer,db.ForeignKey('influencer.I_id'),nullable=True)
    reason = db.column(db.Text)
    date_flagged = db.Column(db.Date,nullable=False)

class Campaign(db.Model):
    C_id = db.Column(db.Integer,primary_key=True)
    C_name = db.Column(db.String(64), unique=True, nullable=False)
    C_description = db.Column(db.Text)
    C_start_date = db.Column(db.Date, nullable=False)
    C_end_date = db.Column(db.Date, nullable=False)
    C_budget = db.Column(db.Float, nullable=False)
    C_visibility = db.Column(db.String(64), nullable=False)
    C_goals = db.Column(db.String(64), nullable=False)   
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.S_id'), nullable=False)
    ad_camp = db.relationship('Ad_request', backref='campaign',lazy=True,cascade='all,delete-orphan')
    

class Ad_request(db.Model):
    Ad_id = db.Column(db.Integer,primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.C_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.I_id'), nullable=False)
    messages = db.Column(db.Text, nullable=False)
    requirments = db.Column(db.Text, nullable=False)
    payement_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    
class Reviews(db.Model):
    R_id = db.Column(db.Integer,primary_key = True)
    R_sponsor = db.Column(db.Integer, db.ForeignKey('sponsor.S_id'), nullable=True)
    R_influencer = db.Column(db.Integer, db.ForeignKey('influencer.I_id'),nullable=True)
    Rating =db.Column(db.Integer, nullable=False)

