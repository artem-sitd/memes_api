#!/bin/bash
set -e

# Apply Alembic migrations
alembic upgrade head
