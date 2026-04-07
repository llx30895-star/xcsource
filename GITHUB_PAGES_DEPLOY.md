# GitHub Pages 部署指南

## 📋 部署步骤

### 1. 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名称输入：`xcsource`（小写，与你的示例一致）
3. 选择 **Public**（公开仓库才能使用免费 GitHub Pages）
4. **不要**勾选 "Add a README file"
5. 点击 "Create repository"

### 2. 推送代码到 GitHub

在 PowerShell 中执行（已在 XCSOURCE 目录）：

```powershell
# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/xcsource.git

# 推送代码
git branch -M main
git push -u origin main
```

**示例**（如果你的用户名是 llx30895-star）：
```powershell
git remote add origin https://github.com/llx30895-star/xcsource.git
git branch -M main
git push -u origin main
```

### 3. 启用 GitHub Pages

1. 进入你的仓库页面：`https://github.com/YOUR_USERNAME/xcsource`
2. 点击 **Settings**（设置）
3. 左侧菜单找到 **Pages**
4. 在 "Source" 下拉菜单选择：
   - Branch: `main`
   - Folder: `/ (root)`
5. 点击 **Save**

### 4. 等待部署完成

- 通常需要 1-3 分钟
- 部署完成后会显示：
  ```
  Your site is live at https://YOUR_USERNAME.github.io/xcsource/
  ```

## 🌐 访问地址

部署成功后，你的网站将在以下地址访问：

```
https://YOUR_USERNAME.github.io/xcsource/
```

例如：
```
https://llx30895-star.github.io/xcsource/
```

## 🔧 后续更新

每次修改代码后，执行：

```powershell
cd C:\Users\Win11\Desktop\XCSOURCE
git add .
git commit -m "更新说明"
git push
```

GitHub Pages 会自动重新部署（1-3分钟）。

## ⚠️ 注意事项

### 1. 路径问题
由于网站在子目录 `/xcsource/` 下，需要确保所有资源路径正确：

- ✅ 相对路径：`images/xxx.png`（推荐）
- ✅ 绝对路径：`/xcsource/images/xxx.png`
- ❌ 错误：`/images/xxx.png`

**当前代码已使用相对路径，无需修改。**

### 2. Flask 后端
GitHub Pages 只支持静态网站（HTML/CSS/JS），不支持 Python Flask。

**解决方案**：
- 联系表单需要使用第三方服务：
  - **Formspree**（推荐）：https://formspree.io/
  - **Netlify Forms**
  - **Google Forms**

### 3. 修改表单提交

如果使用 Formspree，修改 `index.html` 中的表单：

```html
<!-- 原来的 -->
<form id="coopForm" novalidate>

<!-- 改为 -->
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

## 📱 测试清单

部署后检查：
- [ ] 首页正常显示
- [ ] 所有图片加载成功
- [ ] 导航链接工作正常
- [ ] 响应式布局正常（手机/平板/桌面）
- [ ] 表单提交（如果配置了第三方服务）

## 🆘 常见问题

### Q: 图片不显示？
A: 检查 `images/` 文件夹是否已推送到 GitHub，路径是否正确。

### Q: 404 错误？
A: 确保 GitHub Pages 设置中选择了正确的分支（main）和根目录。

### Q: 样式错乱？
A: 清除浏览器缓存，或使用无痕模式访问。

### Q: 表单无法提交？
A: GitHub Pages 不支持后端，需要配置第三方表单服务。

## 📞 需要帮助？

如有问题，请提供：
1. GitHub 仓库地址
2. 错误截图
3. 浏览器控制台错误信息（F12 → Console）
