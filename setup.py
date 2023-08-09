from setuptools import setup, find_packages

setup(
    name="quality-measure-engine",
    version="0.1.0",
    description="A library for extracting quality measure information from HITSP C32's and ASTM CCR's",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Marc Hadley, Andy Gregorowicz",
    author_email="talk@projectpophealth.org",
    url="http://github.com/pophealth/quality-measure-engine",
    packages=find_packages(),
    package_data={
        '': ['*.json', '*.rb', '*.md'],
    },
    install_requires=[
        "mongo==1.1",
        "mongomatic==0.5.8",
        "therubyracer==0.7.5",
        "bson_ext==1.1.1",
    ],
    extras_require={
        "dev": [
            "jsonschema==2.0.0",
            "rspec==2.0.0",
            "awesome_print==0.2.1",
            "jeweler==1.4.0",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ]
)
