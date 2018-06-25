
if [ -z "$DALEK_BASE" ]; then
    echo "DALEK_BASE env must be set!"
    exit 1
fi

pipenv_install () {
    proj_path="$DALEK_BASE$1/"
    cd $proj_path
    pwd
    echo ">> using these requirements from $proj_path$DALEK_REQ"
    cat $proj_path$DALEK_REQ
    echo ">> starting to install $1 subproject via pipenv - this can take some time"
    pipenv install --skip-lock --three -r $proj_path$DALEK_REQ
}
