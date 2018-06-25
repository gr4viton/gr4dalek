#!/bin/bash
# aliases and functions for this subproject

. $DALEK_COMMON_RC

create_cv2_link () {
    echo "Getting pipenv venv folder"
    pipenv_lib=$(pipenv --venv)"/lib/"
    lib_path=$(ag -g 'cv2.so' -- /usr/local)
    pipenv_python=$(ls $pipenv_lib | grep python)
    echo "Check if the py3 version with which the opencv library was compiled = "$lib_path" - is the same as the one in venv = "$pipenv_python

    echo "you have to use the same python version for the virtualenv and the cv2 compiling"

    venv_lib_path=$pipenv_lib"/"$pipenv_python"/site-packages/cv2.so"

    echo "creating symbolic link of $lib_path in $venv_lib_path"
    ln -s $lib_path $venv_lib_path
}

export -f create_cv2_link
