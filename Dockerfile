FROM python:3.9-slim
EXPOSE 8050
RUN pip install poetry
COPY poetry.lock ./poetry.lock
COPY pyproject.toml ./pyproject.toml
RUN poetry install
COPY . ./
RUN poetry install
RUN poetry run pip install gunicorn
CMD ["poetry", "run", "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8050", "social_analysis.main_dashboard:server","dataset.csv"]