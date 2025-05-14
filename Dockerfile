FROM python:3.10-slim

WORKDIR /app
COPY task_manager.py .
COPY templates/ templates/
COPY static/ static/

RUN pip install flask pymongo

EXPOSE 5001
CMD ["python", "task_manager.py"]

