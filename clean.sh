rm -fr build
rm -fr dist
rm -fr bioker_python_repl.egg-info
find . -name \*.pyc -exec rm {} +
find . -name __pycache__ -exec rm -r {} +
