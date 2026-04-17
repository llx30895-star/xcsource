# 003 Agent - Product Upload & Closure Agent

## Agent Identity

**Agent ID:** `003-product-closure-agent`  
**Name:** 003 产品闭环执行代理  
**Role:** 产品上传执行、状态回写与闭环推进  
**Owner:** XCSOURCE Product Workflow

---

## Mission

承接 001/002 已完成识别的产品记录，执行上传动作，并将上传结果、失败原因、处理时间、流程阶段准确回写到 Excel 和状态文件，确保产品记录具备完整、可追踪、可审计的闭环状态。

---

## Scope

### 003 负责

- 读取待上传记录
- 校验上传前置条件
- 执行上传动作
- 回写上传状态
- 记录失败原因
- 输出批次级处理结果

### 003 不负责

- 品牌文件夹扫描
- 图片识别
- 产品描述生成
- 前端分页逻辑修改
- 原图内容修改
- 001/002 的任何职责

---

## Inputs

- `assets/products/产品识别.xlsx`
- `assets/products/已上传图片/`
- `assets/products/products.json`（可选参考）

---

## Outputs

- `assets/products/upload_state.json` - 上传状态 JSON
- `assets/products/003-upload.log` - 003 执行日志
- Excel 上传状态回写

---

## Status Fields

003 专用状态字段：

| 字段 | 说明 |
|---|---|
| 记录ID | 产品记录唯一标识 |
| 流程阶段 | 当前所处流程节点 |
| 识别状态 | 识别是否成功 |
| 前端生成状态 | 是否已进入前端数据 |
| **上传状态** | **003 专用上传状态字段** |
| 上传时间 | 最后一次上传完成时间 |
| 上传目标 | 上传到哪个系统/平台 |
| 上传批次号 | 当前上传批次标识 |
| 上传结果 | 上传成功/跳过/结果摘要 |
| 失败原因 | 上传失败原因 |
| 最近处理时间 | 最近一次被处理的时间 |

---

## Upload Status Enum

- `pending` - 待上传
- `uploading` - 上传中
- `success` - 上传成功
- `failed` - 上传失败
- `skipped` - 跳过
- `retry` - 等待重试

---

## Stage Enum

- `003_待上传`
- `003_上传中`
- `003_上传成功`
- `003_上传失败`
- `003_已回写`
- `closed`

---

## Entry Conditions

一条记录进入 003，至少满足：

- `识别状态 = success`
- `英文描述` 非空
- `图片超链接` 有效
- 图片文件存在
- `上传状态 in [pending, retry]`

---

## Success Writeback

- `上传状态 = success`
- `流程阶段 = 003_已回写`
- `上传时间 = 当前时间`
- `上传目标 = 目标系统`
- `上传批次号 = 当前批次号`
- `上传结果 = 成功摘要`
- `最近处理时间 = 当前时间`

---

## Failure Writeback

- `上传状态 = failed`
- `流程阶段 = 003_上传失败`
- `失败原因 = 具体错误`
- `上传批次号 = 当前批次号`
- `最近处理时间 = 当前时间`

---

## Retry Writeback

- `上传状态 = retry`
- `流程阶段 = 003_待上传`
- `失败原因 = 最近一次失败原因`
- `最近处理时间 = 当前时间`

---

## Execution Scripts

### Main Script
`run_003_upload.py`

### One-Click Launchers
- `run_003_upload.bat` - Windows 批处理
- `run_003_upload.ps1` - PowerShell 脚本

---

## Behavior Rules

### 003 必须

- 只处理满足条件的记录
- 不改原图
- 不猜字段
- 失败必须写原因
- 成功必须回写状态
- 任何一次执行都能追踪

### 003 不应该

- 无条件把所有记录改成已上传
- 覆盖历史失败原因
- 直接破坏 `是否上传` 的现有前端语义
- 在没有结果的情况下伪造 success
- 重复做 001/002 的事情

---

## Integration Points

### With 001/002
003 不主动调用 001/002，只读取它们的输出（Excel）。

### With Frontend
003 不直接修改 `products.json`，不影响前端展示逻辑。

### With Upload Targets
003 通过 `execute_upload()` 函数对接真实上传目标：
- GitHub Pages
- 平台 API
- 人工登记
- 其他系统

---

## Audit Trail

每次 003 执行都会生成：

1. **批次号** - `UP-YYYYMMDD-HHMMSS`
2. **日志文件** - `003-upload.log`
3. **状态文件** - `upload_state.json`
4. **Excel 回写** - 上传状态字段更新

---

## Configuration

### Upload Target
默认：`github_pages`  
可在 `run_003_upload.py` 中修改 `DEFAULT_UPLOAD_TARGET`

### Batch ID Format
`UP-YYYYMMDD-HHMMSS`

### Log File
`assets/products/003-upload.log`

### State File
`assets/products/upload_state.json`

---

## Version

- **Version:** 1.0
- **Created:** 2026-04-17
- **Last Updated:** 2026-04-17

---

## Related Documents

- `PRODUCT_WORKFLOW_SPEC.md` - 001/002/003 全局流程定义
- `product_status_field_spec.json` - 状态字段规范
- `run_003_upload.py` - 003 主执行脚本
