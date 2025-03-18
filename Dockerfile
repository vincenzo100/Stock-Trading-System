# Use an official lightweight web server
FROM nginx:alpine

# Copy the frontend files into the web server's directory
COPY . /usr/share/nginx/html

# Expose port 80 to make it accessible
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]
