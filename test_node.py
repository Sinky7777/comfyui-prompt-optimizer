#!/usr/bin/env python3
"""
简单的测试脚本，用于验证ComfyUI节点功能
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from prompt_optimizer import PromptOptimizer, MetaDataLoader

def test_meta_data_loader():
    """测试元数据加载器"""
    print("=" * 50)
    print("测试 MetaDataLoader")
    print("=" * 50)
    
    loader = MetaDataLoader()
    data, status = loader.load_meta()
    
    print(f"加载状态: {status}")
    if data:
        print(f"加载了 {len(data)} 个样本")
        # 打印前几个样本的信息
        for i, (key, item) in enumerate(list(data.items())[:3]):
            print(f"\n样本 {i+1} ({key}):")
            caption = item.get("caption_en", "")
            if len(caption) > 100:
                caption = caption[:100] + "..."
            print(f"  提示词: {caption}")
    
    print("\n")
    return data

def test_prompt_optimizer():
    """测试提示词优化器"""
    print("=" * 50)
    print("测试 PromptOptimizer")
    print("=" * 50)
    
    optimizer = PromptOptimizer()
    
    # 测试用例1: 带风格词的提示词
    test_prompt_1 = """
    生成一张角色人物概念图。正面全身像，纯白色背景，美国漫画风格的三维渲染图，基本信息：男性，49岁中年，高加索人种，现代都市，电视游戏节目主持人。
    """
    
    print("测试用例1 - 带风格词:")
    print(f"原始提示词: {test_prompt_1.strip()}")
    
    optimized, matched_styles = optimizer.optimize_prompt(test_prompt_1, "auto", 5)
    
    print(f"\n匹配的风格: {matched_styles}")
    print(f"\n优化后的提示词: {optimized}")
    print("\n" + "-" * 50 + "\n")
    
    # 测试用例2: 真实人物提示词
    test_prompt_2 = """
    生成一张角色人物概念图。正面全身像，纯白色背景，基本信息：女性，25岁青年，东亚裔，现代都市，自律的健身爱好者。面部特征：轮廓清晰的健康脸型，下颌线紧致分明，肤色是带有自然光泽感的小麦色。
    """
    
    print("测试用例2 - 真实人物:")
    print(f"原始提示词: {test_prompt_2.strip()}")
    
    optimized, matched_styles = optimizer.optimize_prompt(test_prompt_2, "auto", 5)
    
    print(f"\n匹配的风格: {matched_styles}")
    print(f"\n优化后的提示词: {optimized}")

if __name__ == "__main__":
    print("ComfyUI 提示词优化器节点 - 测试脚本")
    print("=" * 50 + "\n")
    
    # 先测试数据加载
    data = test_meta_data_loader()
    
    if data:
        # 再测试优化器
        test_prompt_optimizer()
    else:
        print("警告: 未能加载meta.json数据，部分测试可能无法正常进行")
        test_prompt_optimizer()
    
    print("\n" + "=" * 50)
    print("测试完成！")
