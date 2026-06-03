# ComfyUI 提示词优化器节点

这是一个为 ComfyUI 设计的提示词优化器节点，它能够根据 meta.json 中的样本提示词来优化用户输入的图片生成提示词。

## 功能特性

1. **Prompt Optimizer (提示词优化器)**: 根据用户输入的提示词，自动匹配相关风格并优化提示词
2. **Meta Data Loader (元数据加载器)**: 加载和管理 meta.json 数据文件

## 安装

1. 将此文件夹复制到 ComfyUI 的 `custom_nodes` 目录中
2. 重启 ComfyUI
3. 节点会自动加载，在节点菜单的 "prompt" 分类中可以找到

## 使用方法

### Prompt Optimizer (提示词优化器)

输入参数:
- `prompt`: 需要优化的原始提示词（多行文本）
- `style_mode`: 风格输出模式
  - `auto`: 自动模式
  - `chinese`: 仅中文
  - `english`: 仅英文
- `sample_count`: 匹配样本数量（1-8）

输出:
- `optimized_prompt`: 优化后的提示词
- `matched_styles`: 匹配到的风格锚点

### Meta Data Loader (元数据加载器)

输入参数:
- `meta_json_path`: meta.json 文件路径（可选，留空则使用默认路径）

输出:
- `meta_data`: 加载的 JSON 数据
- `status`: 加载状态信息

## meta.json 文件格式

节点会自动从以下位置查找 meta.json:
1. 当前节点目录下的 meta.json
2. 当前节点目录下的 t2i/meta.json
3. /Users/bytedance/Desktop/训练数据metajson文件/t2i/meta.json

meta.json 格式示例:
```json
{
  "image_1": {
    "image": "https://...",
    "caption_en": "这是英文提示词样本...",
    "aes_idx": [4, 6, 8]
  }
}
```

## 风格词映射

节点内置了以下风格词映射:
- 美国漫画风格的三维渲染图 → American comic style 3D rendering
- 三维渲染图 → 3D rendering
- 纯白色背景 → pure white background
- 正面全身像 → full-body front view
- 角色人物概念图 → character concept art
- 柔和均匀的演播室光照 → soft studio lighting
- 电影感 → cinematic
- 胶片颗粒 → film grain
- 特写 → close-up
- 超近景 → extreme close-up
- 广角远景 → wide shot
- 油画风格 → oil painting
- 水彩风格 → watercolor
- 动漫风格 → anime style
- 素描风格 → sketch style
- 真人写实风格 → realistic human portrait
