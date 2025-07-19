# 🐳 Stock Bot - Docker Setup

## 🎯 Tổng Quan

Hướng dẫn chạy Stock Bot với Docker, hỗ trợ cả bot cũ và bot modular với hot reload.

## 📋 Yêu Cầu

- Docker
- Docker Compose
- Git

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd stock-bot
```

### 2. Thiết Lập Environment

```bash
# Tạo file .env
cp .env.example .env
# Chỉnh sửa TELEGRAM_TOKEN trong .env
```

### 3. Chạy Bot

```bash
# Sử dụng script quản lý (Khuyến nghị)
./docker-manage.sh start

# Hoặc sử dụng docker-compose trực tiếp
docker-compose up -d
```

## 🛠️ Docker Management Script

Script `docker-manage.sh` cung cấp các lệnh quản lý Docker dễ dàng:

### 📋 Các Lệnh Có Sẵn

```bash
# Khởi động bot
./docker-manage.sh start

# Dừng bot
./docker-manage.sh stop

# Khởi động lại
./docker-manage.sh restart

# Xem logs
./docker-manage.sh logs

# Kiểm tra trạng thái
./docker-manage.sh status

# Migration sang bot modular
./docker-manage.sh migrate

# Rollback về bot cũ
./docker-manage.sh rollback

# Setup bot modular
./docker-manage.sh setup

# Cleanup (xóa tất cả)
./docker-manage.sh cleanup

# Hiển thị help
./docker-manage.sh help
```

## 📊 Cấu Trúc Docker

### 🐳 Services

#### 1. **stockbot-app** (Main Application)

- **Image**: Custom Python 3.11
- **Port**: 3336:3000
- **Volumes**:
  - `.:/app` (Source code)
  - `./logs:/app/logs` (Logs)
  - `./cache:/app/cache` (Cache)
  - `/tmp:/tmp` (Matplotlib charts)
- **Environment**: Database config + Python settings
- **Health Check**: Python process monitoring

#### 2. **stockbot-db** (PostgreSQL Database)

- **Image**: PostgreSQL 15
- **Port**: 5432:5432
- **Volumes**: `pgdata:/var/lib/postgresql/data`
- **Health Check**: Database connectivity

### 🌐 Networks

- **stockbot-net**: Bridge network cho communication

### 💾 Volumes

- **pgdata**: PostgreSQL data persistence
- **cache**: Application cache

## 🔧 Cấu Hình

### Environment Variables

```env
# Bot Configuration
TELEGRAM_TOKEN=your_telegram_bot_token

# Database Configuration
DATABASE_HOST=stockbot-db
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASS=postgres
DATABASE_DB_NAME=stockbot

# Python Configuration
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### Resource Limits

```yaml
deploy:
  resources:
    limits:
      memory: 1G
    reservations:
      memory: 512M
```

## 📈 Monitoring & Logs

### Xem Logs

```bash
# Logs real-time
./docker-manage.sh logs

# Logs với docker-compose
docker-compose logs -f stockbot-app

# Logs database
docker-compose logs -f stockbot-db
```

### Health Checks

```bash
# Kiểm tra trạng thái
./docker-manage.sh status

# Health check manual
docker-compose ps
```

### Resource Usage

```bash
# Sử dụng tài nguyên
docker stats stockbot-app stockbot-db
```

## 🔄 Hot Reload

Bot hỗ trợ hot reload với `watchfiles`:

- **File Changes**: Tự động restart khi có thay đổi code
- **Modular Support**: Hỗ trợ cả bot cũ và bot modular
- **Smart Detection**: Tự động chọn bot phù hợp

## 🚀 Migration & Rollback

### Migration Sang Bot Modular

```bash
# Tự động migration
./docker-manage.sh migrate

# Manual migration
python migrate.py
```

### Rollback Về Bot Cũ

```bash
# Rollback
./docker-manage.sh rollback

# Manual rollback
python migrate.py rollback
```

## 🛠️ Development

### Development Mode

```bash
# Chạy với hot reload
docker-compose up

# Chạy background
docker-compose up -d
```

### Debug Mode

```bash
# Vào container
docker-compose exec stockbot-app bash

# Chạy bot trực tiếp trong container
python bot_new.py
```

### Testing

```bash
# Test bot modular
docker-compose exec stockbot-app python bot_new.py

# Test bot cũ
docker-compose exec stockbot-app python bot.py
```

## 🔧 Troubleshooting

### Common Issues

#### 1. **Container không start**

```bash
# Kiểm tra logs
./docker-manage.sh logs

# Rebuild
docker-compose build --no-cache
```

#### 2. **Database connection failed**

```bash
# Kiểm tra database
docker-compose logs stockbot-db

# Restart database
docker-compose restart stockbot-db
```

#### 3. **Memory issues**

```bash
# Kiểm tra memory usage
docker stats

# Cleanup
./docker-manage.sh cleanup
```

#### 4. **Permission issues**

```bash
# Fix permissions
chmod +x docker-manage.sh
chmod +x run.py migrate.py split_commands.py
```

### Cleanup & Reset

```bash
# Xóa tất cả
./docker-manage.sh cleanup

# Reset database
docker-compose down -v
docker-compose up -d
```

## 📊 Performance

### Optimization Tips

1. **Use .dockerignore**: Giảm build context
2. **Layer Caching**: Copy requirements.txt trước
3. **Multi-stage Build**: Tối ưu image size
4. **Resource Limits**: Tránh memory leaks
5. **Health Checks**: Monitor application health

### Monitoring

```bash
# Resource usage
docker stats

# Container status
docker-compose ps

# Log analysis
docker-compose logs --tail=100 stockbot-app
```

## 🔒 Security

### Best Practices

1. **Environment Variables**: Không hardcode secrets
2. **Non-root User**: Chạy với user không phải root
3. **Resource Limits**: Giới hạn memory/CPU
4. **Network Isolation**: Sử dụng custom networks
5. **Regular Updates**: Cập nhật base images

## 📝 Logs & Debugging

### Log Levels

- **INFO**: General information
- **WARNING**: Potential issues
- **ERROR**: Errors that need attention
- **DEBUG**: Detailed debugging info

### Log Locations

- **Application Logs**: `/app/logs/`
- **Docker Logs**: `docker-compose logs`
- **System Logs**: Container logs

## 🎯 Production Deployment

### Production Checklist

- [ ] Environment variables configured
- [ ] Database backup strategy
- [ ] Monitoring and alerting
- [ ] Resource limits set
- [ ] Security measures implemented
- [ ] Log rotation configured
- [ ] Health checks enabled

### Scaling

```bash
# Scale application
docker-compose up -d --scale stockbot-app=2

# Load balancing (if needed)
# Add nginx reverse proxy
```

---

**🔗 Liên hệ**: @nhanhoang09
