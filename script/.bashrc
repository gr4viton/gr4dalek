# aliases and functions for whole project

DALEK_BASE="/srv/dd/gr4dalek/"
rc_file='.bashrc'
DALEK_RC=$DALEK_BASE"script/"$rc_file
DALEK_COMMON_RC=$DALEK_BASE"script/common.sh"
DALEK_REQ="req/py/base.in"

. $DALEK_COMMON_RC
pipenv_install_tpr () {
    pipenv_install telepresence
}
pipenv_install_brain () {
    pipenv_install brain
    create_cv2_link
}
# export -f create_cv2_link

load_source () {
# include bashrc if it exist
    bashrc_path="$DALEK_BASE$1/script/$rc_file"
    if [ -f $bashrc_path ]; then
        . $bashrc_path & \
        echo ">> Sourced $bashrc_path"
    else
        echo ">> Not found $bashrc_path"
    fi
}

load_all_projects_rc () {
    load_source brain  
    load_source spine  
    load_source proton  
    load_source telepresence  
}

load_all_projects_rc


alias src_dalek="source $DALEK_RC"
alias vrc_dalek="vim $DALEK_RC"


diruser="/home/$USER/"
dirmux="$diruser.config/tmuxinator/"
alias mux="tmuxinator"

copy_mux_yml () {
    my="$DALEK_BASE$1/mux.yml"
    sys=$dirmux"dalek_$1.yml"
    if [ -f $my ]; then
        cp $my $sys & \
        echo "Copied $my to $sys"
    fi
}

copy_all_mux () {
    mkdir -p $dirmux
    copy_mux_yml brain
    copy_mux_yml spine
    copy_mux_yml proton  
    copy_mux_yml telepresence  
}

copy_all_mux

prefix='dalek_'
_muxdalek_start () {
    full=$prefix$1
    src_dalek
    mux start $full
}
_muxdalek_stop () {
    full=$prefix$1
    echo "stopping $full"
    mux stop $full
}
_muxdalek_re () {
    _muxdalek_stop $1
    _muxdalek_start $1
}

alias mux_tpr='_muxdalek_start telepresence'
alias mux_tpr_re='_muxdalek_re telepresence'
alias mux_brain='_muxdalek_start brain'
alias mux_brain_re='_muxdalek_re brain'


STILL_IMG="/home/pi/stream/still.jpg"
alias raspi_still="raspistill -o $STILL_IMG"

# fuckit this should be in project/script/.bashrc
# but export -f function is not working!

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

