# 海森智源官网 GitHub Pages 部署指令

## 任务目标
将本地静态网站部署到 GitHub Pages，使其可通过 `https://<username>.github.io/hysenai-website/` 访问。

## 本地文件位置
- 网站根目录：`C:\Users\<用户名>\Desktop\网站\`
- 入口文件：`index.html`（已从 hysenai_official.html 复制改名）
- 资源文件：logo.png, logo_cutout.png, logo_nav.png, logo_footer.png, logo_partner.png, logo_watermark.png, auth_cert.jpg, volcano_auth.png, xiaoice_auth.jpg, wechat_qr.jpg

## 需要排除的文件（不要上传）
- hysenai_official.html（index.html 的重复副本）
- GEO服务客户成果统计表.xlsx（客户数据，网站不引用）
- original/ 文件夹（早期备份）

## 执行步骤

### Step 1: 检查并安装 Git
```powershell
git --version
# 如果未安装，提示用户从 https://git-scm.com/download/win 下载安装
```

### Step 2: 配置 Git 用户信息
```powershell
git config --global user.name "<GitHub用户名>"
git config --global user.email "<GitHub注册邮箱>"
```

### Step 3: 在 GitHub 创建仓库
- 仓库名：hysenai-website
- 可见性：Public
- 不要勾选 README / .gitignore / license
- 创建空仓库

### Step 4: 初始化本地仓库并推送
```powershell
cd "$env:USERPROFILE\Desktop\网站"

# 初始化
git init
git remote add origin https://github.com/<用户名>/hysenai-website.git

# 只添加需要部署的文件
git add index.html
git add logo.png logo_cutout.png logo_nav.png logo_footer.png logo_partner.png logo_watermark.png
git add auth_cert.jpg volcano_auth.png xiaoice_auth.jpg
git add wechat_qr.jpg

# 提交并推送
git commit -m "海森智源官网部署"
git branch -M main
git push -u origin main
```

### Step 5: 创建 .gitignore（防止后续误传）
在网站根目录创建 `.gitignore` 文件，内容：
```
hysenai_official.html
GEO服务客户成果统计表.xlsx
original/
*.xlsx
```

### Step 6: 开启 GitHub Pages
1. 进入仓库 Settings → Pages
2. Source: Deploy from a branch
3. Branch: main / root
4. Save
5. 等待 1-2 分钟构建完成

### Step 7: 验证部署
- 访问 `https://<用户名>.github.io/hysenai-website/`
- 检查页面正常加载
- 检查所有图片资源正常显示（logo、证书、二维码）
- 检查页面无 404 资源

## 注意事项
- 推送时若弹出认证窗口，登录 GitHub 账号授权即可
- 若推送报错 403，检查仓库是否创建成功、用户名是否正确
- 若 Pages 构建失败，确认 index.html 在仓库根目录（不在子文件夹内）
- 网站为纯静态页面，无需构建工具，无需 Node.js
