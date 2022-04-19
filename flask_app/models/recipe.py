from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re

DATABASE = "recipes"

class Recipe:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.cook_time = data['cook_time']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.under_thirty = data['under_thirty']
        self.liked_by = []

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(recipe_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)[0]
        return results

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, created_at, updated_at, user_id, under_thirty) VALUES (%(name)s, %(description)s, %(instructions)s, NOW(), NOW(), %(user_id)s, %(under_thirty)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, created_at=%(created_at)s, updated_at=NOW(), under_thirty=%(under_thirty)s WHERE id = %(recipe_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        for piece in data:
            print(data[piece])
            if not data[piece]:
                flash("All fields are required")
                is_valid = False
                break
            if piece == "name" and len(data[piece]) < 3:
                flash("name must be at least 3 character long")
                is_valid = False
            if piece == "description" and len(data[piece]) < 3:
                flash("description must be at least 3 character long")
                is_valid = False
            if piece == "instructions" and len(data[piece]) < 3:
                flash("instructions must be at least 3 character long")
                is_valid = False
        return is_valid

    