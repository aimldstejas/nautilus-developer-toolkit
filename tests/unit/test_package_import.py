"""Basic smoke tests for the Version 2 package."""


def test_package_imports() -> None:
    import nautilus_developer_toolkit

    assert nautilus_developer_toolkit is not None


def test_exception_hierarchy_imports() -> None:
    from nautilus_developer_toolkit.exceptions import NDTError

    assert issubclass(NDTError, Exception)
