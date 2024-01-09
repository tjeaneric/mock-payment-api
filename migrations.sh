!/bin/bash

alembic revision --autogenerate  -m "Add changes"
alembic upgrade head