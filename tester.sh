#!/bin/bash

# Antes de arrancar hace falta hacer docker-compose up en otra terminal
cd frontend

# Actualiza los paquetes
npm ci

# Arranca la app
npx expo start