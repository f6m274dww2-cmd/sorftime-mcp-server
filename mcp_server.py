"""
Sorftime Data MCP Server
=======================
把 Sorftime 跨境数据能力封装成 MCP Server，供 Claude / Cursor / 扣子 / 豆包等
AI 客户端直接调用。本文件为可直接运行的工程骨架：

- 4 个工具走数据 API（需配置 SORFTIME_API_KEY）
- 1 个工具（利润测算）为本地计算，无需 API 即可使用

环境变量：
    SORFTIME_API_BASE  数据 API 地址，默认 https://api.sorftime.com/v1
    SORFTIME_API_KEY   数据 API 密钥（必填，否则 API 类工具不可用）

运行方式：
    本地调试（stdio）：  python mcp_server.py
    远程托管（HTTP）：   python mcp_server.py --transport streamable-http --port 8000
"""
from __future__ import annotations

import json
import os
from typing import Any, Optional

import httpx
from mcp.server.fastmcp import FastMCP

API_BASE: str = os.getenv("SORFTIME_API_BASE", "https://api.sorftime.com/v1").rstrip("/")
API_KEY: str = os.getenv("SORFTIME_API_KEY", "")

mcp = FastMCP(
    "sorftime-data",
    instructions=(
        "Sorftime 跨境卖家数据服务。可查询类目趋势、关键词热度、竞品监控、"
        "市场排行，并支持本地利润测算。返回 JSON 文本。"
    ),
)


# ---------------------------------------------------------------------------
# 数据 API 访问层（接入真实数据时无需改动工具代码）
# ---------------------------------------------------------------------------
def _headers() -> dict[str, str]:
    if not API_KEY:
        raise ValueError(
            "未配置 SORFTIME_API_KEY。请先设置环境变量后重试。"
        )
    return {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}


async def _api_get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """调用 Sorftime 数据 API（GET）。"""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{API_BASE}{path}", params=params or {}, headers=_headers())
        resp.raise_for_status()
        return resp.json()


async def _api_post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    """调用 Sorftime 数据 API（POST）。"""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(f"{API_BASE}{path}", json=payload, headers=_headers())
        resp.raise_for_status()
        return resp.json()


def _dump(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# 工具 1：类目趋势
# ---------------------------------------------------------------------------
@mcp.tool()
async def get_category_trend(
    category: str,
    marketplace: str = "amazon_us",
    days: int = 30,
) -> str:
    """查询指定类目在某市场的趋势数据。

    Args:
        category: 类目关键词，如 "gaming chair"、"yoga mat"。
        marketplace: 市场，可选 amazon_us / amazon_uk / amazon_de / tiktok_us 等。
        days: 回看天数，1-90。
    Returns:
        JSON：销量、销售额、均价、新品占比、趋势指数等。
    """
    data = await _api_get(
        "/mcp/category-trend",
        {"category": category, "marketplace": marketplace, "days": days},
    )
    return _dump(data)


# ---------------------------------------------------------------------------
# 工具 2：关键词热度
# ---------------------------------------------------------------------------
@mcp.tool()
async def get_keyword_heat(
    keyword: str,
    marketplace: str = "amazon_us",
) -> str:
    """查询关键词的搜索热度与竞争度。

    Args:
        keyword: 目标关键词，如 "cat water fountain"。
        marketplace: 市场。
    Returns:
        JSON：搜索量、搜索趋势、竞品数、广告竞争度、建议出价等。
    """
    data = await _api_get(
        "/mcp/keyword-heat",
        {"keyword": keyword, "marketplace": marketplace},
    )
    return _dump(data)


# ---------------------------------------------------------------------------
# 工具 3：竞品监控
# ---------------------------------------------------------------------------
@mcp.tool()
async def get_competitor_overview(
    asin: str,
    marketplace: str = "amazon_us",
) -> str:
    """查询单个竞品（ASIN）的核心经营数据。

    Args:
        asin: 商品 ASIN 编码。
        marketplace: 市场。
    Returns:
        JSON：排名、预估销量、销售额、价格波动、Review 增长、上架时间等。
    """
    data = await _api_get(
        "/mcp/competitor-overview",
        {"asin": asin, "marketplace": marketplace},
    )
    return _dump(data)


# ---------------------------------------------------------------------------
# 工具 4：市场排行
# ---------------------------------------------------------------------------
@mcp.tool()
async def get_market_rank(
    category: str,
    marketplace: str = "amazon_us",
    sort: str = "sales",
    top_n: int = 50,
) -> str:
    """查询某类目下的热销商品排行。

    Args:
        category: 类目关键词。
        marketplace: 市场。
        sort: 排序维度，可选 sales(销量) / revenue(销售额) / growth(增速)。
        top_n: 返回条数，1-200。
    Returns:
        JSON：排行列表（ASIN、标题、价格、销量、销售额、增速）。
    """
    data = await _api_get(
        "/mcp/market-rank",
        {"category": category, "marketplace": marketplace, "sort": sort, "top_n": top_n},
    )
    return _dump(data)


# ---------------------------------------------------------------------------
# 工具 5：利润测算（本地计算，无需 API）
# ---------------------------------------------------------------------------
@mcp.tool()
def calc_profit(
    price_usd: float,
    cost_cny: float,
    first_leg_cny: float,
    exchange_rate: float = 7.1,
    commission_pct: float = 15.0,
    ad_pct: float = 10.0,
    tariff_pct: float = 5.0,
    other_pct: float = 5.0,
    return_pct: float = 5.0,
) -> str:
    """跨境单件利润测算（简化口径）。

    Args:
        price_usd: 售价（美元）。
        cost_cny: 采购成本（人民币）。
        first_leg_cny: 头程及国内段费用（人民币/件）。
        exchange_rate: 美元兑人民币汇率。
        commission_pct: 平台佣金率（%）。
        ad_pct: 广告费率（占售价 %）。
        tariff_pct: 关税及税费率（占售价 %）。
        other_pct: 尾程/仓储等其他费率（占售价 %）。
        return_pct: 退货率（%），退货件按售价扣除。
    Returns:
        JSON：净利（USD/CNY）、净利率、保本售价。
    """
    p = price_usd
    unit_cost_usd = (cost_cny + first_leg_cny) / exchange_rate
    rate_sum = commission_pct + ad_pct + tariff_pct + other_pct
    valid_ratio = max(1 - return_pct / 100.0, 0.0)
    net_usd = p * valid_ratio - unit_cost_usd - p * rate_sum / 100.0
    net_margin = net_usd / p * 100.0 if p else 0.0
    denominator = valid_ratio - rate_sum / 100.0
    break_even = unit_cost_usd / denominator if denominator > 0 else float("inf")
    return _dump({
        "net_profit_usd": round(net_usd, 2),
        "net_profit_cny": round(net_usd * exchange_rate, 2),
        "net_margin_pct": round(net_margin, 1),
        "unit_cost_usd": round(unit_cost_usd, 2),
        "break_even_price_usd": round(break_even, 2) if break_even != float("inf") else None,
        "口径说明": "简化口径：退货仅扣售价、未含仓储退货处理费，正式测算请以财务口径为准。",
    })


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sorftime Data MCP Server")
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")
