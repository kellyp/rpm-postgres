#!/bin/bash
# Volker Fröhlich
VERSION="1.9.2"

tar xvfz gdal-"${VERSION}".tar.gz

mv gdal-"${VERSION}"{,-fedora} && pushd gdal-"${VERSION}"-fedora

rm data/cubewerx_extra.wkt
rm data/esri_extra.wkt
rm data/esri_Wisconsin_extra.wkt
rm data/esri_StatePlane_extra.wkt
rm data/ecw_cs.wkt

rm -r frmts/bsb

#Really necessary?
rm -r swig/php

popd


#TODO: Insert Provenance file

tar cvfz gdal-"${VERSION}"-fedora.tar.gz gdal-"${VERSION}"-fedora
