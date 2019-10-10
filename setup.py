from setuptools import setup, find_packages

setup(
    name='bioker-python-repl',
    version='0.1.0',
    description='Python library for REPL oriented work',
    author='Viktor Vlasov',
    author_email='viktorvlasovsiberian@gmail.com',
    install_requires=['requests', 'pandas', 'sqlalchemy', 'pika'],
    packages=find_packages())
