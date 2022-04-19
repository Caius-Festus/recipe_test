from flask import render_template, request, redirect, session
from flask_app import app, flash
from flask_app.models.recipe import Recipe

@app.route("/recipes/<recipe_id>")
def recipes(recipe_id):
    data = {
        "recipe_id" : recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template("/show_recipe.html", recipe=recipe)

@app.route("/recipes/new")
def recipes_form():
    if "user_id" not in session:
        return redirect("/")
    return render_template("/create_recipe.html")

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect("/")
    # check if input is valid, if not redirect to form with flash messages
    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    # enter info into database
    Recipe.create_recipe(request.form)
    return redirect("/dashboard")

@app.route("/recipes/edit/<recipe_id>")
def edit_recipe_form(recipe_id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "recipe_id" : recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template("/edit_recipe.html", recipe=recipe)

@app.route("/edit_recipe", methods=["POST"])
def edit_post():
    if "user_id" not in session:
        return redirect("/")
    # check if input is valid, if not redirect to form with flash messages
    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/edit/%s" %(request.form["recipe_id"]))
    # enter info into database
    Recipe.edit_recipe(request.form)
    return redirect("/dashboard")