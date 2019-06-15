#!/bin/bash

rm -rf ./training-set/
rm ./debug-*.blend
mkdir ./training-set
blender ./table.blend --background --python ./generate_blender_test_data.py -- $@
