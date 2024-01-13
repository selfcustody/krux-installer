"""
constants.py

Some constants to be used accros application
"""

import os
import tomllib
from typing import Any

ROOT_DIRNAME = os.path.abspath(os.path.dirname(__file__)) 


def _open_pyproject() -> dict[str, Any]:
    """
    Open root pyprojet.toml file to get some constant datas
    like name, version and description
    """
    try:
        pyproject_filename = os.path.abspath(os.path.join(ROOT_DIRNAME, "..", "..", "pyproject.toml"))
        with open(pyproject_filename, "r") as pyproject_file:
            data = pyproject_file.read()
            return tomllib.loads(data)
    except ValueError:
        raise ValueError(f'{pyproject_filename} is not valid toml file')

   
def get_name() -> str:
    """
    Get project name defined in pyproject.toml
    """
    return _open_pyproject()["tool"]["poetry"]["name"]


def get_version() -> str:
    """
    Get project version defined in pyproject.toml
    """
    return _open_pyproject()["tool"]["poetry"]["version"]


def get_description() -> str:
    """
    Get project description defined in pyproject.toml
    """
    return _open_pyproject()["tool"]["poetry"]["description"]
