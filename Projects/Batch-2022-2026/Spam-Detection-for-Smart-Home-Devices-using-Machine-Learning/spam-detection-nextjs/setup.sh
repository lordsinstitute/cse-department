#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up IoT Spam Detection Next.js Application...${NC}"

# Install Next.js dependencies
echo -e "${YELLOW}Installing Next.js dependencies...${NC}"
npm install

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p public/uploads
mkdir -p public/images

# Copy images from Flask app if they exist
echo -e "${YELLOW}Checking for ML visualization images...${NC}"
if [ -d "../static/pimg" ]; then
  echo -e "${GREEN}Found ML visualization images, copying...${NC}"
  cp -r ../static/pimg/* public/images/
else
  echo -e "${YELLOW}ML visualization images not found. Default placeholders will be used.${NC}"
fi

# Create a .env.local file for configuration
echo -e "${YELLOW}Creating .env.local file...${NC}"
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:5000
EOF

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}To start the Next.js development server:${NC}"
echo -e "  npm run dev"
echo -e "${YELLOW}Make sure to also run the Flask backend:${NC}"
echo -e "  cd .. && python app.py"
echo -e "${GREEN}Happy coding!${NC}" 