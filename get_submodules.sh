#!/bin/sh

#http://stackoverflow.com/questions/15844542/git-symlink-reference-to-a-file-in-an-external-repository/27770463#27770463

#curl?
#curl -o py -O https://bitbucket.org/gr4viton/kivycv/raw/4a3f85a5702445cdba096f3164d7bfde867a4ba0/StepEnum.py 

#git archive
git archive --remote=https://gr4viton@bitbucket.org/gr4viton/kivycv.git HEAD:StepEnum.py --format=tar | tar -x
