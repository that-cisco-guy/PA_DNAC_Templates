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

@app.route('/dnac_template/new')
def create_dnac_template():
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('new_dnac_template.html')

@app.route('/dnac_template/new/process', methods=['POST'])
def process_dnac_template():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not DNAC_Template.validate_dnac_template(request.form):
        return redirect('/dnac_template/new')

    data = {
        'user_id': session['user_id'],
        'template_name': request.form['template_name'],
        'template_body': request.form['template_body'],
    }
    DNAC_Template.save(data)
    return redirect('/dashboard')

@app.route('/dnac_template/<int:id>')
def view_dnac_template(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('view_dnac_template.html',dnac_template=DNAC_Template.get_by_id({'id': id}))

@app.route('/dnac_template/edit/<int:id>')
def edit_dnac_template(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('edit_dnac_template.html',dnac_template=DNAC_Template.get_by_id({'id': id}))

@app.route('/dnac_template/edit/process/<int:id>', methods=['POST'])
def process_edit_dnac_template(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not DNAC_Template.validate_dnac_template(request.form):
        return redirect(f'/dnac_template/edit/{id}')

    data = {
        'id': id,
        'template_name': request.form['template_name'],
        'template_body': request.form['template_body'],
    }
    DNAC_Template.update(data)
    return redirect('/dashboard')

@app.route('/dnac_template/destroy/<int:id>')
def destroy_dnac_template(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    DNAC_Template.destroy({'id':id})
    return redirect('/dashboard')