from importlib.metadata import distribution


def test_installed_kivymd_resource_is_available():
    kivymd = distribution("kivymd")
    resource = kivymd.locate_file("kivymd/uix/label/label.kv")

    assert resource.is_file()
    assert sum(str(file).endswith(".kv") for file in kivymd.files or []) > 0
