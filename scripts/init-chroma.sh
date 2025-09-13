#!/bin/bash
set -e

# Create the Chroma data directory if it doesn't exist
mkdir -p /chroma/chroma

# Set default environment variables
CHROMA_ADMIN_PASSWORD=${CHROMA_ADMIN_PASSWORD:-admin}

# Create credentials file if it doesn't exist
if [ ! -f /chroma/chroma_users.htpasswd ]; then
    echo "Creating Chroma credentials file..."
    htpasswd -b -c /chroma/chroma_users.htpasswd admin "$CHROMA_ADMIN_PASSWORD"
    chmod 600 /chroma/chroma_users.htpasswd
fi

# Set permissions
chown -R 1000:1000 /chroma/chroma
chmod -R 700 /chroma/chroma

echo "Starting ChromaDB..."

exec chroma run --path /chroma/chroma --host 0.0.0.0 --port 8000 \
    --chroma_server_auth_credentials "admin:$CHROMA_ADMIN_PASSWORD" \
    --chroma_server_auth_credentials_provider "chromadb.auth.token_authn.TokenAuthServerProvider" \
    --chroma_server_auth_provider "chromadb.auth.token_authn.TokenAuthServerProvider" \
    --chroma_server_auth_credentials_file "/chroma/chroma_users.htpasswd"
