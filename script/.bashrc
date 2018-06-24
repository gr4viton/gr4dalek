# aliases and functions for whole project

DALEK_BASE="/srv/dd/gr4dalek/"
rc_file='.bashrc'
DALEK_RC=$DALEK_BASE"script/"$rc_file
DALEK_COMMON_RC=$DALEK_BASE"script/common.sh"
DALEK_REQ="req/py/base.in"

. $DALEK_COMMON_RC
pipenv_install_telepresence () {
    pipenv_install telepresence
}

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
alias mux_telepresence="src_dalek; mux start $prefix""telepresence"
alias mux_telepresence_stop="echo 'stopping mux'; mux stop $prefix""telepresence"
alias mux_telepresence_re="mux_telepresence_stop; mux_telepresence"
alias mux_telepresence_debug="mux debug $prefix""telepresence"
