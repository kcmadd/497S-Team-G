# pull the Python Docker image
FROM python

# Install PDM
RUN pip install pdm

# Create the directory inside the container for the app
WORKDIR /usr/src/app

# Copy the generated modules and all other files to the container
COPY ./pyproject.toml ./
COPY ./pdm.lock ./

# Install libraries
RUN pdm install

# Copy the code into the container
COPY ./main.py ./main.py

# our app is running on port 5000 within the container, so need to expose it
EXPOSE 5003

# the command that starts our app
CMD ["pdm", "run", "start_server"]