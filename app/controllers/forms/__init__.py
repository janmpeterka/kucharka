# This is needed for ExtendedFlaskView to automatically import all Form classes

from .ingredients import IngredientsForm  # noqa: F401

__all__ = [
    "IngredientsForm",
]
