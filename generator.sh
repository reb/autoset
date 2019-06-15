#!/bin/bash

rm ./debug-*.blend
mkdir -p ./training-set
rm training-set/*.jpg
xdg-open preview.html
blender ./table.blend --background --python ./generate_blender_test_data.py -- $@
