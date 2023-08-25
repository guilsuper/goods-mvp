#!/bin/bash

# Copyright 2023 Free World Certified -- all rights reserved.

set +x

export SECRET_KEY="+6vtkpuu+#39e@sfy00(-10+6bagg6q_x3ci-v-8f8%%d#9t&u"
export DEBUG=False
export FRONTEND_HOST="http://localhost:3000"

export EMAIL_USER="dummy.stuff@gmail.com"
export EMAIL_PASSWORD="rcxghoyeshsiyplk"

export POSTGRES_NAME=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=db
export POSTGRES_PORT=5432

export LDFLAGS="-L/opt/homebrew/opt/postgresql@15/lib"
export CPPFLAGS="-I/opt/homebrew/opt/postgresql@15/include"

export PKG_CONFIG_PATH="/opt/homebrew/opt/postgresql@15/lib/pkgconfig"
