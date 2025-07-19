#!/bin/bash

# Stock Bot Docker Management Script
# Hỗ trợ cả bot cũ và bot modular

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_bot_files() {
    if [ -f "bot_new.py" ]; then
        print_success "Tìm thấy bot modular (bot_new.py)"
        return 0
    elif [ -f "bot.py" ]; then
        print_warning "Chỉ tìm thấy bot cũ (bot.py)"
        return 1
    else
        print_error "Không tìm thấy file bot nào!"
        return 2
    fi
}

setup_modular_bot() {
    print_info "Thiết lập bot modular..."
    
    if [ ! -f "bot_new.py" ]; then
        if [ -f "bot.py" ]; then
            print_info "Tách commands từ bot cũ..."
            python split_commands.py
            print_success "Đã tạo bot modular"
        else
            print_error "Không tìm thấy bot.py để tách commands"
            exit 1
        fi
    fi
}

build_and_run() {
    print_info "Build và chạy Docker containers..."
    
    # Build images
    docker-compose build --no-cache
    
    # Run containers
    docker-compose up -d
    
    print_success "Docker containers đã được khởi động!"
    print_info "Bot đang chạy trên port 3336"
    print_info "Database đang chạy trên port 5432"
}

show_logs() {
    print_info "Hiển thị logs..."
    docker-compose logs -f stockbot-app
}

stop_containers() {
    print_info "Dừng containers..."
    docker-compose down
    print_success "Containers đã được dừng"
}

restart_containers() {
    print_info "Khởi động lại containers..."
    docker-compose restart
    print_success "Containers đã được khởi động lại"
}

cleanup() {
    print_warning "Xóa tất cả containers, images và volumes..."
    docker-compose down -v --rmi all
    print_success "Cleanup hoàn thành"
}

show_status() {
    print_info "Trạng thái containers:"
    docker-compose ps
    
    echo ""
    print_info "Sử dụng tài nguyên:"
    docker stats --no-stream
}

migrate_to_modular() {
    print_info "Migration sang bot modular..."
    python migrate.py
    print_success "Migration hoàn thành!"
}

rollback_to_old() {
    print_info "Rollback về bot cũ..."
    python migrate.py rollback
    print_success "Rollback hoàn thành!"
}

show_help() {
    echo "🤖 Stock Bot Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     - Build và chạy containers"
    echo "  stop      - Dừng containers"
    echo "  restart   - Khởi động lại containers"
    echo "  logs      - Hiển thị logs"
    echo "  status    - Hiển thị trạng thái"
    echo "  cleanup   - Xóa tất cả containers và images"
    echo "  migrate   - Migration sang bot modular"
    echo "  rollback  - Rollback về bot cũ"
    echo "  setup     - Thiết lập bot modular"
    echo "  help      - Hiển thị hướng dẫn này"
    echo ""
    echo "Examples:"
    echo "  $0 start      # Khởi động bot"
    echo "  $0 logs       # Xem logs"
    echo "  $0 migrate    # Chuyển sang bot modular"
}

# Main script
case "${1:-help}" in
    start)
        check_bot_files
        setup_modular_bot
        build_and_run
        ;;
    stop)
        stop_containers
        ;;
    restart)
        restart_containers
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    cleanup)
        cleanup
        ;;
    migrate)
        migrate_to_modular
        ;;
    rollback)
        rollback_to_old
        ;;
    setup)
        setup_modular_bot
        ;;
    help|*)
        show_help
        ;;
esac 