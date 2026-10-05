# Sorftime 卖家技能包（Skills Collection）

Sorftime 官方渠道分发的跨境卖家 AI 技能合集。全部技能依赖 **Sorftime 跨境数据服务**（MCP / API / CLI 三通道）提供数据底座。

> 🔗 **数据购买 / 续费入口（渠道 Tag）**：https://open.sorftime.com/home?tag=NTIw
> 新用户首月 39.9 元；MCP 89 元/月、API 99 元/月起；额度不足时技能会自动返回购买引导。

## 技能清单

### 亚马逊全流程（amz-* 10 技能 + 工作流地图）

| 技能 | 用途 |
|---|---|
| `amz-selection` | 选品：候选池 + go/no-go |
| `amz-market-analysis` | 市场验证：11 维评分 / 价格带甜区 |
| `amz-supply-chain` | 找货源：1688 货源 + 价差 |
| `amz-profit-calc` | 利润测算：毛利 / 盈亏平衡 |
| `amz-cpc-keywords` | 关键词词库：核心 / 长尾 / 场景 / 痛点 |
| `amz-listing-creator` | Listing 文案：标题 / 五点 / 描述 |
| `amz-image-creator` | 主图 / A+ / 场景图 |
| `amz-ad-planning` | 广告规划：活动结构 / 预算 / 否定词 |
| `amz-voc-analysis` | VOC 复盘：痛点 / 卖点 / 场景 |
| `amz-competitor-monitor` | 盯盘监控：排名 / 跟卖 / 榜单告警 |
| `amz-workflow-map.md` | 全链路工作流地图（①→⑩ 数据交接） |
| `amz-blue-ocean-picker` | 蓝海选品（模板完善中） |

### 平台数据 CLI

| 技能 | 用途 |
|---|---|
| `sorftime-data-cli` | 117 个数据端点（Amazon 57 / Shopee 17 / Walmart 17 / 1688 9 / Temu 12 / TikTok 17）批量查询、监控、跨平台比价 |
| `sorftime-seller-agent` | 卖家智能体（MCP）：选品 / 竞品 / 沃尔玛新手选品等全流程 agent |

### 1688 爆品雷达

| 技能 | 用途 |
|---|---|
| `kua-jing-bao-pin-lei-da` | 每日扫 1688 跨境专供，按亚马逊类目归类，输出候选池 / 打法卡 / 日报 |

## 安装方式

```bash
# 1. 克隆仓库
git clone https://github.com/f6m274dww2-cmd/sorftime-mcp-server.git
# 2. 把需要的技能目录放入你的 Agent 技能目录（如 ~/.agents/skills/ 或豆包工作区 .user_skills/）
cp -r skills/amz-selection ~/.agents/skills/
# 3. 配置 Sorftime 凭证
#    - CLI/API：注册后获取 Account-SK（见各技能 README）
#    - 新用户注册：https://open.sorftime.com/home?tag=NTIw
```

## 渠道说明

经 `https://open.sorftime.com/home?tag=NTIw` 注册的账号永久归属合作渠道，功能与价格与官网直连完全一致。
