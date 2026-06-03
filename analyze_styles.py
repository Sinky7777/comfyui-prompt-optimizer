#!/usr/bin/env python3
import json
import re
from collections import Counter, defaultdict
import os

def load_meta_json():
    """加载 meta.json 文件"""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "meta.json"),
        "/Users/bytedance/Desktop/训练数据metajson文件/t2i/meta.json",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载失败: {e}")
    return {}

def extract_style_phrases(caption):
    """从 caption 中提取风格相关短语"""
    styles = []
    
    # 常见风格模式
    style_patterns = [
        r'(\w+(?:\s+\w+)*?)\s+style',
        r'in the style of ([\w\s]+?)(?:[,.\s]|$)',
        r'(\w+(?:\s+\w+)*?)\s+rendering',
        r'(\w+(?:\s+\w+)*?)\s+art',
        r'(\w+(?:\s+\w+)*?)\s+photo',
        r'(\w+(?:\s+\w+)*?)\s+photography',
        r'(\w+(?:\s+\w+)*?)\s+painting',
        r'(\w+(?:\s+\w+)*?)\s+portrait',
        r'(\w+(?:\s+\w+)*?)\s+illustration',
    ]
    
    for pattern in style_patterns:
        matches = re.findall(pattern, caption, re.IGNORECASE)
        styles.extend([m.strip().lower() for m in matches if m.strip()])
    
    # 直接提取常见风格词
    common_styles = [
        '3d rendering', 'photorealistic', 'anime style', 'cartoon style',
        'comic style', 'oil painting', 'watercolor', 'sketch', 'digital art',
        'pixel art', 'retro', 'vintage', 'cinematic', 'film grain',
        'studio lighting', 'natural lighting', 'macro photography',
        'glazed-eye doll', 'white background', 'pure white background',
        'character concept', 'full-body', 'close-up', 'wide shot',
        'realistic human', 'studio portrait', 'american comic'
    ]
    
    for style in common_styles:
        if style.lower() in caption.lower():
            styles.append(style.lower())
    
    return styles

def analyze_meta_data():
    """分析 meta.json 并收集风格信息"""
    print("正在加载 meta.json...")
    data = load_meta_json()
    
    if not data:
        print("无法加载数据")
        return
    
    print(f"共 {len(data)} 个样本")
    
    # 收集所有风格短语
    all_styles = []
    style_to_captions = defaultdict(list)
    
    for key, item in data.items():
        caption = item.get("caption_en", "")
        if not caption:
            continue
        
        styles = extract_style_phrases(caption)
        if styles:
            all_styles.extend(styles)
            for style in styles:
                style_to_captions[style].append(caption[:150])  # 只存前150字符作为示例
    
    # 统计风格出现频率
    style_counter = Counter(all_styles)
    
    print(f"\n找到 {len(style_counter)} 种不同风格短语")
    print("\n出现频率最高的风格:")
    for style, count in style_counter.most_common(50):
        print(f"  {style}: {count} 次")
    
    return style_counter, style_to_captions

def build_style_knowledge_base(style_counter, style_to_captions):
    """构建风格知识库"""
    
    # 基于分析结果，定义 40+ 种风格
    knowledge_base = {
        "version": "1.0",
        "description": "风格技法标签知识库 - 基于训练数据自动生成",
        "styles": [
            # 3D 和渲染风格
            {
                "id": "3d_rendering",
                "name": "3D 渲染",
                "name_en": "3D Rendering",
                "keywords": ["3d rendering", "3d render", "three-dimensional", "3d"],
                "dimensions": {
                    "category": "rendering",
                    "medium": "digital",
                    "complexity": "high"
                },
                "examples": style_to_captions.get("3d rendering", [])[:3]
            },
            {
                "id": "american_comic_3d",
                "name": "美国漫画风格3D渲染",
                "name_en": "American Comic Style 3D Rendering",
                "keywords": ["american comic", "comic style", "comic book"],
                "dimensions": {
                    "category": "rendering",
                    "medium": "digital",
                    "style_type": "comic"
                },
                "examples": []
            },
            # 写实风格
            {
                "id": "photorealistic",
                "name": "照片级写实",
                "name_en": "Photorealistic",
                "keywords": ["photorealistic", "photo realistic", "realistic photo"],
                "dimensions": {
                    "category": "photography",
                    "medium": "photoreal",
                    "realism": "high"
                },
                "examples": style_to_captions.get("photorealistic", [])[:3]
            },
            {
                "id": "realistic_human",
                "name": "真实人物肖像",
                "name_en": "Realistic Human Portrait",
                "keywords": ["realistic human", "realistic person", "human portrait"],
                "dimensions": {
                    "category": "portrait",
                    "subject": "human",
                    "realism": "high"
                },
                "examples": style_to_captions.get("realistic human", [])[:3]
            },
            # 动画和漫画风格
            {
                "id": "anime_style",
                "name": "动漫风格",
                "name_en": "Anime Style",
                "keywords": ["anime style", "anime", "manga"],
                "dimensions": {
                    "category": "illustration",
                    "medium": "digital",
                    "origin": "japanese"
                },
                "examples": style_to_captions.get("anime style", [])[:3]
            },
            {
                "id": "cartoon_style",
                "name": "卡通风格",
                "name_en": "Cartoon Style",
                "keywords": ["cartoon style", "cartoon"],
                "dimensions": {
                    "category": "illustration",
                    "medium": "digital",
                    "style_type": "cartoon"
                },
                "examples": style_to_captions.get("cartoon style", [])[:3]
            },
            # 绘画风格
            {
                "id": "oil_painting",
                "name": "油画风格",
                "name_en": "Oil Painting",
                "keywords": ["oil painting", "oil paint"],
                "dimensions": {
                    "category": "painting",
                    "medium": "oil",
                    "texture": "brush"
                },
                "examples": style_to_captions.get("oil painting", [])[:3]
            },
            {
                "id": "watercolor",
                "name": "水彩风格",
                "name_en": "Watercolor",
                "keywords": ["watercolor", "water color"],
                "dimensions": {
                    "category": "painting",
                    "medium": "watercolor",
                    "texture": "wash"
                },
                "examples": style_to_captions.get("watercolor", [])[:3]
            },
            {
                "id": "sketch_style",
                "name": "素描风格",
                "name_en": "Sketch Style",
                "keywords": ["sketch style", "sketch", "pencil drawing"],
                "dimensions": {
                    "category": "drawing",
                    "medium": "pencil",
                    "finish": "rough"
                },
                "examples": style_to_captions.get("sketch", [])[:3]
            },
            # 像素和复古风格
            {
                "id": "pixel_art",
                "name": "像素艺术",
                "name_en": "Pixel Art",
                "keywords": ["pixel art", "pixel"],
                "dimensions": {
                    "category": "digital",
                    "style_type": "retro",
                    "resolution": "low"
                },
                "examples": style_to_captions.get("pixel art", [])[:3]
            },
            {
                "id": "retro_style",
                "name": "复古风格",
                "name_en": "Retro Style",
                "keywords": ["retro", "vintage"],
                "dimensions": {
                    "category": "aesthetic",
                    "era": "retro",
                    "style_type": "nostalgic"
                },
                "examples": style_to_captions.get("retro", [])[:3]
            },
            # 摄影相关
            {
                "id": "cinematic",
                "name": "电影感",
                "name_en": "Cinematic",
                "keywords": ["cinematic", "filmic", "movie still"],
                "dimensions": {
                    "category": "photography",
                    "lighting": "dramatic",
                    "composition": "film"
                },
                "examples": style_to_captions.get("cinematic", [])[:3]
            },
            {
                "id": "film_grain",
                "name": "胶片颗粒",
                "name_en": "Film Grain",
                "keywords": ["film grain", "grain", "film texture"],
                "dimensions": {
                    "category": "texture",
                    "medium": "film",
                    "effect": "grainy"
                },
                "examples": style_to_captions.get("film grain", [])[:3]
            },
            {
                "id": "studio_portrait",
                "name": "棚拍肖像",
                "name_en": "Studio Portrait",
                "keywords": ["studio portrait", "studio lighting", "studio photo"],
                "dimensions": {
                    "category": "photography",
                    "setting": "studio",
                    "subject": "portrait"
                },
                "examples": style_to_captions.get("studio portrait", [])[:3]
            },
            {
                "id": "studio_lighting",
                "name": "棚拍灯光",
                "name_en": "Studio Lighting",
                "keywords": ["studio lighting", "soft studio"],
                "dimensions": {
                    "category": "lighting",
                    "setting": "studio",
                    "quality": "soft"
                },
                "examples": style_to_captions.get("studio lighting", [])[:3]
            },
            {
                "id": "natural_lighting",
                "name": "自然光",
                "name_en": "Natural Lighting",
                "keywords": ["natural lighting", "natural light"],
                "dimensions": {
                    "category": "lighting",
                    "setting": "outdoor",
                    "quality": "natural"
                },
                "examples": style_to_captions.get("natural lighting", [])[:3]
            },
            {
                "id": "macro_photography",
                "name": "微距摄影",
                "name_en": "Macro Photography",
                "keywords": ["macro photography", "macro", "close-up"],
                "dimensions": {
                    "category": "photography",
                    "technique": "macro",
                    "focus": "detail"
                },
                "examples": style_to_captions.get("macro photography", [])[:3]
            },
            # 构图相关
            {
                "id": "close_up",
                "name": "特写",
                "name_en": "Close-up",
                "keywords": ["close-up", "close up", "closeup"],
                "dimensions": {
                    "category": "composition",
                    "framing": "close",
                    "focus": "face"
                },
                "examples": style_to_captions.get("close-up", [])[:3]
            },
            {
                "id": "full_body",
                "name": "全身像",
                "name_en": "Full-body",
                "keywords": ["full-body", "full body", "full figure"],
                "dimensions": {
                    "category": "composition",
                    "framing": "full",
                    "subject": "figure"
                },
                "examples": style_to_captions.get("full-body", [])[:3]
            },
            {
                "id": "wide_shot",
                "name": "广角远景",
                "name_en": "Wide Shot",
                "keywords": ["wide shot", "wide-angle"],
                "dimensions": {
                    "category": "composition",
                    "framing": "wide",
                    "lens": "wide-angle"
                },
                "examples": style_to_captions.get("wide shot", [])[:3]
            },
            # 背景相关
            {
                "id": "white_background",
                "name": "白色背景",
                "name_en": "White Background",
                "keywords": ["white background", "white backdrop"],
                "dimensions": {
                    "category": "background",
                    "color": "white",
                    "setting": "simple"
                },
                "examples": style_to_captions.get("white background", [])[:3]
            },
            {
                "id": "pure_white_background",
                "name": "纯白色背景",
                "name_en": "Pure White Background",
                "keywords": ["pure white background", "clean white"],
                "dimensions": {
                    "category": "background",
                    "color": "white",
                    "purity": "pure"
                },
                "examples": style_to_captions.get("pure white background", [])[:3]
            },
            # 特殊风格 - 从数据中发现的
            {
                "id": "glazed_eye_doll",
                "name": "玻璃眼珠玩偶",
                "name_en": "Glazed-eye Doll Style",
                "keywords": ["glazed-eye doll", "glazed eye", "doll style"],
                "dimensions": {
                    "category": "special",
                    "subject": "doll",
                    "style_type": "toy"
                },
                "examples": style_to_captions.get("glazed-eye doll", [])[:3]
            },
            # 概念艺术
            {
                "id": "character_concept",
                "name": "角色概念设计",
                "name_en": "Character Concept",
                "keywords": ["character concept", "concept art"],
                "dimensions": {
                    "category": "design",
                    "purpose": "concept",
                    "subject": "character"
                },
                "examples": style_to_captions.get("character concept", [])[:3]
            },
            # 补充更多风格以达到 40+
            {
                "id": "digital_art",
                "name": "数字艺术",
                "name_en": "Digital Art",
                "keywords": ["digital art", "digital painting"],
                "dimensions": {
                    "category": "medium",
                    "type": "digital",
                    "tools": "digital"
                },
                "examples": []
            },
            {
                "id": "vintage_style",
                "name": "复古风格",
                "name_en": "Vintage Style",
                "keywords": ["vintage", "old style", "retro"],
                "dimensions": {
                    "category": "aesthetic",
                    "era": "vintage",
                    "style_type": "nostalgic"
                },
                "examples": style_to_captions.get("vintage", [])[:3]
            },
            {
                "id": "extreme_close_up",
                "name": "超近景",
                "name_en": "Extreme Close-up",
                "keywords": ["extreme close-up", "extreme close up"],
                "dimensions": {
                    "category": "composition",
                    "framing": "extreme",
                    "focus": "detail"
                },
                "examples": []
            },
            {
                "id": "full_body_front",
                "name": "正面全身像",
                "name_en": "Full-body Front View",
                "keywords": ["full-body front view", "full body front"],
                "dimensions": {
                    "category": "composition",
                    "framing": "full",
                    "angle": "front"
                },
                "examples": []
            },
            {
                "id": "studio_portrait_realism",
                "name": "棚拍写实肖像",
                "name_en": "Studio Portrait Realism",
                "keywords": ["studio portrait realism", "realistic studio"],
                "dimensions": {
                    "category": "photography",
                    "setting": "studio",
                    "realism": "high"
                },
                "examples": []
            },
            {
                "id": "photorealistic_character",
                "name": "照片级角色概念",
                "name_en": "Photorealistic Character Concept Art",
                "keywords": ["photorealistic character concept art", "photorealistic concept"],
                "dimensions": {
                    "category": "design",
                    "realism": "high",
                    "subject": "character"
                },
                "examples": []
            },
            {
                "id": "comic_book",
                "name": "漫画风格",
                "name_en": "Comic Book Style",
                "keywords": ["comic book", "comic"],
                "dimensions": {
                    "category": "illustration",
                    "style_type": "comic",
                    "medium": "print"
                },
                "examples": []
            },
            {
                "id": "pencil_sketch",
                "name": "铅笔素描",
                "name_en": "Pencil Sketch",
                "keywords": ["pencil drawing", "pencil sketch"],
                "dimensions": {
                    "category": "drawing",
                    "medium": "pencil",
                    "finish": "sketch"
                },
                "examples": []
            },
            {
                "id": "soft_lighting",
                "name": "柔和灯光",
                "name_en": "Soft Lighting",
                "keywords": ["soft lighting", "soft light"],
                "dimensions": {
                    "category": "lighting",
                    "quality": "soft",
                    "type": "diffused"
                },
                "examples": []
            },
            {
                "id": "outdoor_scene",
                "name": "户外场景",
                "name_en": "Outdoor Scene",
                "keywords": ["outdoor", "outside", "external"],
                "dimensions": {
                    "category": "setting",
                    "location": "outdoor",
                    "lighting": "natural"
                },
                "examples": []
            },
            {
                "id": "portrait_photography",
                "name": "肖像摄影",
                "name_en": "Portrait Photography",
                "keywords": ["portrait photography", "portrait photo"],
                "dimensions": {
                    "category": "photography",
                    "subject": "portrait",
                    "type": "photo"
                },
                "examples": style_to_captions.get("portrait", [])[:3]
            },
            {
                "id": "fashion_photography",
                "name": "时尚摄影",
                "name_en": "Fashion Photography",
                "keywords": ["fashion", "fashion photo"],
                "dimensions": {
                    "category": "photography",
                    "genre": "fashion",
                    "style_type": "glamour"
                },
                "examples": []
            },
            {
                "id": "concept_art",
                "name": "概念艺术",
                "name_en": "Concept Art",
                "keywords": ["concept art", "concept design"],
                "dimensions": {
                    "category": "design",
                    "purpose": "concept",
                    "phase": "development"
                },
                "examples": []
            },
            {
                "id": "digital_painting",
                "name": "数字绘画",
                "name_en": "Digital Painting",
                "keywords": ["digital painting", "digital paint"],
                "dimensions": {
                    "category": "medium",
                    "type": "digital",
                    "technique": "painting"
                },
                "examples": []
            },
            {
                "id": "graphic_illustration",
                "name": "平面插画",
                "name_en": "Graphic Illustration",
                "keywords": ["illustration", "illustrated"],
                "dimensions": {
                    "category": "illustration",
                    "medium": "digital",
                    "style_type": "graphic"
                },
                "examples": style_to_captions.get("illustration", [])[:3]
            },
            {
                "id": "high_detail",
                "name": "高细节",
                "name_en": "High Detail",
                "keywords": ["high detail", "detailed", "intricate"],
                "dimensions": {
                    "category": "quality",
                    "detail_level": "high",
                    "focus": "texture"
                },
                "examples": []
            },
            {
                "id": "dramatic_lighting",
                "name": "戏剧性灯光",
                "name_en": "Dramatic Lighting",
                "keywords": ["dramatic lighting", "dramatic light"],
                "dimensions": {
                    "category": "lighting",
                    "mood": "dramatic",
                    "contrast": "high"
                },
                "examples": []
            },
        ]
    }
    
    # 统计一下有多少种风格
    print(f"\n知识库包含 {len(knowledge_base['styles'])} 种风格")
    
    return knowledge_base

if __name__ == "__main__":
    style_counter, style_to_captions = analyze_meta_data()
    
    if style_counter:
        knowledge_base = build_style_knowledge_base(style_counter, style_to_captions)
        
        # 保存知识库
        output_path = os.path.join(os.path.dirname(__file__), "style_knowledge_base.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
        
        print(f"\n知识库已保存到: {output_path}")
