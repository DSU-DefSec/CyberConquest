#!/bin/sh

gcc buzzzt.c -o buzzzt.exe.v0
objcopy buzzzt.exe.v0 buzzzt.exe.v1 -XxSg --strip-unneeded
objcopy buzzzt.exe.v1 buzzzt.exe.v2 -R .note*
objcopy buzzzt.exe.v2 buzzzt.exe -R .comment

rm buzzzt.exe.v0 buzzzt.exe.v1 buzzzt.exe.v2