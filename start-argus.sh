#!/bin/bash
source bin/activate
cd src/argus/
celery -A tasks worker --loglevel=info
