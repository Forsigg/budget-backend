# Budget App

## Setup
Requirements: Docker, any version of Python.


1. Clone repo `git clone https://github.com/Forsigg/budget-backend`

2. Create .env file `python ./scripts/create_dot_env.py` or `python3 ./scripts/create_dot_env.py`

3. Set up environment variable in env.py

4. Build app `docker-compose build`

5. Up containers `docker-compose up -d`

5. Make migrations with alembic `docker-compose exec app bash -c "alembic upgrade head"`

6. Go to http://0.0.0.0:8000/docs 