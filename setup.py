from setuptools import setup

APP = ["main.py"]
DATA_FILES = ["static"]  # Si vous avez des fichiers de ressources, les spécifier ici
OPTIONS = {
    # "packages": ["PyQt5", "ui"],  # Liste des packages à inclure
    "iconfile": "static/icon.icns",  # Votre icône d'application
    "includes": ["Common"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
