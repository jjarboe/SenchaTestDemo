#!/bin/bash

# Script to prepare the project in "Workspace" directory to be built
# This will be used to simplify running tests in a continuous integration
# environment under Jenkins

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $BASEDIR/Workspace
python update-ext.py 6.0.3.21 ext

if [ -d /opt/Sencha -a ! -e "$HOME/bin" ]; then
    ln -s /opt "$HOME/bin"
fi
