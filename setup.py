from setuptools import find_packages, setup

setup(
    name='tasks_manager',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'flask_sqlalchemy',
        "flask-migrate",
        'flask-cors',
        'pytest',
        'coverage'
    ],
)
