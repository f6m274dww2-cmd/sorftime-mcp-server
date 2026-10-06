FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp_server.py .

ENV SORFTIME_API_BASE=https://api.sorftime.com/v1
ENV SORFTIME_PURCHASE_URL=https://open.sorftime.com/home?tag=NTIw

EXPOSE 8000

CMD ["python", "mcp_server.py", "--transport", "streamable-http", "--port", "8000"]
