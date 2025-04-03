**Dashboard prototype for gene data**\
This app is a Flask-based web service to visualize differences in protein activity levels interactively.\
Clicking on a volcano plot point displays the respective old donor (OD) and young donor (YD) protein concentration values in boxplots below the volcano plot.\
Y axes' limits can be edited with `fig.update_yaxes` in the `draw_boxplot_from_data` function.\
Default port is `8855`.
Default IP is set to `0.0.0.0` for container compatibility.\
\
Startup options:

1. Build a Docker container:\
`docker build -t <tag>:<version> .`\
and run locally (or on any cloud compute provider e.g. GCP)\
`docker run --rm -p 8855:8855 <tag>:<version>`

2. Install dependencies:\
`pip install --upgrade pip`\
`pip install -r requirements.txt`\
(most of the dependencies are installed with dash_bio)\
Run locally with Python:\
`python main.py`

Warning: This is not a production environment, use a WSGI server e.g. Gunicorn:\
`pip install gunicorn`\
`gunicorn -w 1 -b <ip>:8855 main:server`\
Increment -w to handle concurrency\
\
Gene-related papers can be acquired with an API call. If the functionality implementation is required, it's recommended to switch to ASGI web framework and server with WSGI middleware (e.g. FastAPI + uvicorn) for async coroutines compatibility.
