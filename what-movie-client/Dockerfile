# Base image for local development
FROM node:14 as development

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the entire application
COPY . .

# Expose port 3000 for development server
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]
