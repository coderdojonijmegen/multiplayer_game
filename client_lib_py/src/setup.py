import os

from setuptools import setup, find_packages

VERSION = f"1.0.{os.environ.get('build_number', '0')}"
DESCRIPTION = "mqtt_app: base for mqtt apps"
LONG_DESCRIPTION = "mqtt_app: base for mqtt apps listening and publishing to topics"

setup(
    name="mqtt_app",
    version=VERSION,
    author="Bas Hopman",
    author_email="<bas@familiehopman.net>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["paho-mqtt", "pyaml"],
    keywords=[],
    classifiers=[],
)
