#!/bin/bash

# Detect docker CLI command
if command -v docker-compose &>/dev/null; then
    DOCKER_CLI="docker-compose"
elif docker compose version &>/dev/null; then
    DOCKER_CLI="docker compose"
else
    echo "Neither docker-compose nor docker compose found."
    exit 1
fi

# Check if docker-compose.yml exists
COMPOSE_FILE="$PWD/docker-compose.yml"
if [ ! -f $COMPOSE_FILE ]; then
    echo "docker-compose.yml not found in current directory: $PWD"
    exit 1
fi

# Alias definition
ALIAS_NAME="starwars-cli"
ALIAS_COMMAND="$DOCKER_CLI -f \"$COMPOSE_FILE\" run --rm cli"

# Detect shell config file
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    if grep -q '. ~/.bash_aliases' "$HOME/.bashrc"; then
        SHELL_RC="$HOME/.bash_aliases"
        [ -f "$SHELL_RC" ] || touch "$SHELL_RC"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
else
    echo "Unsupported shell. Please add the alias manually:"
    echo -e "\talias $ALIAS_NAME='$ALIAS_COMMAND'"
    exit 1
fi

# Avoid duplicating the alias
if grep -q "$ALIAS_NAME=" "$SHELL_RC"; then
    echo "Alias '$ALIAS_NAME' already exists in $SHELL_RC"
else
    echo "Adding alias to $SHELL_RC"
    echo "alias $ALIAS_NAME='$ALIAS_COMMAND'" >> "$SHELL_RC"
    echo "Done. Please run: source $SHELL_RC"
fi
