from flask import abort, flash, request, redirect, url_for, jsonify
from flask import render_template as template

from flask_classful import route
from flask_login import login_required, current_user

# from app.auth import admin_required
from app.helpers.form import create_form, save_form_to_session
from app.helpers.extended_flask_view import ExtendedFlaskView

# from app.handlers.data import DataHandler

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe
from app.controllers.forms.ingredients import IngredientsForm


class IngredientsView(ExtendedFlaskView):
    decorators = [login_required]

    def before_request(self, name, id=None, *args, **kwargs):
        super().before_request(name, id, *args, **kwargs)

        if id is not None:
            if self.ingredient is None:
                abort(404)
            if not self.ingredient.can_current_user_view:
                abort(403)

    def before_edit(self, id):
        super().before_edit(id)
        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_show(self, id):
        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        # self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_index(self):
        self.ingredients = current_user.ingredients

    def post(self):
        form = IngredientsForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:new"))

        ingredient = Ingredient(author=current_user)
        form.populate_obj(ingredient)

        if ingredient.save():
            return redirect(url_for("IngredientsView:show", id=ingredient.id))
        else:
            flash("Nepodařilo se vytvořit surovinu", "error")
            return redirect(url_for("IngredientsView:new"))

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        if not self.ingredient.is_used:
            self.ingredient.remove()
            flash("Surovina byla smazána", "success")
            return redirect(url_for("DashboardView:show"))
        else:
            flash("Tato surovina je použita, nelze smazat", "error")
            return redirect(url_for("IngredientsView:show", id=self.ingredient.id))
