"""Menu-related utility functions."""

from collections.abc import Callable
from typing import TypeVar

MenuItemT = TypeVar("MenuItemT")


def create_menu_item(
    menu_item_factory: Callable[..., MenuItemT],
    name: str,
    label: str,
    tip: str,
    icon: str,
) -> MenuItemT:
    """Create one menu item with the supplied factory."""

    return menu_item_factory(
        name=name,
        label=label,
        tip=tip,
        icon=icon,
    )
