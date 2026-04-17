#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
003 产品上传执行与状态回写脚本
读取待上传记录，执行上传动作，回写状态到 Excel 和 JSON
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from openpyxl import load_workbook
from openpyxl.styles import Alignment

# 配置
PROJECT_ROOT = Path(r"C:\Users\Win11\Desktop\XCSOURCE")
PRODUCTS_DIR = PROJECT_ROOT / "assets" / "products"
EXCEL_PATH = PRODUCTS_DIR / "产品识别.xlsx"
UPLOAD_STATE_FILE = PRODUCTS_DIR / "upload_state.json"
LOG_FILE = PRODUCTS_DIR / "003-upload.log"

# 上传目标配置（示例）
DEFAULT_UPLOAD_TARGET = "github_pages"


def log(msg: str):
    """写日志"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_upload_state() -> Dict[str, Dict]:
    """加载上传状态文件"""
    if UPLOAD_STATE_FILE.exists():
        try:
            with open(UPLOAD_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log(f"加载上传状态文件失败: {e}")
            return {}
    return {}


def save_upload_state(state: Dict[str, Dict]):
    """保存上传状态文件"""
    try:
        with open(UPLOAD_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"保存上传状态文件失败: {e}")


def get_header_map(ws) -> Dict[str, int]:
    """获取表头映射"""
    headers = {}
    for col in range(1, ws.max_column + 1):
        cell_value = ws.cell(1, col).value
        if cell_value:
            headers[str(cell_value).strip()] = col
    return headers


def read_pending_records(ws, header_map: Dict[str, int]) -> List[Dict]:
    """
    读取待上传记录
    筛选条件：
    - 上传状态 in [pending, retry]
    - 识别状态 = success
    - 英文描述非空
    - 图片超链接非空
    """
    records = []
    
    required_fields = ["序号", "图片超链接", "英文描述", "识别状态", "上传状态"]
    missing = [f for f in required_fields if f not in header_map]
    if missing:
        log(f"Excel 缺少必要字段: {', '.join(missing)}")
        return records

    for row_num in range(2, ws.max_row + 1):
        try:
            seq = ws.cell(row_num, header_map["序号"]).value
            image_link = ws.cell(row_num, header_map["图片超链接"]).value
            en_desc = ws.cell(row_num, header_map["英文描述"]).value
            recog_status = ws.cell(row_num, header_map["识别状态"]).value
            upload_status = ws.cell(row_num, header_map["上传状态"]).value

            # 筛选条件
            if not en_desc or not str(en_desc).strip():
                continue
            if not image_link:
                continue
            if str(recog_status).strip() != "success":
                continue
            if str(upload_status).strip() not in ["pending", "retry"]:
                continue

            records.append({
                "row": row_num,
                "序号": seq,
                "图片超链接": image_link,
                "英文描述": en_desc,
                "识别状态": recog_status,
                "上传状态": upload_status,
            })
        except Exception as e:
            log(f"读取第 {row_num} 行失败: {e}")
            continue

    return records


def execute_upload(record: Dict) -> Dict[str, str]:
    """
    执行上传动作
    返回: {"status": "success|failed|skipped", "result": "...", "error": "..."}
    
    TODO: 在这里实现真实的上传逻辑
    - 上传到 GitHub Pages
    - 上传到平台
    - 调用 API
    - 等等
    """
    # 示例：这里只是占位符，实际上传逻辑由你补充
    try:
        # 模拟上传成功
        log(f"  [模拟上传] 序号 {record['序号']}: {record['英文描述']}")
        
        # TODO: 替换为真实上传逻辑
        # 例如：
        # - 调用 GitHub API
        # - 上传到 S3
        # - 调用平台接口
        # - 等等
        
        return {
            "status": "success",
            "result": "模拟上传成功",
            "error": ""
        }
    except Exception as e:
        return {
            "status": "failed",
            "result": "",
            "error": str(e)
        }


def writeback_excel(ws, header_map: Dict[str, int], record: Dict, upload_result: Dict, batch_id: str):
    """回写 Excel 上传状态"""
    row = record["row"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "上传状态" in header_map:
        ws.cell(row, header_map["上传状态"], upload_result["status"])
    
    if "流程阶段" in header_map:
        if upload_result["status"] == "success":
            ws.cell(row, header_map["流程阶段"], "003_已回写")
        elif upload_result["status"] == "failed":
            ws.cell(row, header_map["流程阶段"], "003_上传失败")
    
    if "上传时间" in header_map and upload_result["status"] == "success":
        ws.cell(row, header_map["上传时间"], now)
    
    if "上传目标" in header_map:
        ws.cell(row, header_map["上传目标"], DEFAULT_UPLOAD_TARGET)
    
    if "上传批次号" in header_map:
        ws.cell(row, header_map["上传批次号"], batch_id)
    
    if "上传结果" in header_map:
        ws.cell(row, header_map["上传结果"], upload_result["result"])
    
    if "失败原因" in header_map and upload_result["status"] == "failed":
        ws.cell(row, header_map["失败原因"], upload_result["error"])
    
    if "最近处理时间" in header_map:
        ws.cell(row, header_map["最近处理时间"], now)

    # 设置对齐
    for col in header_map.values():
        ws.cell(row, col).alignment = Alignment(vertical="center", wrap_text=True)


def writeback_json(state: Dict, record: Dict, upload_result: Dict, batch_id: str):
    """回写 JSON 状态文件"""
    record_id = f"PRD-{record['序号']}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    state[record_id] = {
        "upload_status": upload_result["status"],
        "stage": "003_已回写" if upload_result["status"] == "success" else "003_上传失败",
        "upload_target": DEFAULT_UPLOAD_TARGET,
        "uploaded_at": now if upload_result["status"] == "success" else "",
        "batch_id": batch_id,
        "result": upload_result["result"],
        "error": upload_result["error"],
        "last_processed_at": now,
    }


def run_003_upload():
    """003 主执行流程"""
    log("=" * 60)
    log("003 产品上传执行开始")

    if not EXCEL_PATH.exists():
        log(f"错误: Excel 文件不存在 - {EXCEL_PATH}")
        return

    # 生成批次号
    batch_id = f"UP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    log(f"批次号: {batch_id}")

    # 加载 Excel
    wb = load_workbook(EXCEL_PATH)
    ws = wb[wb.sheetnames[0]]
    header_map = get_header_map(ws)

    # 读取待上传记录
    records = read_pending_records(ws, header_map)
    log(f"找到待上传记录: {len(records)} 条")

    if not records:
        log("没有待上传记录")
        log("=" * 60)
        return

    # 加载上传状态
    upload_state = load_upload_state()

    # 执行上传与回写
    success_count = 0
    failed_count = 0
    skipped_count = 0

    for record in records:
        log(f"处理记录: 序号 {record['序号']}")
        
        # 执行上传
        upload_result = execute_upload(record)
        
        # 回写 Excel
        writeback_excel(ws, header_map, record, upload_result, batch_id)
        
        # 回写 JSON
        writeback_json(upload_state, record, upload_result, batch_id)
        
        # 统计
        if upload_result["status"] == "success":
            success_count += 1
            log(f"  ✓ 上传成功")
        elif upload_result["status"] == "failed":
            failed_count += 1
            log(f"  ✗ 上传失败: {upload_result['error']}")
        else:
            skipped_count += 1
            log(f"  - 跳过")

    # 保存 Excel
    wb.save(EXCEL_PATH)
    log(f"已保存 Excel: {EXCEL_PATH}")

    # 保存 JSON 状态
    save_upload_state(upload_state)
    log(f"已保存上传状态: {UPLOAD_STATE_FILE}")

    # 汇总
    log("")
    log(f"批次 {batch_id} 完成:")
    log(f"  成功: {success_count}")
    log(f"  失败: {failed_count}")
    log(f"  跳过: {skipped_count}")
    log(f"  总计: {len(records)}")
    log("=" * 60)


def main():
    try:
        run_003_upload()
    except Exception as e:
        log(f"003 执行出错: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
