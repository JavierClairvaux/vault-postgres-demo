#!/bin/bash

/bin/vault agent -config=/app/agent-config.hcl -config=/app/agent-template.hcl

/bin/python3 /app/app.py