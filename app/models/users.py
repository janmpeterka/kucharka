from flask_security.models.fsqla_v2 import FsUserMixin as UserMixin

from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class User(BaseModel, BaseMixin, UserMixin):
    from app.models.users_have_roles import users_have_roles

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    full_name = db.Column(db.String(255))

    roles = db.relationship("Role", secondary="users_have_roles", backref="users")

    daily_plans = db.relationship("DailyPlan", back_populates="author")

    recipes = db.relationship("Recipe", order_by="Recipe.name", back_populates="author")

    events = db.relationship("Event", back_populates="author")

    # PROPERTIES

    @property
    def name(self):
        if self.full_name:
            return self.full_name
        else:
            return ""

    @property
    def active_events(self):
        return [e for e in self.events if e.is_active]

    @property
    def closest_event(self):
        if not self.active_events:
            return None
        else:
            closest_event = self.active_events[0]
            for event in self.active_events:
                if event.date_from > closest_event.date_from:
                    closest_event = event

            return closest_event

    @property
    def archived_events(self):
        return [e for e in self.events if e.is_archived]

    @property
    def visible_recipes(self):
        return [r for r in self.recipes if r.is_visible]

    @property
    def draft_recipes(self):
        # import time
        # time.sleep(3)
        return [r for r in self.recipes if r.is_draft]

    @property
    def recipes_with_zero_amount(self):
        return [r for r in self.recipes if r.has_zero_amount_ingredient]

    @property
    def recipes_without_category(self):
        return [i for i in self.recipes if i.without_category]

    @property
    def personal_ingredients(self):
        return [i for i in self.ingredients if not i.is_public]

    @property
    def ingredients_without_category(self):
        return [i for i in self.personal_ingredients if i.without_category]

    @property
    def ingredients_without_measurement(self):
        return [i for i in self.personal_ingredients if i.without_measurement]

    # ROLES
    @property
    def is_admin(self):
        return self.has_role("admin")

    @property
    def is_application_manager(self):
        return self.has_role("application_manager")
