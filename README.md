# Ranch Discord Bot

This project aims to create a customized multi-function Discord bot for the discord server named "The Ranch". The scope of the project will increase over time as new features are developed. Right now we are a small team from the discord server working on developing the bot. We are happy to receive help from anyone who is interested, but most likely you will want to be a member of the server for it to make sense for you to develop a server-specific bot.

## Getting Started

The Ranch Discord Bot is developed using Python. It uses the [pycord](https://discordpy.readthedocs.io/en/stable/) API client to communicate with the Discord API. The project itself relies on [Poetry](https://python-poetry.org/) for dependency management. 

So, to get started, clone this repo into a directory of your choosing. Open a terminal and navigate into the directory of the cloned repo on your computer. Make sure to clone the repository and checkout submodules at the same time:

```sh
git clone --recurse-submodules https://github.com/Erik142/ranch-bot.git
```

When that is done, run the command

```sh
make environment
```

if you have `make` installed on your system. If not, run the following commands to create a development environment for the bot locally on your computer

``` sh
pip install --user poetry
poetry install
pip install -e ./src/dpytest
```

This only needs to be done one time after you have cloned the repo. Afterwards, either use the command

``` sh
poetry shell
```

to activate the virtual environment, or run individual commands within the virtual environment with `poetry run`, for example

```sh
poetry run python ./src/main.py
```

This needs to be done every time you start the terminal. When the virtual environment has been activated, you need to configure the file named `.env` which contains the environment variables used to set the configuration for the bot. `.env` does not exist in the project from the beginning, instead we have a template for `.env` named `ENV-VARIABLES`. Simply copy `ENV-VARIABLES` to the subdirectory `src/ranchbot/` and name it `.env`. Then modify `.env` to include the correct configuration. The current configuration parameters are the following:

- TOKEN: The token for your Discord bot that you have created using the Discord Developer Portal. You can find tutorials on the internet regarding how to create your own Discord App/Bot using the Developer Portal, for example using [this tutorial](https://astrogd.medium.com/how-to-create-a-discord-bot-application-afbe0e1e76af). The token is the token for your bot, that can be retrieved from the Discord Developer Portal.
- STATUS: The status for the Discord bot. Usually it is displayed in Discord underneath the bot name, after the string "Playing". For example, if the status was set to "Alive", then it would be displayed underneath the bot name, by the string "Playing Alive".
- PREFIX: The bot's command prefix, that is, the character or series of character that prefixes the command itself.
