from setuptools import setup, find_packages

setup(
    name='pybioker',
    version='0.1.0',
    description='Personal Python Library',
    author='Viktor Vlasov',
    author_email='viktorvlasovsiberian@gmail.com',
    install_requires=['ipython', 'requests', 'lxml', 'beautifulsoup4', 'jsonpath-ng', 'pymysql', 'sqlalchemy', 'numpy',
                      'pandas', 'html5lib', 'matplotlib', 'selenium', 'pika', 'redis', 'pymongo', 'grpcio',
                      'grpcio-tools', 'kafka-python', 'elasticsearch'],
    packages=find_packages())
