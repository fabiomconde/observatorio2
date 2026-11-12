# ---- Build stage ----
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements-docs.txt .
RUN pip install --no-cache-dir -r requirements-docs.txt
COPY . .

# ---- Runtime stage ----
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app /app
EXPOSE 8000
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
