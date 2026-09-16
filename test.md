# AltoroMutual Container Deployment Guide

This guide provides step-by-step instructions for deploying the AltoroMutual application as a Docker container.

**WARNING**: This application contains intentional security vulnerabilities for educational purposes. Run it only in isolated, backed-up environments (such as a VM with host-only networking) at your own risk.

---

## Prerequisites

Before deploying the application as a container, ensure you have the following installed:

- **Docker** (version 20.10 or newer)
  - [Install Docker Desktop](https://docs.docker.com/get-docker/) for macOS/Windows
  - [Install Docker Engine](https://docs.docker.com/engine/install/) for Linux
- **Git** (to clone the repository if needed)
- At least 2GB of available disk space
- At least 1GB of available RAM

- Connect to AWS using: NAgDy8wLhHfbhdh658g4CCupFABc5PI7

Verify Docker is installed and running:

```bash
docker --version
docker ps
```

---

## Step 1: Navigate to the Project Directory

Open a terminal and navigate to the AltoroMutual project root:

```bash
cd /path/to/patch-mutual
```

---

## Step 2: Build the Docker Image

The project includes a multi-stage Dockerfile that:
1. Uses Gradle 7 with JDK 11 to build the application
2. Packages the application as a WAR file
3. Deploys it to Tomcat 9 with JDK 8

Build the Docker image with the following command:

```bash
docker build -t altoromutual:latest .
```

**What happens during the build:**
- The build process downloads all required dependencies
- Gradle compiles the Java source code
- The application is packaged as `altoromutual.war`
- The WAR file is copied to Tomcat's webapps directory as `ROOT.war`
- A non-root user `tomcat` is created for security

**Build time**: The first build typically takes 5-10 minutes depending on your internet connection and system performance.

To verify the image was created successfully:

```bash
docker images | grep altoromutual
```

---

## Step 3: Run the Container

Start the AltoroMutual container using one of the following methods:

### Option A: Basic Run (Foreground)

```bash
docker run -p 8080:8080 altoromutual:latest
```

### Option B: Run in Background (Detached Mode)

```bash
docker run -d -p 8080:8080 --name altoromutual altoromutual:latest
```

### Option C: Run with Persistent Database

To persist the Derby database across container restarts, mount a volume:

```bash
docker run -d -p 8080:8080 \
  -v altoromutual-data:/home/tomcat/.altoro \
  --name altoromutual \
  altoromutual:latest
```

**Command explanation:**
- `-d`: Run in detached mode (background)
- `-p 8080:8080`: Map port 8080 from container to host
- `-v altoromutual-data:/home/tomcat/.altoro`: Create named volume for database persistence
- `--name altoromutual`: Assign a friendly name to the container

---

## Step 4: Verify the Container is Running

Check the container status:

```bash
docker ps
```

You should see output similar to:

```
CONTAINER ID   IMAGE                  COMMAND             STATUS         PORTS
abc123def456   altoromutual:latest   "catalina.sh run"   Up 30 seconds  0.0.0.0:8080->8080/tcp
```

View container logs:

```bash
docker logs altoromutual
```

Wait for the message indicating Tomcat has started successfully (typically shows within 30-60 seconds).

---

## Step 5: Access the Application

Once the container is running and Tomcat has started:

1. Open your web browser
2. Navigate to: `http://localhost:8080`
3. You should see the AltoroMutual login page

### Default Credentials

- **Regular User**: 
  - Username: `jsmith`
  - Password: `demo1234`

- **Administrator**:
  - Username: `admin`
  - Password: `admin`

---

## Step 6: Stopping and Managing the Container

### Stop the Container

```bash
docker stop altoromutual
```

### Start the Container Again

```bash
docker start altoromutual
```

### Restart the Container

```bash
docker restart altoromutual
```

### Remove the Container

```bash
docker stop altoromutual
docker rm altoromutual
```

### Remove the Image

```bash
docker rmi altoromutual:latest
```

### View Container Logs

```bash
# View all logs
docker logs altoromutual

# Follow logs in real-time
docker logs -f altoromutual

# View last 100 lines
docker logs --tail 100 altoromutual
```

---

## Advanced Deployment: Kubernetes

For deploying to Kubernetes clusters, a deployment manifest is provided in `k8s-src/privilegedDeployment.yaml`. 

**Note**: This manifest is for demonstration purposes and includes privileged containers. Do not use in production environments.

### Deploy to Kubernetes

```bash
# First, tag and push your image to a registry
docker tag altoromutual:latest your-registry/altoromutual:latest
docker push your-registry/altoromutual:latest

# Update the image in the deployment YAML to point to your registry

# Apply the deployment
kubectl apply -f k8s-src/privilegedDeployment.yaml

# Check deployment status
kubectl get deployments
kubectl get pods

# Create a service to expose the application
kubectl expose deployment snyk-deployment --type=LoadBalancer --port=8080
```

---

## Troubleshooting

### Container Fails to Start

**Check logs for errors:**
```bash
docker logs altoromutual
```

**Common issues:**
- Port 8080 already in use: Change the host port mapping, e.g., `-p 8081:8080`
- Insufficient memory: Ensure Docker has at least 1GB of RAM allocated

### Cannot Access Application

1. Verify the container is running: `docker ps`
2. Check port binding: `docker port altoromutual`
3. Test connection: `curl http://localhost:8080`
4. Check firewall rules if accessing from another machine

### Database Issues

**Error: "Failed to create database 'altoro'"**

This typically happens due to permission issues. To reset:

```bash
# Stop and remove the container
docker stop altoromutual
docker rm altoromutual

# Remove the data volume
docker volume rm altoromutual-data

# Start fresh
docker run -d -p 8080:8080 --name altoromutual altoromutual:latest
```

### Rebuild After Code Changes

If you've made changes to the source code:

```bash
# Stop and remove existing container
docker stop altoromutual
docker rm altoromutual

# Rebuild the image (use --no-cache to force clean build)
docker build -t altoromutual:latest .

# Start new container
docker run -d -p 8080:8080 --name altoromutual altoromutual:latest
```

---

## Environment Configuration

The application can be configured using environment variables passed to the container:

```bash
docker run -d -p 8080:8080 \
  -e CATALINA_OPTS="-Xmx512m -Xms256m" \
  --name altoromutual \
  altoromutual:latest
```

---

## REST API Access

AltoroMutual includes a REST API documented with Swagger. After starting the container:

1. Navigate to `http://localhost:8080`
2. Click on the "REST API" link in the footer
3. Explore and interact with the API endpoints

---

## Security Considerations

This application is intentionally vulnerable and should **NEVER** be deployed in production or exposed to the public internet. Best practices:

- Run only in isolated development/training environments
- Use Docker networks to limit connectivity
- Consider running on a separate VM with host-only networking
- Do not use real or sensitive data
- Regularly backup your VM/environment before running

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Tomcat Documentation](https://tomcat.apache.org/tomcat-9.0-doc/)
- [Gradle Documentation](https://docs.gradle.org/)
- [AltoroJ GitHub Repository](https://github.com/AppSecDev/AltoroJ)

---

## Quick Reference

```bash
# Build image
docker build -t altoromutual:latest .

# Run container
docker run -d -p 8080:8080 --name altoromutual altoromutual:latest

# View logs
docker logs -f altoromutual

# Stop container
docker stop altoromutual

# Start container
docker start altoromutual

# Access application
# Browser: http://localhost:8080
```

