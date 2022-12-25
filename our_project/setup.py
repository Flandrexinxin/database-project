from setuptools import find_packages, setup

setup(
    name='project',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask','functools','werkzeug.utils','werkzeug.security','mysql.connector','string','random','csv','pandas','datetime','os'
    ],
)