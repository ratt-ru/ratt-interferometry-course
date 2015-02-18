#!/bin/sh

docker run -ti -p 8888:8888 -v `pwd`:/notebooks radioastro/notebook
