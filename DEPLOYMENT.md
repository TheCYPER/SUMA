# SUMA LMS Deployment Guide

This guide covers various deployment options for SUMA LMS, from local development to production environments.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### 1. Clone and Setup
```bash
git clone https://github.com/your-username/suma-lms.git
cd suma-lms
```

### 2. Start with Docker Compose
```bash
# Start all services
docker-compose up -d

# Pull Ollama model (in another terminal)
docker-compose exec ollama ollama pull llama3.1:8b

# Initialize database
docker-compose exec suma-lms python init_db.py
```

### 3. Access the Application
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Ollama: http://localhost:11434

## 🐳 Docker Deployment

### Single Container
```bash
# Build image
docker build -t suma-lms .

# Run container
docker run -d \
  --name suma-lms \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -e SECRET_KEY=your-secret-key \
  suma-lms
```

### With Ollama
```bash
# Start Ollama
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama

# Pull model
docker exec ollama ollama pull llama3.1:8b

# Start SUMA LMS
docker run -d \
  --name suma-lms \
  -p 8000:8000 \
  --link ollama:ollama \
  -e OLLAMA_BASE_URL=http://ollama:11434 \
  suma-lms
```

## ☁️ Cloud Deployment

### Railway

1. **Connect GitHub Repository**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub repository
   - Select the SUMA LMS repository

2. **Configure Environment Variables**
   ```env
   DATABASE_URL=postgresql://user:pass@host:port/db
   SECRET_KEY=your-production-secret-key
   OLLAMA_BASE_URL=https://your-ollama-instance.com
   OLLAMA_MODEL=llama3.1:8b
   ```

3. **Deploy**
   - Railway will automatically build and deploy
   - Access your app at the provided URL

### Render

1. **Create New Web Service**
   - Go to [Render](https://render.com)
   - Connect GitHub repository
   - Select "Web Service"

2. **Configure Build Settings**
   ```bash
   Build Command: pip install -r requirements.txt
   Start Command: python -m app.main
   ```

3. **Set Environment Variables**
   - Add all required environment variables
   - Deploy the service

### Heroku

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI
   # Create Procfile
   echo "web: python -m app.main" > Procfile
   ```

2. **Deploy**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-suma-lms
   
   # Set environment variables
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set OLLAMA_BASE_URL=your-ollama-url
   
   # Deploy
   git push heroku main
   ```

## 🐳 Kubernetes Deployment

### 1. Create Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: suma-lms
```

### 2. Deploy Ollama
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: suma-lms
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        ports:
        - containerPort: 11434
        volumeMounts:
        - name: ollama-data
          mountPath: /root/.ollama
      volumes:
      - name: ollama-data
        persistentVolumeClaim:
          claimName: ollama-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: ollama-service
  namespace: suma-lms
spec:
  selector:
    app: ollama
  ports:
  - port: 11434
    targetPort: 11434
```

### 3. Deploy SUMA LMS
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: suma-lms
  namespace: suma-lms
spec:
  replicas: 3
  selector:
    matchLabels:
      app: suma-lms
  template:
    metadata:
      labels:
        app: suma-lms
    spec:
      containers:
      - name: suma-lms
        image: your-registry/suma-lms:latest
        ports:
        - containerPort: 8000
        env:
        - name: OLLAMA_BASE_URL
          value: "http://ollama-service:11434"
        - name: DATABASE_URL
          value: "postgresql://user:pass@postgres:5432/suma_lms"
---
apiVersion: v1
kind: Service
metadata:
  name: suma-lms-service
  namespace: suma-lms
spec:
  selector:
    app: suma-lms
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 🗄️ Database Setup

### SQLite (Development)
```bash
# No additional setup required
# Database file will be created automatically
```

### PostgreSQL (Production)
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE suma_lms;
CREATE USER suma_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE suma_lms TO suma_user;
\q

# Update DATABASE_URL
export DATABASE_URL="postgresql://suma_user:your_password@localhost:5432/suma_lms"
```

### MySQL (Alternative)
```bash
# Install MySQL
sudo apt-get install mysql-server

# Create database and user
mysql -u root -p
CREATE DATABASE suma_lms;
CREATE USER 'suma_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON suma_lms.* TO 'suma_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Update DATABASE_URL
export DATABASE_URL="mysql://suma_user:your_password@localhost:3306/suma_lms"
```

## 🔧 Environment Configuration

### Production Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Security
SECRET_KEY=your-very-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ollama Configuration
OLLAMA_BASE_URL=https://your-ollama-instance.com
OLLAMA_MODEL=llama3.1:8b

# File Upload
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=10485760

# CORS
ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-app.com

# Production Settings
DEBUG=false
LOG_LEVEL=INFO
```

## 🔒 Security Considerations

### 1. Environment Variables
- Never commit `.env` files
- Use strong, unique secret keys
- Rotate keys regularly
- Use environment-specific configurations

### 2. Database Security
- Use strong passwords
- Enable SSL/TLS connections
- Regular backups
- Access control and firewalls

### 3. Application Security
- Enable HTTPS in production
- Use secure headers
- Implement rate limiting
- Regular security updates

### 4. Ollama Security
- Secure Ollama instance
- Use authentication if needed
- Monitor resource usage
- Regular model updates

## 📊 Monitoring and Logging

### Application Logs
```bash
# View logs
docker logs suma-lms

# Follow logs
docker logs -f suma-lms
```

### Health Checks
```bash
# Check application health
curl http://localhost:8000/health

# Check AI status
curl http://localhost:8000/ai/status
```

### Monitoring Setup
```yaml
# Add to docker-compose.yml
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## 🔄 Backup and Recovery

### Database Backup
```bash
# PostgreSQL
pg_dump suma_lms > backup_$(date +%Y%m%d_%H%M%S).sql

# SQLite
cp suma.db backup_$(date +%Y%m%d_%H%M%S).db
```

### File Backup
```bash
# Backup uploads directory
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz uploads/
```

### Automated Backup Script
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump suma_lms > $BACKUP_DIR/db_backup_$DATE.sql

# Backup uploads
tar -czf $BACKUP_DIR/uploads_backup_$DATE.tar.gz uploads/

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## 🚀 Scaling

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Multiple application instances
- Shared database and file storage
- Session management

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Use caching (Redis)
- CDN for static files

## 📝 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL format
   - Verify database server is running
   - Check network connectivity

2. **Ollama Connection Issues**
   - Verify Ollama service is running
   - Check OLLAMA_BASE_URL
   - Ensure model is downloaded

3. **File Upload Issues**
   - Check upload directory permissions
   - Verify MAX_FILE_SIZE setting
   - Check disk space

4. **CORS Issues**
   - Update ALLOWED_ORIGINS
   - Check frontend URL configuration

### Debug Mode
```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Start application
python -m app.main
```

## 📞 Support

For deployment issues:
1. Check the logs
2. Review this documentation
3. Create an issue on GitHub
4. Check the troubleshooting section

---

**Happy Deploying! 🚀**
