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