# Use the official Node.js image
FROM node:23-slim

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the frontend files
COPY . /app/

# Build the React app
RUN npm run build

# Install a lightweight web server to serve the React app
RUN npm install -g serve

# Expose the React app port (default is 5000)
EXPOSE 5001

# Serve the app
CMD ["serve", "-s", "build", "-l", "5001"]
