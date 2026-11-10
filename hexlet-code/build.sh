#!/usr/bin/env bash
# descargamos uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# aquí van los comandos que tu proyecto necesita para funcionar
make install && make collectstatic && make migrate