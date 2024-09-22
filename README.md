# Setup Guide

## Requirements
    Python 3.8+ (check with python --version)
    Git (for cloning the repository)
    pip

##  Setup Instructions
### 1. Clone the Repository

```
git clone https://github.com/TechCoursesUL/ULTC_BOT
cd ULTC_BOT
```

### 2. Set Up a Virtual Environment

To keep dependencies isolated, create a virtual environment using Python’s venv module:

```
python -m venv env
```
Activate the virtual environment:

On Windows:
```
venv\Scripts\activate
```
On macOS/Linux:
```
source venv/bin/activate
```
### 3. Install Dependencies

With the virtual environment activated, install the required dependencies using pip:

```
pip install -r requirements.txt
```
### 4. Configure the Bot

Before running the bot, make sure you create a .env file in the root of the project to store your bot token and other configuration secrets and place the ULTCDB private key JSON at /backend/DBAUTH.json

Create a .env file and add your bot token:
```
DISCORD_TOKEN=your-bot-token-here
```
Replace your-bot-token-here with the actual token.
### 5. Run the Bot

Now you’re ready to run the bot! With the virtual environment still active, use:

```
python bot.py
```

### 6. Deactivating the Virtual Environment

```
deactivate
```

## Additional Commands
Install a new dependency: If you add a new package, don’t forget to update requirements.txt:
```
pip install <package-name>
pip freeze > requirements.txt
```
Updating dependencies: If there are changes to requirements.txt, you can update the installed packages by running:

```
pip install --upgrade -r requirements.txt
```
## CATION!
### avoid running the main token and create a test bot, this is to avoid multiple runtimes.
### PLEASE make sure your virtualenv is either called: env or update the .gitignore with your venv name
