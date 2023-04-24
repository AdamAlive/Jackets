from flask_app import app
from flask_app.config.MySQLConnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

DB = "jacket"

class Jacket:
    
    def __init__(self, jacket):
        self.id = jacket["id"]
        self.back_name = jacket["back_name"]
        self.prim_color = jacket["prim_color"] 
        self.sec_color = jacket["sec_color"]
        self.size = jacket["size"]
        self.created_at = jacket["created_at"]
        self.updated_at = jacket["updated_at"]
        self.user = None

    @classmethod
    def report_valid_jacket(cls, jacket_dict):
        if not cls.is_valid(jacket_dict):
            return False
        query = """INSERT INTO jackets (back_name, prim_color, sec_color, jackets.size, user_id) VALUES 
        (%(back_name)s, %(prim_color)s, %(sec_color)s, %(size)s, %(user_id)s);"""
        jacket_id = connectToMySQL(DB).query_db(query, jacket_dict)
        jacket = cls.get_by_id(jacket_id)
        return jacket

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM jackets WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)[0]
        jacket = cls(result)
        user_obj = user.User.get_by_id(result["user_id"])
        jacket.user = user_obj
        return jacket

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO jackets (back_name,prim_color,sec_color,jackets.size,user_id)
                VALUES (%(back_name)s,%(prim_color)s,%(sec_color)s,%(size)s,%(user_id)s);
                """
        return connectToMySQL('jacket').query_db(query,form_data)


    @classmethod
    def get_all(cls):
        query = """SELECT 

                    jackets.id, jackets.created_at, jackets.updated_at, sec_color, prim_color, back_name, jackets.size, password,
                    users.id as user_id, first_name, last_name, email, users.created_at as uc, users.updated_at as uu
                    FROM jackets
                    JOIN users on users.id = jackets.user_id;"""
        jacket_data = connectToMySQL(DB).query_db(query)
        jackets = []
        for jacket in jacket_data: 
            jacket_obj = cls(jacket)
            jacket_obj.user = user.User(
                {
                    "id": jacket["user_id"],
                    "first_name": jacket["first_name"],
                    "last_name": jacket["last_name"],
                    "email": jacket["email"],
                    "created_at": jacket["uc"],
                    "password": jacket["password"],
                    "updated_at": jacket["uu"]
                }
            )
            jackets.append(jacket_obj)
        return jackets

    @classmethod
    def update_jacket(cls, jacket_dict, session_id):
    
        query = """UPDATE jackets
                    SET back_name = %(back_name)s, prim_color = %(prim_color)s, 
                    sec_color = %(sec_color)s, jackets.size = %(size)s

                    WHERE id = %(id)s;"""
        
        return connectToMySQL(DB).query_db(query,jacket_dict)



    @classmethod
    def delete_jacket_by_id(cls, jacket_id):

        data = {"id": jacket_id}
        query = "DELETE from jackets WHERE id = %(id)s;"
        connectToMySQL(DB).query_db(query,data)

        return jacket_id


    @staticmethod
    def validate_jacket(jacket_dict):
        valid = True
        flash_string = " field is required and must be at least 3 characters."
        if len(jacket_dict["back_name"]) < 3:
            flash("Name on back " + flash_string)
            valid = False
        if len(jacket_dict["prim_color"]) < 3:
            flash("Primary color " + flash_string)
            valid = False
        if len(jacket_dict["sec_color"]) < 3:
            flash("Secondary color " + flash_string)
            valid = False
        if len(jacket_dict["size"]) <= 0:
            flash("Date is required.")
            valid = False
        return valid
        