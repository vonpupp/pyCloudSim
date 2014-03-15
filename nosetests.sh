#!/bin/sh

#nosetests --nocapture $1

nosetests --ipdb $1
#nosetests --ipdb-failure $1
