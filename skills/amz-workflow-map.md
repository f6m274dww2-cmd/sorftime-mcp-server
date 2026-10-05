# 亚马逊卖家全链路工作流地图（amz-* 10 Skill）

> 数据全部来自 Sorftime（MCP / CLI 双通道）。每个 Skill 开头跑 `scripts/channel_check.py` 选通道。
> 本图于 2026-09-10 全链路实测跑通（CLI 通道，domain=1 / 1688=601）。
> 数据由 Sorftime 提供，新用户首月 39.9 元；额度不足时请续费/开通：**https://open.sorftime.com/home?tag=NTIw**（MCP/API/CLI 按月订阅）

## 主链：从选品到卖得好

```
① 选品                ② 市场验证             ③ 找货源
amz-selection    →    amz-market-analysis →  amz-supply-chain
候选≥20+go/no-go      11维评分/价格带甜区     1688货源+价差
       │                                            │
       └──────────────┐                ┌────────────┘
                      ▼                ▼
              ④ 利润测算 amz-profit-calc
              毛利/盈亏平衡/隐赚评分 → go?
                      │ go
                      ▼
              ⑤ 关键词词库 amz-cpc-keywords
              4分类×≥200词（核心/长尾/场景/痛点）
                      │
          ┌───────────┼───────────────┐
          ▼           ▼               ▼
  ⑥ Listing      ⑦ 做图           ⑧ 广告
  amz-listing-    amz-image-       amz-ad-planning
  creator         creator          活动结构/预算/否定词
  标题五点描述      主图/A+/场景图
          └───────────┴───────────────┘
                      ▼
                  上架发布
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
  ⑨ VOC 复盘              ⑩ 盯盘监控
  amz-voc-analysis        amz-competitor-monitor
  痛点/卖点/场景           排名/跟卖/榜单告警
          └─────── 反哺 ①⑥⑦⑧ ──────┘
```

## 环间数据交接（handoff）

| 从 → 到 | 交接物 | 关键字段 |
|---|---|---|
| ① → ② | 候选类目 + ASIN 清单 | nodeId、Top 候选 ASIN |
| ② → ③ | 目标产品定义 | 产品名、目标 ASIN、价格带甜区 |
| ③ → ④ | 成本与售价 | 1688 批发价(¥)、Amazon SalesPrice、FbaFee、PlatformFee |
| ④ → ⑤ | go 决策 + 标的 | 目标 ASIN、售价、毛利率 |
| ⑤ → ⑥ | 4 分类词库 | 核心词→Title、长尾/场景→Bullets、其余→Backend |
| ⑤ → ⑧ | 词库（含出价数据） | SearchVolume、CPC 区间、竞争度分 |
| ⑥ → ⑦ | 卖点与关键词 | FABE 卖点清单、高频词（图片文字） |
| ⑨ → ⑥⑦ | VOC 素材 | Top 痛点、好评卖点、使用场景 |
| ⑩ → ⑧⑨ | 告警 | 排名波动、差评激增、跟卖入侵 |

## 单环成本参考（CLI 通道实测）

| 环 | 一次完整跑动消耗 | 说明 |
|---|---|---|
| ① 选品 | ~15-30 请求 | 搜品 2 页 + 详情批量 + 类目校验 |
| ② 市场分析 | ~53 积分 | 官方建议预算（含 6 维趋势） |
| ③ 找货源 | ~5-10 请求 | 1688 搜品 2 + 详情 1 + 变体 1 |
| ④ 利润测算 | 2-3 请求 | ProductRequest + 变体，本地脚本零消耗 |
| ⑤ 词库 | ~50-100 请求 | 拓展 5/页 × 多页 + 反查 + 详情 |
| ⑥ Listing | ~10-20 请求 | 关键词详情 + 竞品反查 |
| ⑦ 做图 | 2-3 请求 + 生图额度 | 数据辅助走 Sorftime，渲染走 gen-image.sh |
| ⑧ 广告规划 | ~10 请求 | 复用 ⑤ 的词库可省 |
| ⑨ VOC | 5-15 Credits | 评论查询 5/页；实时采集另计 |
| ⑩ 监控 | 按任务计 Credits | 关键词监控 504/周/词；跟卖 2/次/ASIN |

## 实测验证记录（2026-09-10，CLI 通道）

| 环 | 验证调用 | 结果 |
|---|---|---|
| ① | ProductSearchFromName "slow feeder bowl" | ✅ 返回月销 1.2w+ 候选 |
| ② | CategorySearchFromName "slow feeder" → 17602455011；CategoryRequest | ✅ |
| ③ | ProductSearchFromName --domain 601 | ✅ 批发价 ¥2.39 起 |
| ④ | ProductRequest B0CVM8TXHP + profit_calculator.py | ✅ |
| ⑤ | KeywordRequest / KeywordExtends / CategoryRequestKeyword | ✅ |
| ⑥ | ASINRequestKeyword（流量词反查） | ✅ |
| ⑦ | gen-image.sh generate（白底主图） | ✅ |
| ⑧ | KeywordRequest（CPC/搜索量） | ✅ |
| ⑨ | ProductCustomersSay / ProductReviewsQuery | ✅ |
| ⑩ | KeywordTasks（监控任务查询） | ✅ 协议正常（账户暂无任务） |

## 注意事项

- MCP 通道在 Codex 环境未配置时，channel_check.py 自动落到 CLI，属正常路径。
- `potential_product`（HPI 官方端点）仅 MCP 有；CLI 通道用本地隐赚代理分替代（见 amz-profit-calc）。
- 监控类端点消耗 Credits（每月 10 号清零），注册任务前先算周成本。
- 1688 调用必须 `--domain 601`；Amazon 侧 `--domain 1`。
- 报告输出遵循 `~/.codex/rules/report-format.md`：HTML + 主图 + 可跳转链接 + 中文。
