# ComfyUI 提示词优化器 - 使用指南

## 📦 安装步骤

1. 将整个 `风格技法标签节点` 文件夹复制到 ComfyUI 的 `custom_nodes` 目录下
2. 重启 ComfyUI
3. 节点会自动加载！

## 🔍 节点位置

在 ComfyUI 节点菜单中，找到 **prompt** 分类，您会看到：
- **Prompt Optimizer (提示词优化器)** - 主节点
- **Meta Data Loader (元数据加载器)** - 辅助节点

## 🔗 连接上游节点

### 方式一：直接输入（最简单）
直接在 Prompt Optimizer 节点的 `prompt` 输入框中输入您的提示词。

### 方式二：从其他文本节点输入
您可以连接以下类型的上游节点：
- 任何输出 `STRING` 类型的节点
- 其他提示词生成节点
- 文本加载节点

**连接方法：** 将上游节点的输出端口连接到 Prompt Optimizer 的 `prompt` 输入端口。

## 🔗 连接下游节点

### 方式一：连接到 KSampler 等采样节点
将 `optimized_prompt` 输出连接到 KSampler 的 `positive` (正向提示词) 输入。

### 方式二：连接到 CLIP Text Encode
将 `optimized_prompt` 输出连接到 CLIP Text Encode 的 `text` 输入。

### 方式三：连接到其他文本处理节点
可以继续连接到其他需要字符串输入的节点进行进一步处理。

## 🎯 典型工作流示例

### 工作流 1：简单文生图
```
[您的提示词] 
    ↓
[Prompt Optimizer] 
    ↓ (optimized_prompt)
[CLIP Text Encode (Positive)]
    ↓
[KSampler]
    ↓
[VAE Decode]
    ↓
[Save Image]
```

### 工作流 2：带预览的优化
```
[您的提示词] 
    ↓
[Prompt Optimizer] 
    ├→ (optimized_prompt) → [CLIP Text Encode] → [KSampler] → ...
    └→ (matched_styles) → [显示文本的节点]
```

## 📊 参数说明

### Prompt Optimizer 参数
- **prompt**: 输入的原始提示词（多行文本）
- **style_mode**: 风格输出模式
  - `auto`: 自动模式（默认）
  - `chinese`: 纯中文输出
  - `english`: 英文风格锚点 + 中文内容
- **sample_count**: 匹配样本数量（1-8，默认5）

### 输出端口
- **optimized_prompt**: 优化后的提示词（用于生成）
- **matched_styles**: 匹配到的风格锚点（用于参考）

## 💡 使用技巧

1. **中文提示词**: 直接输入中文，节点会自动处理
2. **添加风格词**: 在提示词中加入如 "美国漫画风格"、"油画风格" 等词汇
3. **查看匹配结果**: 可以将 `matched_styles` 连接到显示节点查看匹配了哪些风格
4. **多人脸描述**: 支持详细的人脸特征描述，节点会优化相关表达

## ⚙️ 进阶使用

### 自定义 meta.json 路径
如果需要使用其他 meta.json 文件：
1. 添加 Meta Data Loader 节点
2. 输入自定义路径
3. 查看加载状态

### 同时优化正向和负向提示词
添加两个 Prompt Optimizer 节点，分别处理正向和负向提示词。

## 🎨 支持的风格词（部分）
- 美国漫画风格的三维渲染图
- 三维渲染图
- 纯白色背景 / 白色背景
- 正面全身像
- 角色人物概念图
- 柔和均匀的演播室光照
- 电影感 / 胶片颗粒
- 特写 / 超近景 / 广角远景
- 油画风格 / 水彩风格 / 动漫风格 / 素描风格
- 真人写实风格 / 真实人物 / 写实 / 棚拍
- 以及人脸特征描述词汇
