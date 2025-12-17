# Frontend Dockerfile (Dev Mode)
# Use Node 20 as base
FROM node:20-slim

WORKDIR /app

# Copy package.json to install dependencies first
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port (8081 as per user config)
EXPOSE 8081

# Command to run dev server
# --host 0.0.0.0 is crucial for Docker networking
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
