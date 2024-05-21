#
# This script runs the tests in all supported python versions.
#
# You are required to have pyenv installed, the included devcontainer has pyenv
# preinstalled for convenience.
#

# need to use a map
py3_12_flask_versions=("3.0" "2.3" "2.2" "2.1" "2.0")
py3_11_flask_versions=("3.0" "2.3" "2.2" "2.1" "2.0")
py3_10_flask_versions=("3.0" "2.3" "2.2" "2.1" "2.0")
py3_9_flask_versions=("3.0" "2.3" "2.2" "2.1" "2.0")
py3_8_flask_versions=("3.0" "2.3" "2.2" "2.1" "2.0")
py3_7_flask_versions=("2.2" "2.1" "2.0")
py_versions=("3.12" "3.11" "3.10" "3.9" "3.8" "3.7")

# install python versions
for py_ver in ${py_versions[@]}
do
    echo "Installing python $py_ver..."
    pyenv install $py_ver --skip-existing
done

# generate virtualenvs
for py_ver in ${py_versions[@]}
do
    # get list of flask versions compatible with this python version
    py_ver_underscore=$(echo $py_ver | tr . _)
    flask_versions_var_name="py${py_ver_underscore}_flask_versions[@]"

    for flask_ver in ${!flask_versions_var_name}
    do
        if test -d .virtualenv-py$py_ver-flask$flask_ver
        then
            echo "Skipping .virtualenv-py$py_ver-flask$flask_ver because it already exists"
        else
            echo "Building .virtualenv-py$py_ver-flask$flask_ver..."
            pyenv global $py_ver
            python -m venv .virtualenv-py$py_ver-flask$flask_ver/
            .virtualenv-py$py_ver-flask$flask_ver/bin/pip install flask==$flask_ver.*
            .virtualenv-py$py_ver-flask$flask_ver/bin/pip install -r requirements-dev.txt
            .virtualenv-py$py_ver-flask$flask_ver/bin/pip install -e .
        fi
    done
done

# run tests
for ver in ${py_versions[@]}
do
    # get list of flask versions compatible with this python version
    py_ver_underscore=$(echo $py_ver | tr . _)
    flask_versions_var_name="py${py_ver_underscore}_flask_versions[@]"

    for flask_ver in ${!flask_versions_var_name}
    do
        echo "running tests for python $ver and flask $flask_ver"
        .virtualenv-py$py_ver-flask$flask_ver/bin/python -m pytest flask_parameters/
    done
done
