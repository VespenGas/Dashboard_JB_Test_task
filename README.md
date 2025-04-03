**Dashboard prototype for gene data**__
This app is a Flask-based web service to visualize differences in protein activity levels interactively.__
Clicking on a volcano plot point displays the respective old donor (OD) and young donor (YD) protein concentration values in boxplots below the volcano plot.__
Y axes' limits can be edited with `fig.update_yaxes` in the `draw_boxplot_from_data` function.__
Default port is `8855`.
Default IP is set to `0.0.0.0` for container compatibility.__
__
Startup options:__
__
1. Build a Docker container:__
`docker build -t <tag>:<version> .`__
and run locally (or on any cloud compute provider e.g. GCP)__
`docker run --rm -p 8855:8855 <tag>:<version>`__

2. Install dependencies:__
`pip install --upgrade pip`__
`pip install -r requirements.txt`__
(most of the dependencies are installed with dash_bio)__
Run locally with Python:__
`python main.py`__
__
Warning: This is not a production environment, use a WSGI server e.g. Gunicorn:__
`pip install gunicorn`__
`gunicorn -w 1 -b <ip>:8855 main:server`__
Increment -w to handle concurrency__
__
Gene-related papers can be acquired with an API call. If the functionality implementation is required, it's recommended to switch to ASGI web framework and server with WSGI middleware (e.g. FastAPI + uvicorn) for async coroutines compatibility.
