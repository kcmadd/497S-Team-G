# Creating an API App

This is a short example on how to create a Python HTTP app server using FastAPI and Docker.

# Prerequisites

1. This activity assumes you already have Docker installed and have tested to make sure it works.
2. You know how to use the command line on your platform (e.g., Linux, Mac, Windows).
3. You have already seen how to run the default Nginx container.
4. You have already seen how to use volumes.
5. You have already seen how to create a custom Docker image.
5. You are not afraid to explore!

# Overview

There are so many ways to create HTTP servers in a variety of programming languages. This example will use the Python language and the [FastAPI](https://fastapi.tiangolo.com) package to demonstrate how to write a *very* simple API server that runs inside of docker. We will be using [PDM](https://pdm.fming.dev) which is a new Python project management tool that is similar to Node's [NPM](https://www.npmjs.com) tool.

**Note:** you will need to have a recent version of [Python](https://www.python.org) installed and PDM installed to work with this example. Please visit the [PDM website](https://pdm.fming.dev) to see various installation methods.

# Step 1: Initializing the PDM project

First, create a directory named `python_api_server_1`. Then, from the command line run `pmd init`. This will prompt you with various questions that you will either need to answer and pick the default. After you do this a `pyproject.toml` file will be generated with your configuration information. Here is an example of our `pyproject.toml`:

```
[project]
name = "python_api_server_1"
version = "1.0"
description = "A simple API server"
authors = [
    {name = "Tim Richards", email = "richards@cs.umass.edu"},
]
dependencies = []
requires-python = ">=3.9"
dynamic = ["classifiers"]
license = {text = "MIT"}

[project.urls]
homepage = ""

[build-system]
requires = ["pdm-pep517"]
build-backend = "pdm.pep517.api"
```

This process will also generate a `.pdm.toml` file which is used to store local configuration information. If you are using Github, you should put this file name in your `.gitignore`.

# Step 2: Install dependencies

This example will use FastAPI to write a basic API server. It also uses [uvicorn](https://www.uvicorn.org) as the underlying HTTP server, so we will need to install that as well. This is how you do it using PDM:

```
$ pdm add fastapi
$ pdm add uvicorn
```

You will see output that indicates that both of these libraries have been installed. You will also notice that it updated your `pyproject.toml` file to include these dependencies. In addition, you will notice that a `pdm.lock` file was also generated. This file is used to "lock" the dependency versions to ensure that if you build/run the application on another system it uses *exactly* the version of the installed packages that you used. You should not delete this file and it should be included in a Git repository.

You will also notice that a `__packages__` directory was produced. This is where all of the installed libraries go. If you are familiar with Node's NPM, it is similar to the `node_modules` directory. You do not need to touch this and it should be added to your `.gitignore` file if you are using Git.

# Step 3: Setting up VSCode

It is highly recommended that you use VSCode to edit your files. To allow for Python auto-completion of installed libraries you should create a directory called `.vscode` and inside that directory create a `settings.json` file with the following content:

```
{
    "python.autoComplete.extraPaths": [
        "${workspaceFolder}/__pypackages__/PYTHON_VERSION/lib"
    ],
    "python.analysis.extraPaths": [
        "${workspaceFolder}/__pypackages__/PYTHON_VERSION/lib"
    ],
}
```

You will need to replace `PYTHON_VERSION` with the Python version shown in the `__pypackages__` folder.

# Step 4: A Simple API Server

Next, we want to write a simple API server in Python using FastAPI. Create a new file in the root of your project folder called `main.py`. First, we import the packages we are going to use:

```python
from typing import Optional
from fastapi import FastAPI
```

The `typing` library allows us to use Python's support for specifying types statically. This is used by the FastAPI library to provide rudimentary validation on routes and parameters. We are importing the `Optional` type which is used to indicate that the query parameter is optional. More on this later.

Next, we create the application object:

```python
app = FastAPI()
```

Now, we write a route that will return some simple JSON when the root is requested:

```python
@app.get('/')
def read_root():
    return {'Hello': 'World'}
```

The `@app.get('/')` decorator indicates that the function it "decorates" will be invoked when this application receives a request where the URL path is `/`/`. This function simply returns a Python dictionary, which to our delight, is automatically converted into JSON to be returned as the response.

Here is another route to make it more interesting:

```python
@app.get('/item/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):
    return {'item_id': item_id, "q": q}
```

This route will be invoked when the URL path matches the route pattern that is specified. The pattern is a path starting with `/item/` followed by a variable indicated by `{item_id}`. This `item_id` could be anything, however, the function parameters constrain it.

The `read_item` function has two parameters that work in coordinate with the route decorator. The first parameter is named to match the route variable, `item_id`, and it is typed as an `int`. This will inform the FastAPI library to ensure that the `{item_id}` matched in the route is an integer. The second parameter, `q`, is an optional string representing a query string. Not surprisingly, this means that the query string is optional.

Here is the complete program:

```python
from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/item/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):
    return {'item_id': item_id, "q": q}
```

# Step 5: Test the application on your computer

Now that we have packages installed and a basic API server, let us test it out. To do this we need to run `uvicorn` with our code we wrote in `main.py`. This is quite simple:

```
pdm run uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

We use the `pdm run` command which is followed by the actual command we want to run. This will run the command in our local Python environment and give our code access to the libraries that we installed. This is what each argument means:

`uvicorn`: this is the HTTP server that will receive incoming requests and invoke the routes we defined in `main.py`.
`main:app`: this is the name of the entry point to our server. The format is `module:attribute`. In our case, the module is `main.py` (without the `.py`) and the attribute is simply `app`. 
`--host 0.0.0.0`: this indicates that the server may receive incoming requests from any host.
`--port 5000`: the server will listen for incoming requests on port 5000.
`--reload`: this will reload the server when there are changes to the source files; useful for development.

You will see output that looks something like this when you run the command above:

```
INFO:     Will watch for changes in these directories: ['/the/directory/you/run/this/from']
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started reloader process [95771] using statreload
INFO:     Started server process [95788]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Now, you can visit [http://localhost:5000](http://localhost:5000) in your browser of choice and interact with the server. Type C-c in the terminal to exit the server.

To make life easier, we can create shortcuts in PDM to have it run complicated commands for us. Open up the `pyproject.toml` file and add this to the bottom of it:

```
[tool.pdm.scripts]
start_server = "uvicorn main:app --host 0.0.0.0 --port 5000 --reload"
```

Now, we can run this command in a shorter form like this:

```
$ pdm run start_server
```

# Step 6: Create a Dockerfile to run the app in Docker

We now want to build a Docker image that will allow us to run our application entirely in a container. The basic idea is to use an officially supported [Python Docker image from DockerHub](https://hub.docker.com/_/python), install PDM, copy PDM configuration files into the image, install Python packages using PDM, and indicate how to run the server. Let us look at this step-by-step.

Create a new file in the root of this project called `Dockerfile`. The first line of this file is:

```
FROM python
```

This is the official Docker image we will build from. Next, we will install PDM by running this command:

```
RUN pip install pdm
```

We will then set a working directory (similar to the `cd` command), which is where our application will live.

```
WORKDIR /usr/src/app
```

Next, we copy the PDM files that will allow us to install the required Python libraries and then install them with PDM:

```
COPY ./pyproject.toml ./
COPY ./pdm.lock ./
RUN pdm install
```

Lastly, we copy our `main.py` file into the image, export port 5000 in the container to allow HTTP communication to come in from outside the container, and indicate the command to run to start the server.

```
COPY ./main.py ./main.py
EXPOSE 5000
CMD ["pdm", "run", "start_server"]
```

Note that we use our "shortcut" to start the server using PDM.

Here is the complete `Dockerfile`:

```
# pull the Python Docker image
FROM python

# Install PDM
RUN pip install pdm

# Create the directory inside the container for the app
WORKDIR /usr/src/app

# Copy the generated modules and all other files to the container
COPY ./pyproject.toml ./
COPY ./pdm.lock ./pdm.lock

# Install libraries
RUN pdm install

# Copy the code into the container
COPY ./main.py ./main.py

# our app is running on port 5000 within the container, so need to expose it
EXPOSE 5000

# the command that starts our app
CMD ["pdm", "run", "start_server"]
```

# Step 7: Build the custom image

We have seen how to build a Docker image before. To make things easier, we are going to add another shortcut to our `pyproject.toml` file to build the docker image (after the `start_server` shortcut):

```
docker_build = "docker build -t python_server_1 ."
```

Then we can run it with:

```
$ pdm run docker_build
```

This will create the `python_server_1` image from which we can instantiate a new container with our HTTP app running inside it.

# Step 8: Running a container with out custom image

Now with everything setup we can create a new container and run our application inside it. To make life easier, we will add two additional shortcuts to the `pyproject.toml` file:

```
docker_run = "docker run -d --rm --name my_python_server_1 -p 5000:5000 python_server_1"
docker_stop = "docker stop my_python_server_1"
```

Now, we can simply run the following from the terminal:

```
$ pdm run docker_run
```

Now, you can visit [http://localhost:5000](http://localhost:5000) in your browser of choice and interact with the server running in the Docker container.

To stop the server do this:

```
$ pdm run docker_stop
```