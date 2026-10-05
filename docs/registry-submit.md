# MCP 上架操作指引（registry-submit.md）

> 依据 2026 年 MCP 生态实测整理，按官方推荐顺序执行。全程无需企业资质、0 元上架费。

## 1. 前置（一次准备）

- [ ] MCP server 已部署为公开 HTTPS 地址（如 `https://mcp.sorftime.com/mcp`，Streamable HTTP）
- [ ] 公开 GitHub 仓库已就绪（docs + 本 server.json + README），建议公司组织名
- [ ] 免费体验 key 方案确定（供目录审核方试用）

## 2. 官方 MCP Registry（最重要，先做）

官方 Registry（registry.modelcontextprotocol.io）是下游所有目录的数据源头，用 CLI 提交、不接受 PR。

1. 生成 Ed25519 密钥对
2. 把公钥放到域名 `https://mcp.sorftime.com/.well-known/mcp-registry-auth`
3. 安装并认证 `mcp-publisher` CLI
4. 用反向 DNS 命名发布本仓库的 `server.json`（`io.sorftime/sorftime-data`）

提交一次后，Glama、PulseMCP 等下游目录会更快收录。

## 3. 社区目录（批量提交，共约 20 分钟）

| 目录 | 方式 | 备注 |
|---|---|---|
| Glama | 自动抓取 GitHub，3–7 天 | 未抓到则手动提交 glama.ai/mcp/connectors（托管型走这里） |
| mcp.so | 表单提交 | 约 2 分钟，自动拉取 README |
| MCP Market | 表单提交 + 人工审核 | 约 2 分钟 |
| FastMCP | 表单提交 | 约 2 分钟 |
| PulseMCP | 自动收录 | 发邮件 hello@pulsemcp.com 可加速 |
| awesome-remote-mcp-servers | GitHub PR | 托管型产品提交这里（punkpeye/awesome-mcp-servers 只收纯开源，别投） |
| Docker MCP Catalog | 容器化提交 | 可选，需容器化 |

## 4. 收费与变现（早期建议先免费试用）

- 早期：目录内免费试用 → 引导官网付费（39.9 首月 → 89/99 元起）
- 可选变现平台：MCPize（按次计费、85% 分成）、Smithery（开发者品牌）

## 5. 加分项

- VS Code 薄客户端扩展（vsce publish 即时上线，无审核队列）
- dev.to / 掘金 1 篇技术文章（"用 AI 做跨境选品"）

## 6. KPI 与复盘

- 收录目录数 ≥8
- 周 MCP 调用量（需服务端打点）
- 官网来自 MCP 市场的试用注册数（UTM 追踪）
