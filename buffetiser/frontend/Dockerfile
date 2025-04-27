# Use node image
FROM node:23-slim

# Set working directory
WORKDIR /app

# Copy only package.json and package-lock.json first
COPY package*.json ./

# Install dependencies
RUN npm install

# Now copy the rest of your app
COPY . .

# Build
RUN npm run build