# Smart Restaurant Backend API 🚀

## Overview
A high-performance, containerized backend architecture designed for restaurant operations. It handles secure user authentication, product management, and real-time stateful cart operations.

## 🛠️ System Architecture
- **Core Framework:** FastAPI (Python)
- **Primary Database:** PostgreSQL with SQLAlchemy ORM
- **In-Memory Cache:** Redis (for lightning-fast cart operations)
- **Containerization:** Docker & Docker Compose
- **Security:** JWT Authentication & Password Hashing

## ⚙️ Key Features
- **Asynchronous Processing:** Built entirely with async Python for maximum concurrent request handling.
- **Stateful Cart Management:** Utilizing Redis for rapid cart read/write operations before database checkout.
- **Isolated Environments:** Fully containerized setup allowing one-click deployment.

## 🚀 Quick Start
```bash
docker-compose up --build