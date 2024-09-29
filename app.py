from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from models import db, Admin, Influencer, Sponsor, Campaign, Ad_request

app = Flask(__name__)
app.secret_key="secret"

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/",methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    
    elif request.method=='POST':
        username=request.form['user_name']
        password=request.form['pswd']
        I = Influencer.query.filter_by(I_username=username).first()
        S = Sponsor.query.filter_by(S_username=username).first()

        if I:
            if I.I_username == username and I.I_password==password:
                return redirect(url_for('inf_profile',influencer=I))
            else:
                return redirect(url_for('login'))
        if S:
            if S.S_username == username and S.S_password==password:
                return redirect(url_for('spon_profile',S_username=S.S_username))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

@app.route("/influencer_reg",methods=['GET','POST'])
def influencer():
    if request.method =='POST':
        username_I = request.form['user_name']
        password_I = request.form['pswd']
        platform = request.form['presence']

        new_influencer = Influencer(I_username=username_I, I_password=password_I ,I_platform=platform)
        db.session.add(new_influencer)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("influencer_reg.html")

@app.route("/sponsor_reg",methods=['GET','POST'])
def sponsor():
    if request.method =='POST':
        username_S = request.form['user_name']
        password_S = request.form['pswd']
        industry_S = request.form['industry']

        new_sponsor = Sponsor(S_username=username_S, S_password=password_S, S_industry =industry_S)
        db.session.add(new_sponsor)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template("sponsor_reg.html")

@app.route("/admin",methods=['GET','POST'])
def admin():
    if request.method =='POST':
        new_ad = Admin(A_username="Sumesha", A_password="admin123")
        db.session.add(new_ad)
        db.session.commit()

    return render_template("admin.html")

@app.route("/admin_info")
def admin_info():
    return render_template("admin_info.html")

@app.route("/admin_find")
def admin_find():
    spon = Sponsor.query.all()
    inf = Influencer.query.all()
    return render_template("admin_find.html",Influencer=inf,sponsors=spon)

@app.route("/inf_profile")
def inf_profile():
    return render_template("inf_profile.html")

@app.route("/inf_find")
def inf_find():
    return render_template("inf_find.html")

@app.route("/spon_profile/<S_username>",methods=['GET'])
def spon_profile(S_username):
    sponsor = Sponsor.query.filter_by(S_username=S_username).first()
    S = Sponsor.query.filter_by(S_username=S_username).first()
    return render_template("spon_profile.html",sponsor=S)

@app.route("/spon_find")
def spon_find():
    return render_template("spon_find.html")

@app.route("/spon_campaign/<int:S_id>",methods=['GET'])
def spon_campaign(S_id):
    # username = request.args.get('S_username')
    sponsor = Sponsor.query.filter_by(S_id=S_id).first()
    camp = Campaign.query.filter_by(sponsor_id=S_id).all()
    return render_template("spon_campaign.html",campaigns=camp,sponsor=sponsor,S_id=S_id)

@app.route("/campaigns_1/<int:S_id>",methods=['GET','POST'])
def campaigns_1(S_id):
    if request.method =='POST':
        name_c = request.form['title']
        description_c = request.form['description']
        budget_c = request.form['budget']
        s_date = datetime.strptime(request.form['start'], '%Y-%m-%d').date()
        e_date = datetime.strptime(request.form['end'], '%Y-%m-%d').date()
        goal_c = request.form['goals']
        visible =request.form['visibility']
        id=S_id

        new_camp = Campaign(C_name = name_c, C_description=description_c, C_budget = budget_c,
                            C_start_date = s_date,C_end_date = e_date, C_visibility = visible,
                            C_goals=goal_c,sponsor_id=id)
        db.session.add(new_camp)
        db.session.commit()
        return redirect(url_for('spon_campaign',S_id=S_id))

    return render_template("campaigns_1.html",S_id=S_id)

@app.route("/campaigns_2/<int:C_id>",methods=['GET'])
def campaigns_2(C_id):
    camp = Campaign.query.filter_by(C_id=C_id).first()
    
    return render_template("campaigns_2.html",campaign=camp)

@app.route("/campaigns/<int:C_id>/<int:S_id>", methods=['POST','GET'])
def delete_campaign(C_id,S_id):
    camp = Campaign.query.filter_by(C_id=C_id).first()
    db.session.delete(camp)
    db.session.commit()
    return redirect(url_for('spon_campaign',S_id=S_id))

'''@app.route("/campaigns_3/<int:C_id>", methods=['POST','GET'])
def campaigns_3():
    camp = Campaign.query.filter_by(C_id=C_id).first()
    return render_template("campaigns_3.html",campaigns=camp)'''

@app.route("/status")
def status():
    return render_template("status.html")

@app.route("/view_sponsor",methods=['GET'])
def view_sponsor():
    spon = Sponsor.query.all()
    return render_template("view_sponsor.html",sponsor=spon)

if __name__=="__main__":
    app.run(debug=True)