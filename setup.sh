#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Setting up Autonomous Interview Interface${NC}"
echo -e "${YELLOW}This script will guide you through the setup process.${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "\n${GREEN}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please update the .env file with your configuration.${NC}"
    read -p "Press any key to open the .env file in your default editor..." -n 1 -r
    "${EDITOR:-nano}" .env
else
    echo -e "\n${GREEN}.env file already exists.${NC}"
fi

# Install root dependencies
echo -e "\n${GREEN}Installing root dependencies...${NC}"
yarn install

# Install and build all project dependencies
echo -e "\n${GREEN}Installing and building all project dependencies...${NC}"
make install

# Set up git hooks
echo -e "\n${GREEN}Setting up git hooks...${NC}"
npx husky install

# Build the application
echo -e "\n${GREEN}Building the application...${NC}"
make build

echo -e "\n${GREEN}✅ Setup complete!${NC}"
echo -e "\nTo start the development environment, run: ${YELLOW}make dev${NC}"
echo -e "Or start services individually:"
echo -e "- Frontend only: ${YELLOW}make dev-web${NC}"
echo -e "- API only: ${YELLOW}make dev-api${NC}"
echo -e "\nAccess the application at:"
echo -e "- Frontend: ${YELLOW}http://localhost:3000${NC}"
echo -e "- API Documentation: ${YELLOW}http://localhost:8000/docs${NC}"
