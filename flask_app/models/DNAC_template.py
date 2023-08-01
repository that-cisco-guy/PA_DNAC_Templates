from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "dnac_template_schema"
class DNAC_Template:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.template_name = db_data['template_name']
        self.template_body = db_data['template_body']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT d.id, d.template_name, d.template_body, d.created_at, d.updated_at, d.user_id,
                    u.id as creator_id, u.first_name as creator_first_name,
                    u.last_name as creator_last_name
                FROM dnac_templates d
                JOIN users u ON d.user_id = u.id
                GROUP BY d.id, u.id;
                """
        results = connectToMySQL(db).query_db(query)
        dnac_templates = []
        for row in results:
            this_dnac_template = cls(row)
            user_data = {
                "id": row['creator_id'],
                "first_name": row['creator_first_name'],
                "last_name": row['creator_last_name'],
                "email": "",
                "password": "",
                "created_at": "",
                "updated_at": ""
            }
            this_dnac_template.creator = user.User(user_data)
            dnac_templates.append(this_dnac_template)
        return dnac_templates
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM dnac_templates
                JOIN users on dnac_templates.user_id = users.id
                WHERE dnac_templates.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_dnac_template = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_dnac_template.creator = user.User(user_data)
        return this_dnac_template

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO dnac_templates (template_name,template_body,user_id)
                VALUES (%(template_name)s,%(template_body)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)

    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE dnac_templates
                SET template_name = %(template_name)s,
                template_body = %(template_body)s,
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM dnac_templates
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_dnac_template(form_data):
        is_valid = True

        if form_data['template_name'] == '':
            flash("Please input Template Name.")
            is_valid = False
        if form_data['template_body'] == '':
            flash("Please input Template Body.")
            is_valid = False

        return is_valid