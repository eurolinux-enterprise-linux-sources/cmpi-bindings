#!/bin/sh

##
## Check usage
##

if [ "$#" != 1 ]; then
    echo "Usage: $0 [op|sfcb]"
    exit 1
fi

if [ "$1" != "op" -a "$1" != "sfcb" ]; then
    echo "Usage: $0 [op|sfcb]"
    exit 1
fi

##
## Install python provider infrastructure implementation.
##

PKGS=/usr/lib64/python2.5/site-packages
echo "cp ./build/swig/python/cmpi.py $PKGS"
cp ./build/swig/python/cmpi.py $PKGS
echo "cp ./swig/python/cim_provider.py $PKGS"
cp ./swig/python/cim_provider.py $PKGS
echo "cp ./swig/python/cmpi_pywbem_bindings.py $PKGS"
cp ./swig/python/cmpi_pywbem_bindings.py $PKGS

##
## Install provider shared library.
##

SO=./build/swig/python/libpyCmpiProvider.so

if [ ! -f "$SO" ]; then
    echo "$0: no such file: $SO"
    exit 1
fi

PEGASUS_PROVIDER_DIR=$PEGASUS_HOME/lib

if [ "$1" = "op" ]; then
    if [ ! -d "$PEGASUS_PROVIDER_DIR" ]; then
        echo "Please define PEGASUS_PROVIDER_DIR"
    fi
    echo "cp $SO $PEGASUS_PROVIDER_DIR"
    cp $SO $PEGASUS_PROVIDER_DIR
fi

if [ "$1" = "sfcb" ]; then
    echo "cp $SO /usr/lib64/"
    cp $SO /usr/lib64/
fi
