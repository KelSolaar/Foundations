#/bin/bash
echo -------------------------------------------------------------------------------
echo Foundations - Files Gathering
echo -------------------------------------------------------------------------------

export PROJECT_DIRECTORY=$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)

export DOCUMENTATION_DIRECTORY=$PROJECT_DIRECTORY/docs/
export RELEASES_DIRECTORY=$PROJECT_DIRECTORY/releases/
export REPOSITORY_DIRECTORY=$RELEASES_DIRECTORY/repository/
export UTILITIES_DIRECTORY=$PROJECT_DIRECTORY/utilities

#! Gathering folder cleanup.
rm -rf $REPOSITORY_DIRECTORY
mkdir -p $REPOSITORY_DIRECTORY/Foundations

#! Foundations Changes gathering.
cp -rf $RELEASES_DIRECTORY/Changes.html $REPOSITORY_DIRECTORY/Foundations/

#! Foundations Manual / Help files.
cp -rf $DOCUMENTATION_DIRECTORY/help $REPOSITORY_DIRECTORY/Foundations/Help
rm $REPOSITORY_DIRECTORY/Foundations/help/Foundations_Manual.rst

#! Foundations Api files.
cp -rf $DOCUMENTATION_DIRECTORY/sphinx/build/html $REPOSITORY_DIRECTORY/Foundations/Api