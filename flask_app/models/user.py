from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re

db = "dnac_template_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    @classmethod
    def save(cls,form_data):
        hashed_data = {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': bcrypt.generate_password_hash(form_data['password']),
        }
        query = """
                INSERT INTO users (first_name,last_name,email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                """
        return connectToMySQL(db).query_db(query,hashed_data)

    @classmethod
    def get_by_email(cls,data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        return cls(result[0])

    @classmethod
    def get_all_dnac_templates(cls, data):
        query = '''SELECT users.*, dnac_templates.*
            FROM users
            LEFT JOIN dnac_templates ON users.id = dnac_templates.user_id
            WHERE users.id = %(id)s'''
        results = connectToMySQL(db).query_db(query, data)
        if results is None:
            return None
        user = cls(results[0])
        user.dnac_template = []
        from flask_app.models.dnac_template import DNAC_Template
        for dnac_template in results:
            dnac_template_data = {
                'id': dnac_template['id'],
                'template_name': dnac_template['template_name'],
                'template_body': dnac_template['template_body'],
                'created_at': dnac_template['created_at'],
                'updated_at': dnac_template['updated_at'],
                'user_id': dnac_template['user_id'],
            }
            user.dnac_template.append(DNAC_Template(dnac_template_data))
            return user

    @staticmethod
    def validate_reg(form_data):
        is_valid = True

        if len(form_data['email']) < 1:
            flash("Email cannot be blank.","register")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address.","register")
            is_valid = False
        elif User.get_by_email(form_data):
            flash("A user already exists for that email.","register")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters long.","register")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords must match.","register")
            is_valid = False
        if len(form_data['first_name']) < 2:
            flash("First name must be at least 2 characters long.","register")
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters long.","register")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(form_data):
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email/password.","login")
            return False

        user = User.get_by_email(form_data)
        if not user:
            flash("Invalid email/password.","login")
            return False
        
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Invalid email/password.","login")
            return False
        
        return user