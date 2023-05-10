FROM python:3.10

# 
WORKDIR /FastAPI

# 
COPY ./requirements.txt /FastAPI/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /FastAPI/requirements.txt

# 
COPY . /FastAPI

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]