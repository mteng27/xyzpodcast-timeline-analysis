#!/usr/bin/env python3
import json

def show_all_podcasts_stats():
    """显示所有播客的统计信息"""
    print(f"\n=== 所有播客数据统计 ===")
    
    with open('all_podcasts_complete_timeline.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"播客总数: {data['metadata']['total_podcasts']:,}")
    print(f"同时有Git数据的播客: {data['metadata']['matched_with_git']:,}")
    print(f"仅Excel数据的播客: {data['metadata']['excel_only']:,}")
    print(f"Git数据匹配率: {data['metadata']['matched_with_git']/data['metadata']['total_podcasts']*100:.1f}%")
    
    # 统计时间跨度
    time_spans = []
    for podcast in data['podcasts'].values():
        time_spans.append(podcast['days_tracked'])
    
    if time_spans:
        print(f"平均跟踪天数: {sum(time_spans)/len(time_spans):.1f} 天")
        print(f"最长跟踪天数: {max(time_spans)} 天")
        print(f"最短跟踪天数: {min(time_spans)} 天")
    
    # 统计分类信息
    categories = {}
    for podcast in data['podcasts'].values():
        category = podcast['basic_info'].get('category', '未知')
        categories[category] = categories.get(category, 0) + 1
    
    print(f"\n分类统计 (前10名):")
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    for i, (category, count) in enumerate(sorted_categories[:10], 1):
        print(f"  {i:2d}. {category}: {count:,} 个播客")

def show_top_growers(limit=20):
    """显示增长率最高的播客"""
    print(f"\n=== 增长率排行榜（前{limit}名）===")
    
    with open('all_podcasts_complete_timeline.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 按增长率排序
    sorted_podcasts = sorted(
        data['podcasts'].values(),
        key=lambda x: x['growth_rate'],
        reverse=True
    )
    
    for i, podcast in enumerate(sorted_podcasts[:limit], 1):
        print(f"{i:2d}. {podcast['podcastName']}")
        print(f"    增长率: {podcast['growth_rate']:+.1f}%")
        print(f"    增长数: {podcast['growth']:+,}")
        print(f"    订阅数: {podcast['start_subscription']:,} → {podcast['end_subscription']:,}")
        print(f"    跟踪天数: {podcast['days_tracked']} 天")
        print(f"    分类: {podcast['basic_info'].get('category', '')}")
        print(f"    作者: {podcast['basic_info'].get('author', '')}")
        print(f"    有Git数据: {podcast['basic_info']['has_git_data']}")
        print()

def show_excel_only_top_growers(limit=10):
    """显示仅Excel数据的高增长播客"""
    print(f"\n=== 仅Excel数据的高增长播客（前{limit}名）===")
    
    with open('all_podcasts_complete_timeline.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 筛选仅Excel数据的播客
    excel_only_podcasts = [
        podcast for podcast in data['podcasts'].values()
        if not podcast['basic_info']['has_git_data']
    ]
    
    # 按增长率排序
    sorted_podcasts = sorted(
        excel_only_podcasts,
        key=lambda x: x['growth_rate'],
        reverse=True
    )
    
    for i, podcast in enumerate(sorted_podcasts[:limit], 1):
        print(f"{i:2d}. {podcast['podcastName']}")
        print(f"    增长率: {podcast['growth_rate']:+.1f}%")
        print(f"    增长数: {podcast['growth']:+,}")
        print(f"    订阅数: {podcast['start_subscription']:,} → {podcast['end_subscription']:,}")
        print(f"    跟踪天数: {podcast['days_tracked']} 天")
        print(f"    分类: {podcast['basic_info'].get('category', '')}")
        print(f"    作者: {podcast['basic_info'].get('author', '')}")
        print()

def show_podcast_timeline(podcast_name):
    """显示特定播客的完整时间线"""
    print(f"正在查找播客: {podcast_name}")
    
    with open('all_podcasts_complete_timeline.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 查找播客
    target_podcast = None
    for podcast in data['podcasts'].values():
        if podcast['podcastName'] == podcast_name:
            target_podcast = podcast
            break
    
    if not target_podcast:
        print(f"未找到播客: {podcast_name}")
        return
    
    print(f"\n=== {podcast_name} 完整订阅变化时间线 ===")
    print(f"播客ID: {target_podcast['podcastID']}")
    print(f"完整时间范围: {target_podcast['start_date']} 到 {target_podcast['end_date']}")
    print(f"跟踪天数: {target_podcast['days_tracked']} 天")
    print(f"总数据点: {target_podcast['total_timeline_points']} 个")
    print(f"Excel数据点: {target_podcast['excel_points']} 个")
    print(f"Git数据点: {target_podcast['git_points']} 个")
    print()
    
    print(f"订阅数变化:")
    print(f"  开始: {target_podcast['start_subscription']:,} 订阅")
    print(f"  结束: {target_podcast['end_subscription']:,} 订阅")
    print(f"  增长: {target_podcast['growth']:+,} 订阅")
    print(f"  增长率: {target_podcast['growth_rate']:+.1f}%")
    print(f"  平均日增长率: {target_podcast['daily_growth_rate']:+.4f}%")
    print()
    
    # 显示基础信息
    basic_info = target_podcast.get('basic_info', {})
    print(f"基础信息:")
    print(f"  分类: {basic_info.get('category', '')}")
    print(f"  作者: {basic_info.get('author', '')}")
    print(f"  描述: {basic_info.get('summary', '')[:100]}...")
    print(f"  专辑ID: {basic_info.get('album_id', '')}")
    print(f"  节目数量: {basic_info.get('track_count', 0)}")
    print(f"  有Git数据: {basic_info.get('has_git_data', False)}")

def main():
    """主函数"""
    print("=== 所有播客完整时间线展示工具 ===")
    
    # 显示统计信息
    show_all_podcasts_stats()
    
    # 显示增长率排行榜
    show_top_growers(10)
    
    # 显示仅Excel数据的高增长播客
    show_excel_only_top_growers(5)
    
    # 显示特定播客的完整时间线
    print(f"\n=== 特定播客完整时间线 ===")
    representative_podcasts = [
        "胡叨叨",  # 增长率最高，有Git数据
        "旷野时刻",  # 增长率第二，仅Excel数据
        "暗送秋波"   # 增长率第三，有Git数据
    ]
    
    for podcast_name in representative_podcasts:
        show_podcast_timeline(podcast_name)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
