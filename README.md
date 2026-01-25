# 🚀 Python CI/CD App - Complete DevOps Pipeline


**Production-ready Flask app with complete GitHub Actions CI/CD pipeline using self-hosted runner!**

## ✨ **Features**

- 🔄 **6-Stage CI/CD Pipeline**: Build → Test → Quality → Reports → Notify → Deploy
- 🖥️ **Self-Hosted Runner**: Direct Docker deployment to production VM
- 🧪 **Multi-Python Testing**: Python 3.9, 3.10, 3.11 matrix
- 📊 **85% Code Coverage** requirement with HTML dashboards
- 🛡️ **Security Scanning**: Bandit + Secret Detection
- 📈 **Zero-Downtime Deployments** with health checks & rollback
- 🎨 **Production Reports**: Interactive coverage dashboards

## 🏗️ **Tech Stack**

```
Backend: Flask (Python 3.9+)
CI/CD: GitHub Actions + Self-Hosted Runner
Container: Docker + GHCR
Testing: pytest + pytest-cov (85% coverage)
Linting: flake8 + pylint
Security: Bandit + detect-secrets
Deployment: Direct Docker (no SSH!)
```

## 🚀 **Quick Start**

### **1. Clone & Install**
```bash
git clone https://github.com/aatirFound42/python-cicd-app.git
cd python-cicd-app
pip install -r requirements.txt
```

### **2. Run Locally**
```bash
# Development
flask run

# Production mode
FLASK_ENV=production flask run --host=0.0.0.0 --port=5000
```

### **3. Docker**
```bash
# Build
docker build -t python-cicd-app .

# Run
docker run -p 8000:5000 python-cicd-app
```

**Access:** `http://localhost:8000`

## 🔄 **CI/CD Pipeline**

### **6 Production Stages:**

| **Stage** | **Runner** | **Purpose** |
|-----------|------------|-------------|
| **Build** | `ubuntu-latest` | Docker image → GHCR |
| **Test** | `ubuntu-latest` | pytest matrix 3.9-3.11 |
| **Quality** | `ubuntu-latest` | 85% coverage gate |
| **Reports** | `ubuntu-latest` | HTML dashboards |
| **Deploy** | `self-hosted` | 🚀 Production VM |

### **Pipeline Flow:**
```
develop → Tests → Quality Gates → Coverage Reports
     ↓ (main + approve)
main → Build → Deploy to VM:8000 → Health Check ✓
```

## 🖥️ **Self-Hosted Runner Setup**

### **VM Requirements:**
```
Ubuntu 20.04+ / Docker 20+
GitHub Runner v2.330.0
Port 8000 open
```

### **Runner Install:**
```bash
# On production VM
sudo apt install docker.io
sudo useradd -m -G docker runner
sudo su - runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.330.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.330.0/actions-runner-linux-x64-2.330.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.330.0.tar.gz
./config.sh --url https://github.com/aatirFound42/python-cicd-app --token YOUR_TOKEN
./run.sh  # Keep running!
```

## 🔐 **Environment Secrets**

```
Repo → Settings → Environments → production:

CONTAINER_NAME=python-cicd-app-prod
CONTAINER_PORT_HOST=8000
```

## 📊 **Quality Gates**

```
✅ 85% Code Coverage (3 Python versions)
✅ Linting: flake8 + pylint  
✅ Security: Bandit scan
✅ Secrets: detect-secrets
✅ Multi-stage testing
✅ Health check deployment
```

## 🌐 **Production Access**

```
VM Local: http://localhost:8000
Network: http://YOUR_VM_IP:8000
Internet: http://PUBLIC_IP:8000 (port forward 8000)
```

## 📁 **Project Structure**

```
python-cicd-app/
├── app/                 # Flask application
│   ├── __init__.py
│   └── routes.py
├── tests/               # pytest tests
├── requirements.txt     # Python dependencies
├── Dockerfile          # Production Docker image
├── .github/
│   └── workflows/
│       └── python-cicd.yml  # Complete pipeline
├── docker-compose.yml  # Local development
└── README.md          # This file!
```

## 🧪 **Running Tests Locally**

```bash
# Install test deps
pip install -r requirements.txt pytest pytest-cov

# Run tests + coverage
pytest tests/ --cov=app --cov-report=html

# View coverage
open htmlcov/index.html
```

## 🔧 **Development Workflow**

```
1. git checkout -b feature/xyz
2. code → commit → push
3. Tests run automatically (develop)
4. Merge develop → main (production deploy)
5. VM auto-deploys: docker pull → docker run
```

## 📈 **Coverage Reports**

After pipeline runs:
```
Actions → Artifacts → all-coverage-reports
→ Interactive HTML dashboards for 3 Python versions
```

## ⚙️ **Dockerfile Highlights**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
HEALTHCHECK --interval=30s CMD curl -f http://localhost:5000/health
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
```

## 🎯 **Why This Pipeline Rocks**

```
✅ Self-hosted = FREE unlimited minutes
✅ No SSH complexity
✅ Automatic rollbacks
✅ Multi-environment testing
✅ Production dashboards
✅ Zero-downtime deploys
✅ Scalable to teams
```

## 🤝 **Contributing**

1. Fork repository
2. Create feature branch (`git checkout -b feature/xyz`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push (`git push origin feature/xyz`)
5. Open Pull Request

**All PRs run full CI/CD pipeline automatically!**

## 📄 **License**

[MIT License](LICENSE) - Free to use & modify!

***

**⭐ Star this repo if you found the self-hosted CI/CD setup helpful!**

[Pipeline](https://github.com/aatirFound42/python-cicd-app/actions) | [Docker Hub](https://ghcr.io/aatirFound42/python-cicd-app)
