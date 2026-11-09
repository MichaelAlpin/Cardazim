from pathlib import Path

from setuptools import find_packages, setup

REQUIREMENTS_FILE = Path(".") / "requirements.txt"


def _read_requirements(file: Path) -> list[str]:
    with open(file) as req_file:
        lines = req_file.readlines()
    return [line.rstrip() for line in lines]


setup(
    name="cardazim",
    version="0.0.1",
    author="Michael",
    author_email="misha.alpin@gmail.com",
    description="The Cardazim project!",
    long_description="""The classic Cardazim card game
    """,
    packages=find_packages("cardazim"),
    install_requires=_read_requirements(REQUIREMENTS_FILE),
)
