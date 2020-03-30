from setuptools import setup, find_packages

setup(
    name='pybioker',
    version='0.1.0',
    description='Personal Python Library',
    author='Viktor Vlasov',
    author_email='viktorvlasovsiberian@gmail.com',
    install_requires=['requests', 'pandas', 'sqlalchemy', 'pika', 'redis', 'kafka-python', 'elasticsearch'],
    packages=find_packages())
