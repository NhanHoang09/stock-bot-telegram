# 🚀 Hướng dẫn Setup GitHub Repository

## 📋 Bước 1: Tạo Repository trên GitHub

1. Truy cập [GitHub.com](https://github.com)
2. Click **"New repository"** hoặc **"+"** → **"New repository"**
3. Điền thông tin:
   - **Repository name:** `stock-bot`
   - **Description:** `Telegram Bot cho Thị trường Chứng khoán Việt Nam`
   - **Visibility:** Public hoặc Private (tùy chọn)
   - **Initialize with:** Không chọn gì (để trống)
4. Click **"Create repository"**

## 🔗 Bước 2: Kết nối Local Repository với GitHub

Sau khi tạo repository trên GitHub, bạn sẽ thấy URL. Copy URL đó và chạy lệnh:

```bash
# Thêm remote origin
git remote add origin https://github.com/YOUR_USERNAME/stock-bot.git

# Hoặc nếu dùng SSH:
git remote add origin git@github.com:YOUR_USERNAME/stock-bot.git

# Push code lên GitHub
git branch -M main
git push -u origin main
```

## 🔧 Bước 3: Cấu hình Repository

### 1. Thêm Topics/Tags

Trong repository settings, thêm các topics:

- `telegram-bot`
- `stock-market`
- `vietnam-stocks`
- `python`
- `vnstock`
- `financial-data`

### 2. Cấu hình GitHub Pages (Tùy chọn)

- Vào **Settings** → **Pages**
- Source: **Deploy from a branch**
- Branch: **main**
- Folder: **/ (root)**

### 3. Thêm Repository Description

```
📈 Telegram Bot cung cấp thông tin thị trường chứng khoán Việt Nam
✨ Tính năng: Giá cổ phiếu, Thông tin công ty, Chỉ số tài chính
🎨 Loading animation đẹp mắt
🐳 Docker ready
```

## 📊 Bước 4: Tạo Issues và Projects

### Issues Template

Tạo file `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:

1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**

- OS: [e.g. iOS]
- Python Version: [e.g. 3.8]
- Bot Version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### Feature Request Template

Tạo file `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## 🔄 Bước 5: Setup GitHub Actions (Tùy chọn)

Tạo file `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          python -m pytest test/
```

## 📈 Bước 6: Tạo Release

### 1. Tạo Tag

```bash
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"
git push origin v1.0.0
```

### 2. Tạo Release trên GitHub

- Vào **Releases** → **"Create a new release"**
- Chọn tag v1.0.0
- Title: `v1.0.0 - Initial Release`
- Description:

```markdown
## 🎉 Initial Release

### ✨ Features

- 📊 Thông tin công ty với `/company <mã>`
- 💹 Giá cổ phiếu với `/stock <mã>`
- 💰 Chỉ số tài chính với `/financial <mã>`
- 🎨 Loading animation đẹp mắt
- 🐳 Docker support

### 🛠️ Technical

- Python 3.8+
- python-telegram-bot
- vnstock library
- SQLAlchemy ORM
- Docker & Docker Compose

### 📱 Usage
```

/company VNM
/stock VNM  
/financial VNM

```

```

## 🔐 Bước 7: Bảo mật

### 1. Thêm Security Policy

Tạo file `SECURITY.md`:

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please email [your-email@example.com] instead of using the issue tracker.
```

### 2. Cấu hình Branch Protection

- Vào **Settings** → **Branches**
- Add rule cho branch `main`
- Require pull request reviews
- Require status checks to pass
- Include administrators

## 📊 Bước 8: Analytics và Insights

### 1. Thêm Repository Insights

- **Traffic:** Xem số lượt clone, view
- **Contributors:** Theo dõi contributors
- **Commits:** Phân tích commit activity

### 2. Setup Google Analytics (Tùy chọn)

Nếu có website, thêm Google Analytics tracking.

## 🎯 Bước 9: Quảng bá Repository

### 1. Social Media

- Chia sẻ trên Twitter, LinkedIn
- Tạo post trên Reddit r/Python
- Chia sẻ trong các group Telegram

### 2. GitHub Community

- Thêm vào GitHub Topics
- Tạo discussions
- Tham gia GitHub Sponsors

### 3. Documentation

- Cập nhật README.md thường xuyên
- Tạo Wiki pages
- Thêm examples và tutorials

---

## ✅ Checklist

- [ ] Tạo repository trên GitHub
- [ ] Push code lên GitHub
- [ ] Thêm topics và description
- [ ] Tạo Issues templates
- [ ] Setup GitHub Actions (tùy chọn)
- [ ] Tạo Release v1.0.0
- [ ] Thêm Security Policy
- [ ] Cấu hình Branch Protection
- [ ] Quảng bá repository

**🎉 Chúc mừng! Repository của bạn đã sẵn sàng!**
