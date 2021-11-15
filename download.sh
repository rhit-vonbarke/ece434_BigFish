#!/bin/bash

sudo youtube-dl -x --audio-format wav -o $PWD'/audiodownloads/%(id)s.%(ext)s' $1

