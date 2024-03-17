#
# This script runs the tests in all supported python versions.
#
# You are required to have pyenv installed, the included devcontainer has pyenv
# preinstalled for convenience.
#

versions=("3.12" "3.11" "3.10" "3.9" "3.8" "3.7")

# install python versions
for ver in ${versions[@]}
do
    echo "install python version $ver"
    pyenv install $ver --skip-existing
done

# generate virtualenvs
for ver in ${versions[@]}
do
    if test -d .virtualenv-$ver
    then
        echo "skipping .virtualenv-$ver because it already exists"
    else
        echo "building .virtualenv-$ver..."
        pyenv global $ver
        python -m venv .virtualenv-$ver/
        .virtualenv-$ver/bin/pip install -r requirements.txt
        .virtualenv-$ver/bin/pip install -r requirements-dev.txt
        .virtualenv-$ver/bin/pip install -e .
    fi
done

# run tests
for ver in ${versions[@]}
do
    echo "running tests for python $ver"
    .virtualenv-$ver/bin/python -m pytest flask_parameters/
done
