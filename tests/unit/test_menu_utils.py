"""Tests for menu utility functions."""

import importlib
import sys
from types import ModuleType
from typing import Any

import pytest

from nautilus_developer_toolkit.utils.menu_utils import create_menu_item


def test_create_menu_item_passes_exact_factory_arguments_and_returns_item() -> None:
    created_item = object()
    received: dict[str, object] = {}

    def factory(**kwargs: object) -> object:
        received.update(kwargs)
        return created_item

    result = create_menu_item(
        factory,
        "nautilus-developer-toolkit::open-terminal",
        "Open Terminal",
        "Open a terminal here",
        "utilities-terminal",
    )

    assert result is created_item
    assert received == {
        "name": "nautilus-developer-toolkit::open-terminal",
        "label": "Open Terminal",
        "tip": "Open a terminal here",
        "icon": "utilities-terminal",
    }


def test_create_menu_item_propagates_factory_exceptions() -> None:
    class FactoryError(Exception):
        pass

    def factory(**kwargs: object) -> object:
        raise FactoryError("factory failed")

    with pytest.raises(FactoryError, match="factory failed"):
        create_menu_item(factory, "item", "Label", "Tip", "icon")


def test_create_menu_item_wrapper_delegates_with_nautilus_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gi_module: Any = ModuleType("gi")

    def require_version(namespace: str, version: str) -> None:
        return None

    gi_module.require_version = require_version
    repository_module: Any = ModuleType("gi.repository")

    class FakeGObject:
        class GObject:
            pass

    class FakeNautilus:
        class FileInfo:
            pass

        class Menu:
            pass

        class MenuProvider:
            pass

        class MenuItem:
            pass

    repository_module.GObject = FakeGObject
    repository_module.Nautilus = FakeNautilus
    monkeypatch.setitem(sys.modules, "gi", gi_module)
    monkeypatch.setitem(sys.modules, "gi.repository", repository_module)
    monkeypatch.delitem(sys.modules, "developer_context_menu", raising=False)
    context_menu_module = importlib.import_module("developer_context_menu")

    expected_item = object()
    received: dict[str, Any] = {}

    def fake_build_menu_item(
        menu_item_factory: object,
        name: str,
        label: str,
        tip: str,
        icon: str,
    ) -> object:
        received.update(
            factory=menu_item_factory,
            name=name,
            label=label,
            tip=tip,
            icon=icon,
        )
        return expected_item

    monkeypatch.setattr(context_menu_module, "build_menu_item", fake_build_menu_item)

    result = context_menu_module.DeveloperContextMenu.create_menu_item(
        "item",
        "Label",
        "Tip",
        "icon",
    )

    assert result is expected_item
    assert received == {
        "factory": context_menu_module.Nautilus.MenuItem,
        "name": "item",
        "label": "Label",
        "tip": "Tip",
        "icon": "icon",
    }
