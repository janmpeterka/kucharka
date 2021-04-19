from .dashboard import DashboardView
from .index import IndexView
from .ingredients import IngredientsView

__all__ = [
    "DashboardView",
    "IndexView",
    "IngredientsView",
    # "UsersView",
]


def register_all_controllers(application):
    # AdminView.register(application)
    # CookbookView.register(application)
    # DailyPlansView.register(application)
    DashboardView.register(application)
    # ErrorsView.register(application)
    # FilesView.register(application)
    IndexView.register(application)
    IngredientsView.register(application)
    # RecipesView.register(application)
    # SupportView.register(application)
    # UsersView.register(application)


# def register_error_handlers(application):
#     from .errors import error404
#     from .errors import error405
#     from .errors import error500

#     application.register_error_handler(403, error404)
#     application.register_error_handler(404, error404)
#     application.register_error_handler(405, error405)
#     application.register_error_handler(500, error500)
