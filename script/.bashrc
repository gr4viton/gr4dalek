# aliases and functions for whole project

DALEK_BASE="/srv/dd/gr4dalek/"
rc_file='.bashrc'
DALEK_RC=$DALEK_BASE"script/"$rc_file
DALEK_COMMON_RC=$DALEK_BASE"script/common.sh"
DALEK_REQ="req/py/base.in"


load_source () {
# include bashrc if it exist
    bashrc_path="$1/script/$rc_file"
    if [ -f $bashrc_path ]; then
        . $bashrc_path
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
