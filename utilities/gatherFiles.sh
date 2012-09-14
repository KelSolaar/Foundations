#/bin/bash
echo -------------------------------------------------------------------------------
echo Foundations - Files Gathering
echo -------------------------------------------------------------------------------

export PROJECT=$( dirname "${BASH_SOURCE[0]}" )/..

export DOCUMENTATION=$PROJECT/docs/
export RELEASES=$PROJECT/releases/
export REPOSITORY=$RELEASES/repository/
export UTILITIES=$PROJECT/utilities

#! Gathering folder cleanup.
rm -rf $REPOSITORY
mkdir -p $REPOSITORY/Foundations

#! Foundations Changes gathering.
cp -rf $RELEASES/Changes.html $REPOSITORY/Foundations/

#! Foundations Manual / Help files.
cp -rf $DOCUMENTATION/help $REPOSITORY/Foundations/Help
rm $REPOSITORY/Foundations/help/Foundations_Manual.rst

#! Foundations Api files.
cp -rf $DOCUMENTATION/sphinx/build/html $REPOSITORY/Foundations/Api