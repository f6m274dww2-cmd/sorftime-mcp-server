# Sorftime Data MCP Server

把 Sorftime 跨境卖家数据能力封装成 MCP Server，让 Claude / Cursor / 扣子 / 豆包等 AI 客户端直接调用数据工具。

> 🔗 **数据购买 / 续费入口（渠道 Tag）**：https://open.sorftime.com/home?tag=NTIw
> 新用户首月 39.9 元；MCP/API 按月订阅，额度用尽时工具会自动返回购买引导。

## 工具清单



| 工具                        | 说明                         | 数据来源   |
| ------------------------- | -------------------------- | ------ |
| `get_category_trend`      | 类目趋势（销量 / 销售额 / 均价 / 新品占比） | 数据 API |
| `get_keyword_heat`        | 关键词搜索热度与竞争度                | 数据 API |
| `get_competitor_overview` | 竞品（ASIN）核心经营数据             | 数据 API |
| `get_market_rank`         | 类目热销排行                     | 数据 API |
| `calc_profit`             | 跨境单件利润测算（本地计算）             | 本地公式   |

## 快速开始



```
pip install -r requirements.txt
export SORFTIME_API_KEY=你的密钥        # 必填（API 类工具）
export SORFTIME_API_BASE=https://api.sorftime.com/v1   # 可选

# 本地调试（stdio，可直接在 Claude Desktop / Cursor 中连接）
python mcp_server.py

# 远程托管（Streamable HTTP，供线上 AI 客户端调用）
python mcp_server.py --transport streamable-http --port 8000
```

## 部署建议



1. **本地 / 内网调试**：stdio 模式，配 Claude Desktop / Cursor。

2. **公开托管**：`--transport streamable-http` 部署到云函数 / Docker，配 HTTPS 域名（如 `https://mcp.sorftime.com/mcp`），用于上架各 MCP 目录。

3. **鉴权**：公开托管时建议在网关上做 API Key 鉴权，与官方目录的认证流程配合。

## 上架（分发）

见 [docs/registry-submit.md](docs/registry-submit.md)。核心顺序：

官方 MCP Registry → Glama 自动抓取 → mcp.so/ MCP Market / FastMCP 表单 → 托管型列表。

## 开源策略（建议）



* 本仓库公开（docs + manifest 必须公开），服务端可私有。

* `calc_profit` 为免费工具，可无 Key 使用，作为引流钩子。

* README 顶部放官网链接与定价入口。

## 免责说明

`calc_profit` 为简化口径（退货仅扣售价、未含退货处理费），正式财务测算请以公司财务口径为准。