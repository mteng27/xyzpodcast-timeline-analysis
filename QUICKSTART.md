# 快速开始指南

## 安装依赖

```bash
pip install -r requirements.txt
```

## 查看数据

```bash
# 查看所有播客的统计信息和排行榜
python3 show_all_podcasts.py
```

## 数据结构

核心数据文件 `all_podcasts_complete_timeline.json` 包含：

- **7,378个播客**的完整订阅变化时间线
- **最长336天**的跟踪数据
- **19个分类**的播客分布
- **基础信息**：分类、作者、描述等

## 示例数据

```json
{
  "podcastID": "excel_123456",
  "podcastName": "播客名称",
  "start_date": "2024-09-18",
  "end_date": "2025-08-20",
  "start_subscription": 100,
  "end_subscription": 1000,
  "growth": 900,
  "growth_rate": 900.0,
  "daily_growth_rate": 2.5,
  "days_tracked": 336,
  "timeline": [...],
  "basic_info": {
    "category": "自我成长",
    "author": "作者名",
    "summary": "播客描述",
    "has_git_data": true
  }
}
```

## 主要发现

- **最高增长率**: +20,757.1% (胡叨叨)
- **最多播客分类**: 自我成长 (1,425个)
- **平均跟踪天数**: 175天
- **Git数据匹配率**: 14.1%
