# Magnolia Nook 2.0

一个使用 Vue 3、FastAPI 与 MySQL 构建的个人数字花园，用来记录生活、学习、阅读、电影、动漫和网站成长轨迹。

## 2.0 功能

- 双屏叙事主页，欢迎语、当前歌曲和心里话均可在后台维护
- 个人档案、状态、社交账号和技术栈展示
- 生活记录、学习笔记、标签、置顶和 Markdown 正文
- 可点亮时间的学习成长树
- 书籍、电影、动漫与相册
- 访客留言、审核和站长回复
- 网站版本更新日志
- 关键词、分类和日期范围搜索
- 独立内容后台与媒体中心
- 从电脑选择或拖入图片，自动压缩为 WebP 并生成缩略图
- 可切换存储层，为 Cloudflare R2 升级预留接口

## 本地开发

后端配置：

```bash
cp backend/.env.example backend/.env
```

填写 MySQL 连接和安全密钥后安装依赖：

```bash
uv sync
```

首次创建管理员前，还需要在 `backend/.env` 中设置至少 12 位的 `ADMIN_PASSWORD`，然后运行：

```bash
cd backend
../.venv/bin/python -m app.init_admin
```

首次创建全新数据库：

```bash
cd backend
../.venv/bin/python -m app.init_db
../.venv/bin/alembic stamp head
```

从 1.0 数据库升级到 2.0：

```bash
cd backend
../.venv/bin/alembic upgrade head
```

启动后端：

```bash
cd backend
../.venv/bin/uvicorn app.main:app --reload
```

启动前端：

```bash
cd frontend
npm install
npm run dev
```

## 图片存储

2.0 默认使用本地存储，生产环境请把 `UPLOAD_DIR` 指向独立的持久化目录，例如：

```env
STORAGE_DRIVER=local
UPLOAD_DIR=/srv/magnolia/data/uploads
MEDIA_BASE_URL=/media
MAX_UPLOAD_SIZE_MB=10
```

不要把上传目录放在 `frontend/public` 或 `frontend/dist`，前端重新部署时这些目录可能被覆盖。

后台上传图片后会自动：

- 验证真实图片格式和文件大小
- 处理手机照片方向
- 移除 EXIF 信息
- 转换为 WebP
- 限制长边尺寸
- 生成列表缩略图
- 保存可迁移的媒体元数据

Cloudflare R2 计划在 2.0.1 接入。业务层已经通过 `StorageBackend` 隔离存储实现，文章、图书馆和相册无需重写。

## 上线前检查

1. 备份现有 MySQL 数据库。
2. 运行 Alembic 迁移。
3. 配置持久化上传目录及其写入权限。
4. 让 Nginx 将 `/media/` 映射到上传目录，或交由 FastAPI 提供静态文件。
5. 构建前端并保留 `/api/`、`/media/` 的反向代理规则。
6. 登录后台填写主页、成长树、图书馆和 2.0.0 更新日志。

线上地址：[blog.magnolianook.com](https://blog.magnolianook.com)
