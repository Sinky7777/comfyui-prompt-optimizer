# GitHub 上传指南

本项目已经准备好上传到 GitHub！以下是步骤说明：

## 步骤 1: 在 GitHub 上创建新仓库

1. 访问 https://github.com/new
2. 填写仓库名称（例如：`comfyui-prompt-optimizer`）
3. 选择 Public 或 Private
4. **不要**初始化 README、.gitignore 或 LICENSE（我们已经有了）
5. 点击 "Create repository"

## 步骤 2: 连接本地仓库到 GitHub

在终端中运行以下命令（替换为您的实际用户名和仓库名）：

```bash
cd /Users/bytedance/Desktop/风格技法标签节点
git remote add origin https://github.com/您的用户名/您的仓库名.git
git branch -M main
git push -u origin main
```

## 步骤 3: 如果使用 SSH

如果您使用 SSH 而不是 HTTPS：

```bash
git remote add origin git@github.com:您的用户名/您的仓库名.git
git branch -M main
git push -u origin main
```

## 包含的文件

- `__init__.py` - 节点注册文件
- `prompt_optimizer.py` - 核心实现
- `meta.json` - 训练数据样本
- `README.md` - 使用说明
- `test_node.py` - 测试脚本
- `.gitignore` - Git 忽略文件
- `GITHUB_UPLOAD_GUIDE.md` - 本指南

## 推送到 GitHub 后

成功推送后，您可以：
- 分享仓库链接给其他人
- 创建 Release 版本
- 添加 Issues 和 Pull Requests
- 持续更新和改进项目

## 常见问题

**问：提示需要输入用户名和密码？**
答：建议使用 GitHub Personal Access Token 或配置 SSH 密钥。

**问：meta.json 文件太大？**
答：如果需要，可以将 meta.json 添加到 .gitignore 并使用 Git LFS 管理大文件。
