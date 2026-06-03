import json
import os
import re
from typing import Dict, List, Tuple

class PromptOptimizer:
    """
    ComfyUI节点：提示词优化器
    根据meta.json中的样本提示词，优化用户输入的图片生成提示词
    """
    
    def __init__(self):
        self.meta_data = {}
        self.captions = []
        self.load_meta_data()
    
    def load_meta_data(self):
        """加载meta.json文件"""
        # 尝试从多个位置加载meta.json
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "meta.json"),
            os.path.join(os.path.dirname(__file__), "t2i", "meta.json"),
            "/Users/bytedance/Desktop/训练数据metajson文件/t2i/meta.json",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self.meta_data = json.load(f)
                    print(f"Loaded meta data from: {path}")
                    # 提取所有caption_en
                    self.captions = []
                    for key, item in self.meta_data.items():
                        if isinstance(item, dict) and "caption_en" in item:
                            self.captions.append(item["caption_en"])
                    break
                except Exception as e:
                    print(f"Failed to load {path}: {e}")
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "请输入您的提示词...",
                }),
                "style_mode": (["auto", "chinese", "english"], {
                    "default": "auto",
                }),
                "sample_count": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 8,
                    "step": 1,
                }),
            },
            "optional": {
                "optional_prompt": ("STRING", {
                    "multiline": True,
                    "forceInput": True,
                }),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("optimized_prompt", "matched_styles",)
    FUNCTION = "optimize_prompt"
    CATEGORY = "prompt"
    
    # 风格词映射
    STYLE_MAPPING = {
        "美国漫画风格的三维渲染图": "American comic style 3D rendering",
        "三维渲染图": "3D rendering",
        "纯白色背景": "pure white background",
        "白色背景": "white background",
        "正面全身像": "full-body front view",
        "角色人物概念图": "character concept art",
        "柔和均匀的演播室光照": "soft studio lighting",
        "电影感": "cinematic",
        "胶片颗粒": "film grain",
        "特写": "close-up",
        "超近景": "extreme close-up",
        "广角远景": "wide shot",
        "油画风格": "oil painting",
        "水彩风格": "watercolor",
        "动漫风格": "anime style",
        "素描风格": "sketch style",
        "真人写实风格": "realistic human portrait",
        "真实人物": "realistic human portrait",
        "写实": "photorealistic",
        "棚拍": "studio portrait",
    }
    
    # 人脸关键词映射
    FACE_KEYWORDS = {
        "脸型": ["facial bone structure", "jawline", "cheekbones", "brow ridge"],
        "轮廓": ["facial bone structure", "jawline"],
        "方正脸": ["square jawline", "angular jawline", "distinct jawline"],
        "硬朗脸": ["square jawline", "angular jawline"],
        "瓜子脸": ["narrow chin", "delicate facial structure"],
        "精致脸型": ["narrow chin", "delicate facial structure"],
        "杏眼": ["almond-shaped eyes"],
        "凤眼": ["slightly upturned eyes"],
        "眼尾上挑": ["slightly upturned eyes"],
        "深褐色瞳孔": ["dark brown irises"],
        "野生眉": ["natural thick eyebrows"],
        "浓眉": ["natural thick eyebrows"],
        "高马尾": ["high ponytail"],
        "小麦色肤色": ["warm wheat-toned skin", "healthy tan skin"],
        "哑光裸色唇": ["matte nude lips"],
        "健康光泽": ["clean skin texture", "subtle natural sheen"],
    }
    
    # 常见构图和光影词
    COMPOSITION_WORDS = [
        "full-body", "front view", "close-up", "wide shot", "portrait",
        "macro photography", "outdoor", "natural lighting", "studio lighting"
    ]
    
    def extract_keywords(self, prompt: str) -> List[str]:
        """从提示词中提取关键词"""
        keywords = []
        
        # 检查风格词
        for cn, en in self.STYLE_MAPPING.items():
            if cn in prompt:
                keywords.extend(en.lower().split())
        
        # 检查人脸关键词
        for cn, ens in self.FACE_KEYWORDS.items():
            if cn in prompt:
                for en in ens:
                    keywords.extend(en.lower().split())
        
        # 检查构图词
        for word in self.COMPOSITION_WORDS:
            if word.lower() in prompt.lower():
                keywords.append(word.lower())
        
        return list(set(keywords))
    
    def find_matching_samples(self, keywords: List[str], top_k: int = 5) -> List[Tuple[int, str]]:
        """找到最匹配的样本"""
        if not self.captions:
            return []
        
        matches = []
        for caption in self.captions:
            if not caption:
                continue
            
            caption_lower = caption.lower()
            score = sum(1 for kw in keywords if kw in caption_lower)
            
            if score > 0:
                matches.append((score, caption))
        
        # 按分数排序
        matches.sort(reverse=True, key=lambda x: x[0])
        return matches[:top_k]
    
    def extract_style_anchors(self, samples: List[Tuple[int, str]]) -> List[str]:
        """从匹配的样本中提取风格锚点"""
        style_anchors = []
        
        # 从样本中收集常见短语
        if self.captions:
            # 收集所有样本中的短语
            all_text = " ".join(self.captions).lower()
            
            # 检查常见风格短语是否在样本中存在
            common_phrases = [
                "3D rendering", "American comic style", "white background",
                "pure white background", "soft studio lighting", "cinematic",
                "film grain", "close-up", "full-body front view",
                "full-body front-facing view", "anime style", "oil painting",
                "watercolor", "sketch style", "realistic human portrait",
                "photorealistic", "photorealistic character concept art",
                "studio portrait realism", "macro photography",
                "glazed-eye doll style", "natural lighting"
            ]
            
            for phrase in common_phrases:
                if phrase.lower() in all_text and phrase not in style_anchors:
                    style_anchors.append(phrase)
        
        return style_anchors
    
    def find_valid_style_anchors(self, desired_styles: List[str]) -> List[str]:
        """找出在meta.json中实际存在的风格锚点"""
        valid_anchors = []
        
        if not self.captions:
            return valid_anchors
        
        all_text = " ".join(self.captions).lower()
        
        for style in desired_styles:
            if style.lower() in all_text:
                valid_anchors.append(style)
        
        return valid_anchors
    
    def optimize_prompt(self, prompt: str, style_mode: str = "auto", sample_count: int = 5, optional_prompt: str = None) -> Tuple[str, str]:
        """
        优化提示词的主函数
        """
        # 如果有可选输入，优先使用可选输入
        if optional_prompt is not None and optional_prompt.strip():
            input_prompt = optional_prompt
        else:
            input_prompt = prompt
        
        # 提取关键词
        keywords = self.extract_keywords(input_prompt)
        
        # 找到匹配样本
        samples = self.find_matching_samples(keywords, sample_count)
        
        # 提取风格锚点
        style_anchors = self.extract_style_anchors(samples)
        
        # 优化提示词
        optimized = self._rewrite_prompt(input_prompt, style_anchors, style_mode)
        
        # 准备风格锚点输出
        matched_styles_str = ", ".join(style_anchors) if style_anchors else "未找到匹配的风格锚点"
        
        return (optimized, matched_styles_str,)
    
    def _rewrite_prompt(self, prompt: str, style_anchors: List[str], style_mode: str) -> str:
        """重写提示词"""
        # 清理输入提示词
        cleaned = self._clean_prompt(prompt)
        
        # 构建优化后的提示词
        parts = []
        
        # 添加风格锚点
        if style_anchors and style_mode != "chinese":
            parts.append(", ".join(style_anchors))
        
        # 添加清理后的主体内容
        parts.append(cleaned)
        
        # 合并并微调
        result = ". ".join(parts)
        result = self._fine_tune(result)
        
        return result
    
    def _clean_prompt(self, prompt: str) -> str:
        """清理提示词"""
        # 删除章节标题（如"基本信息："、"面部特征："等）
        cleaned = re.sub(r'[^\n：:]+[：:]\s*', '', prompt, flags=re.MULTILINE)
        
        # 删除空行和多余空格
        cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def _fine_tune(self, prompt: str) -> str:
        """微调优化后的提示词"""
        # 确保标点正确
        prompt = prompt.replace("。.", "。").replace("..", ".")
        prompt = prompt.replace("，,", "，").replace(",,", ",")
        prompt = prompt.replace("。,", "，").replace(".,", ",")
        
        # 去除开头多余的标点
        prompt = prompt.lstrip(".,。，")
        
        # 合并重复的风格描述
        return prompt.strip()


class MetaDataLoader:
    """
    辅助节点：加载和管理meta.json数据
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "meta_json_path": ("STRING", {
                    "default": "",
                }),
            },
        }
    
    RETURN_TYPES = ("JSON", "STRING",)
    RETURN_NAMES = ("meta_data", "status",)
    FUNCTION = "load_meta"
    CATEGORY = "prompt"
    
    def load_meta(self, meta_json_path: str = ""):
        """加载meta.json"""
        status = ""
        data = {}
        
        if not meta_json_path:
            # 尝试默认路径
            possible_paths = [
                os.path.join(os.path.dirname(__file__), "meta.json"),
                os.path.join(os.path.dirname(__file__), "t2i", "meta.json"),
                "/Users/bytedance/Desktop/训练数据metajson文件/t2i/meta.json",
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    meta_json_path = path
                    break
        
        if meta_json_path and os.path.exists(meta_json_path):
            try:
                with open(meta_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                status = f"成功加载: {meta_json_path}"
            except Exception as e:
                status = f"加载失败: {str(e)}"
        else:
            status = "未找到meta.json文件"
        
        return (data, status,)

