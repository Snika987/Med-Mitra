```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000
    volumes:
      - .:/app
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://sanika:pass123@db:5432/medassistant

  frontend:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
    command: streamlit run frontend/Home.py --server.port 8501
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: sanika
      POSTGRES_PASSWORD: pass123
      POSTGRES_DB: medassistant
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```