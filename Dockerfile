FROM python:3.8

WORKDIR /app

# install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# add project files *after* dependencies to speed up building image
# project files are updated more often than dependencies
COPY . .

CMD ["uvicorn", "main:app"]
