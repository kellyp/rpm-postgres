#!/bin/sh

/usr/lib/rpm/perl.req $* | grep -v 'perl(Pg'|grep -v PGLIBDIR|grep -v log

