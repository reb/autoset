#!/bin/bash

blender ./table.blend --background --python ./generate_blender_test_data.py -- $@
