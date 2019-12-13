from setuptools import setup, find_packages

setup(
    name='bioker',
    version='0.1.0',
    description='Python library for REPL oriented work',
    author='Viktor Vlasov',
    author_email='viktorvlasovsiberian@gmail.com',
    install_requires=['requests', 'pandas', 'sqlalchemy', 'pika', 'redis', 'kafka-python'],
    packages=find_packages())
