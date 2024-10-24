# Subjective Lexical Frequency in LSU

_Subjective Lexical Frequency in LSU_ is a task that gathers subjective
frequency ratings for 277 signs from the Uruguayan sign language (LSU). The
task was programmed using [Django](https://www.djangoproject.com/),
[Bootstrap](https://getbootstrap.com) and [jsPsych](https://www.jspsych.org),
and can be run online or offline (it is configured to display a larger list of
signs if it is being run offline and a longer timeout for ending the task).

As this same web server could be easily adapted for running the task for a
different set of signs or even a different sign language (see instructions
below), the source code is being made public for other researchers to use.

## Installation

> [!IMPORTANT]
> If [`pip`](https://docs.python.org/3/library/ensurepip.html),
> [`venv`](https://docs.python.org/3/library/venv.html) or
> [Postgres](https://www.postgresql.org/) are not installed,
> install them first:
>
> ```
> sudo apt install python3-pip
> sudo apt install python3-venv
> sudo apt install postgresql
> ```

1. Create a new [virtual environment](https://docs.python.org/3/library/venv.html):

```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the dependencies:

```
python -m pip install -r requirements.txt
```

3. Create the [Postgres](https://www.postgresql.org/) database:

```
createdb martin
sudo -u martin psql
CREATE DATABASE frecuencialexicalsu WITH OWNER martin;
```

4. Set-up the initial state of the database:

```
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed --mode=refresh
```

## Starting the server

1. Activate the [virtual environment](https://docs.python.org/3/library/venv.html):

```
source .venv/bin/activate
```

2. Start a web server on your local machine:

```
gunicorn mysite.wsgi
```

This will start a development server at [localhost](http://127.0.0.1:8000). 
You can open that address to run the task in online mode or you can open it in
[offline mode](http://127.0.0.1:8000?mode=2) (it will use a larger set of
stimuli and longer timeout), or even in
[debug mode](http://127.0.0.1:8000?mode=3) (it just use a very small set of
stimuli). Head to the [settings site](http://127.0.0.1:8000/settings) to
 configure the size of the set of stimuli in each mode, and to the
 [admin site](http://127.0.0.1:8000/admin) to see the replies and to
 [API](http://127.0.0.1:8000/api) to interact with the REST interface.

## Adaptation

Follow the next steps to either update the list of signs or language the task
is run in.

### Updating the set of stimuli (videos with LSU signs)

1. Place the video files at folder at `frequencies/static/terms` and update
2. the CSV file accordingly at `frequencies/management/commands/seed.csv`.

2. Activate the
[virtual environment](https://docs.python.org/3/library/venv.html):

```
source .venv/bin/activate
```

3. Fill the database with the stimuli:

```
python manage.py seed --mode=refresh
```

### Updating the instructions

If the task is meant to be run for a different sign language, you will need to
update the instructions and form as well (that is, everything visible to the
user that is either in LSU or Spanish). To do so, walk through the following
steps in the order you want:

* The videos with instructions in LSU and form questions are located in
`frequencies/static/hints` and referenced in `frequencies/views.py` (the form
questions) and in `frequencies/templates/index.html` (the instructions).

* Update the `information_paper.pdf` file that is referenced in `index.html`.

* The constrained set of replies the user can answer in the form are coded in
`frequencies/models.py` (you will need to update the database afterwards:
`python manage.py migrate`).
