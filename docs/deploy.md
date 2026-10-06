# MCP Server 部署说明（Docker）

把 Sorftime Data MCP Server 部署为公开 HTTPS 端点，供 Claude/Cursor/扣子等远程调用，并用于 MCP 目录收录。

## 1. 准备

- 一台可公网访问的服务器（云主机 / 轻量服务器均可）
- 一个域名（生产必需，MCP 目录收录与鉴权都要 HTTPS 域名）
- Sorftime 数据 API Key（SORFTIME_API_KEY）

## 2. 构建与启动

```bash
# 在仓库根目录（含 Dockerfile 与 docker-compose.yml）
cp .env.example .env          # 如有；或直接 export
export SORFTIME_API_KEY=你的Key
docker compose up -d --build
# 验证本地
curl http://localhost:8000/    # MCP streamable-http 端点
```

单容器方式：

```bash
docker build -t sorftime-mcp .
docker run -d --name sorftime-mcp -p 8000:8000 \
  -e SORFTIME_API_KEY=你的Key sorftime-mcp
```

## 3. 域名 + HTTPS（必需）

Nginx 反向代理 + 自动证书（以 `mcp.sorftime.com` 为例）：

```nginx
server {
    listen 443 ssl;
    server_name mcp.sorftime.com;
    # ssl_certificate / ssl_certificate_key 由 certbot 或云厂商托管证书提供
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        # streamable-http 需要流式响应
        proxy_buffering off;
        proxy_read_timeout 300s;
    }
}
```

然后用 certbot 签发证书：

```bash
sudo certbot --nginx -d mcp.sorftime.com
```

## 4. 网关鉴权（公开托管必须）

- 在网关上做 API Key 鉴权（Header `Authorization: Bearer <Key>`），
  与 MCP 官方 Registry 的认证流程配合（见 docs/registry-submit.md）
- 限频建议：单 Key 100 QPS 内，避免被滥用

## 5. 上架

部署完成后即可按 docs/registry-submit.md 走官方 Registry 收录。
