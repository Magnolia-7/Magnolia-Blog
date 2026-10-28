# Magnolia · 黑白漫画版

Vue 3、FastAPI 与 MySQL 构建的个人博客。界面采用黑白漫画线条、英文漫画体标题和可替换的山治头像、海贼王合照。

## 功能

- 主页、关于、记录、图书馆、友链、留言、搜索七项导航
- 首页匿名访客数（UV）、页面访问量（PV）、已发布文章数及站点运行天数
- 记录贴、技术贴、说说贴，保留旧 life / study 文章分类的数据兼容
- 后台按日填写各项目的投入分钟数；独立“日历”标签与关于页本周、本月、累计表共用数据
- 书籍、电影、动漫、相册和作品集；旧作品入口自动转到图书馆作品集
- 许愿墙与独立留言列表，支持审核、隐藏和站长回复
- 后台站点设置：原始上线日期、头像、漫画背景图
- 文章管理、个人资料、媒体中心及 Cloudflare R2 图片存储

音乐、技术栈、成长树、更新日志和独立作品页面已下线；原数据库内容保留，不做破坏性删除。TreeLife 隐私政策和支持页面继续可访问。

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

默认使用本地存储，生产环境请把 `UPLOAD_DIR` 指向独立的持久化目录，例如：

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

### Cloudflare R2

生产环境可以切换到 Cloudflare R2，新上传的图片和缩略图会直接保存到 R2：

```env
STORAGE_DRIVER=r2
R2_ACCOUNT_ID=your_cloudflare_account_id
R2_ACCESS_KEY_ID=your_r2_access_key_id
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key
R2_BUCKET_NAME=magnolia-blog-images
R2_PUBLIC_BASE_URL=https://img.magnolianook.com
```

R2 密钥只能保存在服务器的 `backend/.env`，不要写进前端或提交到 Git。切换后，数据库中已有的本地图片仍继续使用 `/media/`，只有新上传图片进入 R2，因此不要删除原上传目录或 Nginx 的 `/media/` 配置。

## 上线前检查

1. 备份现有 MySQL 数据库。
2. 运行 Alembic 迁移。
3. 配置持久化上传目录及其写入权限。
4. 让 Nginx 将 `/media/` 映射到上传目录，或交由 FastAPI 提供静态文件。
5. 构建前端并保留 `/api/`、`/media/` 的反向代理规则。
6. 登录后台“站点设置”填写原始上线日期；在“投入时间”中录入每日记录。

本次迁移版本为 `20261029_0003`。升级已有站点时，先备份数据库，再在 `backend` 目录运行 `../.venv/bin/alembic upgrade head`，之后启动新版后端并发布前端构建。迁移会新增三张表，并为旧留言添加默认的“留言”类型，保留旧内容。

站点运行天数按“站点设置”的上线日期计算；迁移默认日期是升级当天，需要修改为真实上线日期。访客与访问量从启用新版本后累计，无法补算旧访问历史。UV 按匿名浏览器标识去重，PV 按公开页面切换或刷新累计；后台、登录、同页重复点击和仅切换图书馆标签不计入。服务端只保存散列后的访客标识，不保存 IP 或网址查询参数。

每日记录以北京时间的日期为准，时长单位为分钟。同一天的项目名不能重复，每日合计不超过 1440 分钟；再次保存会更新当天记录。空记录不计入投入天数。关于页汇总与日历从同一份记录计算。

头像和背景图可在后台替换；留空恢复随站点打包的预览素材。字体和图片来源见 `frontend/public/ASSET_SOURCES.md`。

## 验证

```bash
.venv/bin/python -m unittest discover -s backend/tests -v
cd frontend
npm run build
```

后端测试使用独立内存 SQLite，覆盖每日记录、自动汇总、权限、匿名访客去重、说说贴、许愿审核及旧数据迁移，不连接实际 MySQL。

开发时可用 `API_PROXY_TARGET=http://127.0.0.1:8011 npm run dev` 指定测试后端端口；默认仍代理到 8000。

线上地址：[blog.magnolianook.com](https://blog.magnolianook.com)
