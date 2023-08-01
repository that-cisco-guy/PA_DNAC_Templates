from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.dnac_template import DNAC_Template
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    dnac_templates = DNAC_Template.get_all()
    if not user:
        return redirect('/user/logout')
        
    return render_template('dashboard.html', user=user, dnac_templates=dnac_templates)