# PRODUCT_WORKFLOW_SPEC

## 1. 目标

本文件定义 XCSOURCE 产品处理链路中的 001 / 002 / 003 正式职责边界、全局闭环状态字段规范，以及 Excel / JSON / 日志的最小落地规则。

核心原则：

- **`是否上传` 保持现有语义不变**：它继续作为前端 `generate_products_data.py` 的展示筛选字段使用。
- **003 不复用 `是否上传` 作为闭环上传状态**。
- **003 新增独立字段 `上传状态`**，并围绕该字段建立可审计闭环。
- Excel 是当前产品主数据源；JSON 状态文件用于程序化读写与审计增强。

---

## 2. 流程定义

### 001：采集 / 入池

职责：
- 监控品牌目录与日期文件夹
- 发现新图片
- 复制或移动到统一产品目录
- 记录已处理来源目录状态

输入：
- 品牌原始目录
- 日期子目录（如 `YYYYMMDD`）

输出：
- `assets/products/` 中的新图片
- `assets/products/.monitor_state.json`
- `assets/products/品牌文件夹监控.log`

不负责：
- AI 识别
- 产品中英文描述生成
- 上传状态回写

---

### 002：识别 / 建档 / 前端生成

职责：
- 识别产品图片
- 写入 / 更新 `产品识别.xlsx`
- 写入提示词、中文描述、英文描述
- 保持图片超链接有效
- 生成前端 `products.json`
- 同步前端展示图片目录

输入：
- `assets/products/` 中待识别图片
- `assets/products/已上传图片/`

输出：
- `assets/products/产品识别.xlsx`
- `assets/products/products.json`
- `assets/products/display/`
- `assets/products/产品识别.log`

不负责：
- 业务上传成功判定
- 003 上传闭环回写

---

### 003：上传 / 回写 / 闭环

职责：
- 读取符合上传条件的产品记录
- 执行上传动作（平台 / 站点 / 人工登记等）
- 回写上传状态与结果
- 记录失败原因与批次信息
- 形成可审计闭环

输入：
- `assets/products/产品识别.xlsx`
- 未来的上传配置 / 目标系统参数

输出：
- Excel 上传状态回写
- `assets/products/upload_state.json`（建议）
- `assets/products/003-upload.log`（建议）

不负责：
- 原始图片采集
- 图片识别
- 前端分页逻辑

---

## 3. 全局闭环状态字段规范

## 3.1 保留字段

以下字段保留既有语义：

| 字段 | 说明 |
|---|---|
| 序号 | Excel 中的行内序号 |
| 添加时间 | 记录被加入 Excel 的时间 |
| 图片超链接 | 图片路径 / 超链接字段 |
| 提示词 | AI 识别生成的提示词 |
| 中文描述 | 产品中文描述 |
| 英文描述 | 产品英文描述 |
| 是否上传 | **保留现有语义，不变更**；目前用于前端是否展示的筛选 |

> 当前规则：`generate_products_data.py` 继续仅按 `是否上传 = 否` 读取前端展示数据。

---

## 3.2 新增字段（正式规范）

| 字段 | 类型 | 说明 |
|---|---|---|
| 记录ID | string | 产品记录唯一标识，建议格式 `PRD-YYYYMMDD-0001` |
| 流程阶段 | string | 当前所处流程节点 |
| 识别状态 | string | 识别是否成功 |
| 前端生成状态 | string | 是否已进入前端 products 数据 |
| 上传状态 | string | **003 专用上传状态字段** |
| 上传时间 | string | 最后一次上传完成时间 |
| 上传目标 | string | 上传到哪个系统 / 平台 |
| 上传批次号 | string | 当前上传批次标识 |
| 上传结果 | string | 上传成功 / 跳过 / 结果摘要 |
| 失败原因 | string | 上传失败原因 |
| 最近处理时间 | string | 最近一次被任一流程节点处理的时间 |

---

## 3.3 枚举值规范

### 流程阶段

统一建议值：

- `001_已采集`
- `002_待识别`
- `002_已识别`
- `002_已生成前端数据`
- `003_待上传`
- `003_上传中`
- `003_上传成功`
- `003_上传失败`
- `003_已回写`
- `closed`

### 识别状态

- `pending`
- `success`
- `failed`

### 前端生成状态

- `pending`
- `success`
- `failed`

### 上传状态

- `pending`
- `uploading`
- `success`
- `failed`
- `skipped`
- `retry`

---

## 4. 003 上传状态回写规则

### 成功回写

- `上传状态 = success`
- `流程阶段 = 003_已回写`
- `上传时间 = 当前时间`
- `上传目标 = 目标系统`
- `上传批次号 = 当前批次号`
- `上传结果 = 成功摘要`
- `最近处理时间 = 当前时间`

### 失败回写

- `上传状态 = failed`
- `流程阶段 = 003_上传失败`
- `失败原因 = 具体错误`
- `上传批次号 = 当前批次号`
- `最近处理时间 = 当前时间`

### 重试回写

- `上传状态 = retry`
- `流程阶段 = 003_待上传`
- `失败原因 = 最近一次失败原因`
- `最近处理时间 = 当前时间`

---

## 5. 当前落地约束

在现阶段代码中：

- 前端展示仍然只依赖 `是否上传`
- 003 闭环字段已经在 Excel 结构中预埋
- 003 的实际上传动作与回写逻辑将在后续脚本中继续实现

因此当前阶段目标是：

1. **先稳定字段结构**
2. **不破坏前端现有读取逻辑**
3. **为 003 正式回写代码预留字段与文档基础**

---

## 6. 建议状态文件

建议新增：

```text
assets/products/upload_state.json
```

建议用途：
- 以 `记录ID` 为 key 存放 003 执行状态
- 便于程序级增量更新
- 便于失败重试与批次审计

建议结构示例：

```json
{
  "PRD-20260417-0001": {
    "upload_status": "success",
    "stage": "003_已回写",
    "upload_target": "github_pages",
    "uploaded_at": "2026-04-17 15:23:08",
    "batch_id": "UP-20260417-152308",
    "result": "页面已发布",
    "last_processed_at": "2026-04-17 15:23:08"
  }
}
```

---

## 7. 当前实现约定

### 001 / 002 当前已知主脚本

- `skills/brand-folder-monitor/scripts/monitor_brand_folders.py`
- `skills/brand-folder-monitor/scripts/organize_products_with_ai.py`
- `skills/brand-folder-monitor/scripts/organize_products_with_gpt.py`
- `generate_products_data.py`

### 当前预埋内容

- 新建 Excel 时会带上 003 相关字段
- 打开旧 Excel 时会自动补齐缺失字段
- 新增记录时会预填：
  - `流程阶段 = 002_已识别`
  - `识别状态 = success`
  - `前端生成状态 = pending`
  - `上传状态 = pending`
  - `最近处理时间 = 当前时间`

---

## 8. 下一步

下一阶段继续：

1. 实现 003 独立执行脚本
2. 写 `upload_state.json`
3. 回写 Excel 上传状态字段
4. 增加 003 日志与批次控制
