import re
from build.create_methods import Parser
from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

with open("tg_api/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()


parser = Parser()


setup(
name="Bot api base",
version=version,
description="This repo is a small-library, or rather a base used to build a telegram client. It is developed in python3 and comes with filters and is super simple to use.",
long_description=readme,
long_description_content_type="text/markdown",
url="https://github.com/Skammato/Base-for-bot_api.git",
download_url="https://github.com/pyrogram/pyrogram/releases/latest",
author="Skammato",
author_email="Skammatoontg@gmail.com",
keywords="telegram bot chat api library python",
python_requires="~=3.9",
package_data={
    "tg_api": ["py.typed"],
},
packages=find_packages(exclude=["build*"]),
zip_safe=False,
install_requires=requires
)

create_
