#!/usr/bin/env python3
import json
import pandas as pd
from datetime import datetime
from collections import defaultdict

def main():
    print("=== 为所有播客创建完整订阅变化时间线 ===")
    
    # 读取Excel数据
    print("正在读取Excel文件...")
    df = pd.read_excel("小宇宙专辑资料-all.xlsx")
    print(f"Excel数据时间范围: {df['get_time'].min()} 到 {df['get_time'].max()}")
    print(f"Excel中的播客总数: {df['album_name'].nunique()}")
    
    # 按播客名称和时间分组，创建订阅变化时间线
    podcast_timelines = defaultdict(list)
    
    for _, row in df.iterrows():
        podcast_name = str(row['album_name'])
        get_time = str(row['get_time']).split('T')[0]  # 只取日期部分
        subscribe_count = int(row['subscribe_count']) if pd.notna(row['subscribe_count']) else 0
        
        podcast_timelines[podcast_name].append({
            'date': get_time,
            'subscription': subscribe_count,
            'album_id': str(row['album_id']),
            'category': str(row['category']) if pd.notna(row['category']) else '',
            'author': str(row['author_name']) if pd.notna(row['author_name']) else '',
            'summary': str(row['summary']) if pd.notna(row['summary']) else '',
            'track_count': int(row['track_count']) if pd.notna(row['track_count']) else 0
        })
    
    # 对每个播客的时间线按日期排序
    for podcast_name in podcast_timelines:
        podcast_timelines[podcast_name].sort(key=lambda x: x['date'])
    
    print(f"成功创建 {len(podcast_timelines)} 个播客的Excel时间线")
    
    # 读取Git历史数据（如果有的话）
    git_data = None
    try:
        with open('podcast_growth_analysis.json', 'r', encoding='utf-8') as f:
            git_data = json.load(f)
        print(f"Git数据中的播客总数: {len(git_data['podcasts'])}")
    except:
        print("未找到Git数据文件，将只使用Excel数据")
    
    # 创建完整的时间线数据
    complete_data = {
        "metadata": {
            "data_sources": {
                "excel": {
                    "file": "小宇宙专辑资料-all.xlsx",
                    "time_range": {
                        "start": df['get_time'].min(),
                        "end": df['get_time'].max()
                    },
                    "podcast_count": len(podcast_timelines)
                }
            },
            "creation_time": datetime.now().isoformat()
        },
        "podcasts": {}
    }
    
    if git_data:
        complete_data["metadata"]["data_sources"]["git"] = {
            "time_range": git_data["metadata"]["date_range"],
            "podcast_count": len(git_data["podcasts"])
        }
    
    # 为所有Excel播客创建时间线
    matched_with_git = 0
    excel_only = 0
    
    for podcast_name, excel_timeline in podcast_timelines.items():
        # 查找Git中的对应播客
        git_podcast = None
        if git_data:
            for git_id, git_podcast_data in git_data["podcasts"].items():
                if git_podcast_data["podcastName"] == podcast_name:
                    git_podcast = git_podcast_data
                    break
        
        # 合并时间线数据
        complete_timeline = []
        
        # 添加Excel数据
        for point in excel_timeline:
            complete_timeline.append({
                "date": point['date'],
                "subscription": point['subscription'],
                "source": "excel",
                "category": point['category'],
                "author": point['author'],
                "summary": point['summary'],
                "track_count": point['track_count']
            })
        
        # 添加Git数据（如果有的话）
        if git_podcast:
            for point in git_podcast["timeline"]:
                complete_timeline.append({
                    "date": point['date'],
                    "subscription": point['subscription'],
                    "source": "git"
                })
            matched_with_git += 1
        else:
            excel_only += 1
        
        # 按日期排序
        complete_timeline.sort(key=lambda x: x['date'])
        
        # 计算完整时间线的增长数据
        if complete_timeline:
            first_point = complete_timeline[0]
            last_point = complete_timeline[-1]
            
            start_subscription = first_point['subscription']
            end_subscription = last_point['subscription']
            growth = end_subscription - start_subscription
            growth_rate = (growth / start_subscription) * 100 if start_subscription > 0 else 0
            
            # 计算时间跨度
            start_date = first_point['date']
            end_date = last_point['date']
            days_diff = (datetime.strptime(end_date, '%Y-%m-%d') - 
                       datetime.strptime(start_date, '%Y-%m-%d')).days
            daily_growth_rate = growth_rate / days_diff if days_diff > 0 else 0
            
            # 创建播客ID（使用专辑ID或生成一个）
            podcast_id = first_point.get('album_id', f"excel_{hash(podcast_name) % 1000000}")
            
            complete_podcast = {
                "podcastID": podcast_id,
                "podcastName": podcast_name,
                "start_date": start_date,
                "end_date": end_date,
                "start_subscription": start_subscription,
                "end_subscription": end_subscription,
                "growth": growth,
                "growth_rate": growth_rate,
                "daily_growth_rate": daily_growth_rate,
                "days_tracked": days_diff,
                "total_timeline_points": len(complete_timeline),
                "excel_points": len([p for p in complete_timeline if p.get('source') == 'excel']),
                "git_points": len([p for p in complete_timeline if p.get('source') == 'git']),
                "timeline": complete_timeline,
                "basic_info": {
                    "category": first_point.get('category', ''),
                    "author": first_point.get('author', ''),
                    "summary": first_point.get('summary', ''),
                    "track_count": first_point.get('track_count', 0),
                    "album_id": first_point.get('album_id', ''),
                    "has_git_data": git_podcast is not None
                }
            }
            
            complete_data["podcasts"][podcast_id] = complete_podcast
    
    complete_data["metadata"]["total_podcasts"] = len(complete_data["podcasts"])
    complete_data["metadata"]["matched_with_git"] = matched_with_git
    complete_data["metadata"]["excel_only"] = excel_only
    
    # 保存完整数据
    output_file = "all_podcasts_complete_timeline.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== 整合完成 ===")
    print(f"Excel播客总数: {len(podcast_timelines)}")
    print(f"成功创建时间线的播客: {len(complete_data['podcasts'])}")
    print(f"同时有Git数据的播客: {matched_with_git}")
    print(f"仅Excel数据的播客: {excel_only}")
    print(f"Git数据匹配率: {matched_with_git/len(complete_data['podcasts'])*100:.1f}%")
    print(f"输出文件: {output_file}")
    
    # 显示示例
    print(f"\n=== 完整时间线示例 ===")
    sorted_podcasts = sorted(
        complete_data["podcasts"].values(),
        key=lambda x: x['growth_rate'],
        reverse=True
    )
    
    for i, podcast in enumerate(sorted_podcasts[:5], 1):
        print(f"\n{i}. {podcast['podcastName']}")
        print(f"   完整时间线: {podcast['start_date']} 到 {podcast['end_date']}")
        print(f"   跟踪天数: {podcast['days_tracked']} 天")
        print(f"   总数据点: {podcast['total_timeline_points']} 个")
        print(f"   Excel数据点: {podcast['excel_points']} 个")
        print(f"   Git数据点: {podcast['git_points']} 个")
        print(f"   增长率: {podcast['growth_rate']:+.1f}%")
        print(f"   订阅数: {podcast['start_subscription']:,} → {podcast['end_subscription']:,}")
        print(f"   有Git数据: {podcast['basic_info']['has_git_data']}")

if __name__ == "__main__":
    main()
