#!/bin/bash
source bin/activate
cd src/argus/
celery -A tasks call tasks.run_agent --args='[["'"$1"'"]]'
