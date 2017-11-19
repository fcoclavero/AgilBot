# AgilBot
A Telegram to save study resources.

Visit: https://agilbot.herokuapp.com/

## Project configuration Guide:
### Create a Bot in Telegram:
1. Talk to BotFather (@BotFather)
2. Create a new bot: send `/newbot` and follow the instructions
3. List your bots: `/mybots`
4. Select your bot
5. Go to "Bot Settings", then "Allow Groups?" and select "Enable"

### Save Bot settings in project:
1. Go to Django Admin and login as admin:
2. Create or modify a Bot (the projct only uses the first bot):
3. Save the Bot name and use the TOKEN given by Botfather when you created the bot

### Teach commands through BotFather
1. Send `/setcommands` to BotFather
2. Choose your Bot
3. Send a list of commands in the following format: `command1 - Description`

### Add Bot to Groups and assign them a Semester:
1. Create a Telegram Group
2. Add the Bot to the Group
3. Send `/chat_id`, the Bot will reply the chat ID
4. Go to the Django admin and create a Semester, in the field `chat_id` store the chat ID given by the Bot

#### Example (you can copy and paste the following):
chat_id - Retorna el ID del chat a través del cuál se le está hablando al Bot

recurso - Agrega un recurso

## Instructions for Developers
### Installation Guide

  1. Install system requirements `sudo apt-get install libpq-dev python-dev python-pip python3-pip virtualenv`

  2. Create a virtualenvironment with python3: `virtualenv -p python3 venv`

  3. Activate virtualenv: `source venv/bin/activate`

  4. Install project requirements: `pip install -r requirements.txt`

### Execution (development server)
  * Activate virtual environment (if not already activated): `source venv/bin/activate`
  * Run development server: `python manage.py runserver`

### Run Tests
  * Run tests: `python manage.py test`
  * Run tests with coverage: `coverage run --source='.' manage.py test`
  * View coverage report in terminal:
    * Excluding third-party libraries in venv (recommended): `coverage report --omit='venv/*'`
    * Including third-party libraries: `coverage report`
  * View coverage report in website:
    * Excluding third-party libraries in venv (recommended): `coverage html --omit='venv/*'`
    * Including third-party libraries: `coverage html`
    * Open report: `<browser-command> htmlcov/index.html`, e.g:
      * Google Chrome: `google-chrome htmlcov/index.html`
      * Firefox: `firefox htmlcov/index.html`
