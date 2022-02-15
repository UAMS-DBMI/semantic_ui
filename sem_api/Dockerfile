FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install requests

COPY ./app /app

EXPOSE 3000
CMD ["uvicorn", "semantic-api:app", "--host", "0.0.0.0", "--port", "3000"]
