rm -fr build
rm -fr dist
rm -fr pypawa.egg-info
find . -name \*.pyc -exec rm {} +
find . -name __pycache__ -exec rm -r {} +
