#!/bin/bash

if [[ -e .vagrant_local ]]; then
    mv .vagrant .vagrant_digi
    mv .vagrant_local .vagrant
else
    mv .vagrant .vagrant_local
    mv .vagrant_digi .vagrant
fi
