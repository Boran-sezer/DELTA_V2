#!/bin/bash
# Script de build pour Render.com

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Node.js dependencies..."
npm install

echo "Building frontend..."
npm run build

echo "Creating necessary directories..."
mkdir -p projects backend/printer_profiles

echo "Build complete!"
