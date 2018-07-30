from setuptools import find_packages, setup

setup(
    name='requests_manager',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'flask_sqlalchemy',
        "flask-migrate",
        'pytest',
        'coverage'
    ],
)
