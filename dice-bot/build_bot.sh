#!/bin/bash
pip -m venv env
cd env
source bin/activate
pip install -r ../requirements.txt
cd ..
