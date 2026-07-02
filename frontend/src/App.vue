<template>
  <div class="app">
    <!-- 全站背景层 -->
    <div class="site-bg" aria-hidden="true"></div>

    <!-- 顶部导航 -->
    <header class="site-header">
      <div class="header-inner">
        <RouterLink to="/" class="brand">
          <span class="brand-mark">✦</span>
          <span>Magnolia Nook</span>
        </RouterLink>

        <nav class="nav-links">
          <RouterLink to="/">主页</RouterLink>
          <RouterLink to="/about">关于</RouterLink>
          <RouterLink to="/records">记录</RouterLink>
          <RouterLink to="/search">搜索</RouterLink>
        </nav>
      </div>
    </header>

    <!-- 路由页面出口 -->
    <main class="main">
      <RouterView />
    </main>

    <!-- 全站页脚 -->
    <footer class="footer">
      <div class="footer-line"></div>
      <p>愿这里像一场安静的樱花雨，也像一朵慢慢盛开的白玉兰。</p>
      <a
        href="https://beian.miit.gov.cn/"
        target="_blank"
        rel="noopener noreferrer"
      >
        闽ICP备2026014322号-1
      </a>
      <br>
      <img 
      src="/beian.png" 
      alt="" 
      style="width: 16px; height: 16px; 
      vertical-align: middle; 
      margin-right: 4px;" 
      />  
      <a 
      href="https://beian.mps.gov.cn/#/query/webSearch?code=35082302000285" 
      rel="noreferrer" 
      target="_blank"
      >
      闽公网安备35082302000285号
      </a>
    </footer>
  </div>
</template>

<style scoped>
.app {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

/* 全站固定背景图层 */
.site-bg {
  position: fixed;
  inset: 0;
  z-index: -2;
  background-image:
    linear-gradient(
      90deg,
      rgba(255, 255, 255, 0.9) 0%,
      rgba(255, 255, 255, 0.76) 42%,
      rgba(255, 255, 255, 0.5) 72%,
      rgba(255, 255, 255, 0.38) 100%
    ),
    url("/images/sakura-bg.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* 背景上的柔光遮罩 */
.site-bg::after {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 12% 10%, rgba(255, 228, 236, 0.42), transparent 28%),
    radial-gradient(circle at 88% 20%, rgba(255, 255, 255, 0.36), transparent 26%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.1), rgba(255, 247, 250, 0.3));
}

/* 外层 header 只负责固定和背景 */
.site-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
  border-bottom: 1px solid rgba(90, 50, 64, 0.08);
  background-image:
    linear-gradient(
      90deg,
      rgba(255, 255, 255, 0.58) 0%,
      rgba(255, 255, 255, 0.38) 48%,
      rgba(255, 246, 249, 0.28) 100%
    ),
    url("/images/sakura-bg.jpg");
  background-size: cover;
  background-position: center 16%;
  background-repeat: no-repeat;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

/* 内层负责真正的左右布局 */
.header-inner {
  width: 100%;
  min-height: 48px;
  padding: 8px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

/* 左侧站点名称 */
.brand {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #1f1f1f;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.3px;
  text-decoration: none;
  white-space: nowrap;
}

.brand-mark {
  color: #b87b8b;
  font-size: 14px;
}

/* 右侧主导航 */
.nav-links {
  flex-shrink: 0;
  margin-left: auto;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 18px;
  white-space: nowrap;
}

.nav-links a {
  position: relative;
  color: #2f2f2f;
  font-size: 14px;
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.2s ease;
}

/* 导航 hover / 当前页下划线 */
.nav-links a::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -5px;
  width: 0;
  height: 1px;
  background: #b87b8b;
  transform: translateX(-50%);
  transition: width 0.2s ease;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #111;
}

.nav-links a:hover::after,
.nav-links a.router-link-active::after {
  width: 100%;
}

/* 主内容区域避开固定 header */
.main {
  flex: 1;
  padding-top: 48px;
}

/* 页脚备案和收尾文案 */
.footer {
  position: relative;
  padding: 38px 24px 28px;
  text-align: center;
  color: #7b6f73;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.46);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.footer-line {
  width: 56px;
  height: 1px;
  margin: 0 auto 18px;
  background: linear-gradient(90deg, transparent, #b87b8b, transparent);
}

.footer p {
  margin: 0 0 10px;
  color: #8b7c82;
}

.footer a {
  color: #7b6f73;
  text-decoration: none;
}

.footer a:hover {
  color: #b87b8b;
  text-decoration: underline;
}

/* 小屏导航间距 */
@media (max-width: 720px) {
  .header-inner {
    min-height: 52px;
    padding: 8px 14px;
    gap: 12px;
  }

  .brand {
    font-size: 13px;
  }

  .brand-mark {
    font-size: 13px;
  }

  .nav-links {
    gap: 10px;
  }

  .nav-links a {
    font-size: 13px;
  }

  .main {
    padding-top: 52px;
  }
}
</style>
