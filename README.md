# Khiem Le Discord Bot (Slave of Khiem Le)

## Features

General:

- [x] **/help** - List all commands
- [x] **/ping_bot** - Ping the bot
- [x] **/random_number** - Choose random number in a range
- [x] **/random_pick** - Randomly pick an item from a list

Moderation:

- [x] **/vote_kick** - Create a poll to kick a member
- [x] **/vote_ban** - Create a poll to ban a member

ChatGPT:

- [x] **/chatgpt** - Chat with GPT-3
- [x] You can mention the bot to chat with it (using ChatGPT under the hood)

Meme:

- [x] **/meme** - Get random meme

## Start the bot

### Using Docker

First, you need to change the environment variables in the `.env.prod` file:

```bash
DISCORD_BOT_TOKEN=replace_with_your_key
CHATGPT_MODEL_NAME=gpt-3.5-turbo
OPENAI_API_KEY=replace_with_your_key
```

Then, start the bot using Docker:

```bash
docker-compose up -d
```

### Manually

First, you need to set these environment variables:

```bash
export DISCORD_BOT_TOKEN=replace_with_your_key
export CHATGPT_MODEL_NAME=gpt-3.5-turbo
export OPENAI_API_KEY=replace_with_your_key
```

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

Finally, start the bot:

```bash
cd src
python main.py
```

## Config

You can change the config in the `src/config/app.yaml` file. The config in
`${env:ENV_NAME}` will be loaded from environment variable.

## To-do

<!-- - [ ] **/help** - List all commands -->

## Want a features?

Feel free to open an issue or create a pull request.

## Issues

If you have any issues, please open an issue.
