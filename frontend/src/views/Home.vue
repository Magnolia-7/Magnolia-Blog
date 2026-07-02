<template>
  <div class="home-page">
    <!-- 第一屏：欢迎和当前展示内容 -->
    <section ref="heroSectionRef" class="snap-section hero-section">
      <div class="hero-inner">
        <p class="eyebrow">Magnolia Nook · Personal Blog</p>

        <h1>{{ currentText }}</h1>

        <p class="subtitle">
          一个安静的个人空间，用来记录学习、生活、思考，以及那些慢慢长大的瞬间。
        </p>
      </div>

      <div class="hero-side-card">
        <div class="flower-dot">✦</div>
        <p>Today Sharing</p>
        <h3>
          <a href="https://music.163.com/song?id=31108722&uct2=U2FsdGVkX18j7WRBaAt8BjAtP1VeSdjIq/ZJAcAx08Y=" target="_blank" style="text-decoration: none;" >
            兄妹（Live） - 方大同/薛凯琪
          </a>
        </h3>
        <span class="music-note">♪</span>
      </div>

      <div class="scroll-arrow" aria-hidden="true">
        ↓
      </div>
    </section>

    <!-- 第二屏：心里话内容 -->
    <section ref="thoughtSectionRef" class="snap-section thought-section">
      <div class="flower-mark" aria-hidden="true">
        <span>✿</span>
      </div>

      <div class="thought-card">
        <p class="eyebrow">Inner monologue</p>
        <h2>Thought</h2>

        <p>
          我想把这个网站当作一个长期维护的小窝。它不需要一开始就完美，
          但它会随着我的学习、生活和思考一点点生长。
        </p>


        <p>
          我会在这里记录技术上的收获，也记录生活里细小的瞬间。
          有些内容可能很理性，有些内容可能很感性，但它们都会是真实的我。
        </p>

        <p>
          最终成为一本介绍我的书📖。
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";

// 首页标题轮播文案
const texts = [
  "欢迎来到我的个人博客",
  "要天天开心😊",
];

const currentIndex = ref(0);
const currentText = ref(texts[0]);
const heroSectionRef = ref(null);
const thoughtSectionRef = ref(null);

let timer = null;
let autoScrollTimer = null;
let isAutoScrolling = false;

// 读取固定 header 高度，滚动定位时避开顶部导航
function getHeaderOffset() {
  return document.querySelector(".site-header")?.offsetHeight || 48;
}

// 计算目标 section 在整页里的顶部位置
function getSectionTop(section) {
  return window.scrollY + section.getBoundingClientRect().top - getHeaderOffset();
}

// 控制整页滚动到指定 section
function scrollToSection(section) {
  if (!section) return;

  isAutoScrolling = true;

  window.scrollTo({
    top: getSectionTop(section),
    behavior: "smooth",
  });

  window.clearTimeout(autoScrollTimer);
  autoScrollTimer = window.setTimeout(() => {
    isAutoScrolling = false;
  }, 720);
}

// 首页两屏之间的滚轮翻页
function handleHomeWheel(event) {
  if (isAutoScrolling || Math.abs(event.deltaY) < 4) {
    return;
  }

  const heroSection = heroSectionRef.value;
  const thoughtSection = thoughtSectionRef.value;

  if (!heroSection || !thoughtSection) {
    return;
  }

  const headerOffset = getHeaderOffset();
  const currentTop = window.scrollY;
  const heroTop = getSectionTop(heroSection);
  const thoughtTop = getSectionTop(thoughtSection);
  const thoughtBottom = thoughtTop + thoughtSection.offsetHeight;
  const isInsideHome = currentTop >= heroTop - 8 && currentTop < thoughtBottom - headerOffset;

  if (!isInsideHome) {
    return;
  }

  if (event.deltaY > 0 && currentTop < thoughtTop - 12) {
    event.preventDefault();
    scrollToSection(thoughtSection);
  }

  if (event.deltaY < 0 && currentTop > heroTop + 12 && currentTop < thoughtBottom - 12) {
    event.preventDefault();
    scrollToSection(heroSection);
  }
}

// 定时切换首屏标题
onMounted(() => {
  timer = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % texts.length;
    currentText.value = texts[currentIndex.value];
  }, 2800);

  window.addEventListener("wheel", handleHomeWheel, { passive: false });
});

// 离开首页时清理定时器
onUnmounted(() => {
  if (timer) {
    clearInterval(timer);
  }

  window.clearTimeout(autoScrollTimer);
  window.removeEventListener("wheel", handleHomeWheel);
});
</script>

<style scoped>
/* 首页容器跟随整页滚动，不单独产生内部滚动条 */
.home-page {
  min-height: calc(100vh - 48px);
}

/* 每一屏占满 header 下方的可视高度 */
.snap-section {
  min-height: calc(100vh - 48px);
}

/* 首屏介绍区域 */
.hero-section {
  position: relative;
  max-width: 1160px;
  margin: 0 auto;
  padding: 0 32px;
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(300px, 0.65fr);
  align-items: center;
  gap: 72px;
}

.hero-inner {
  position: relative;
  z-index: 1;
  transform: translateY(-12px);
}

/* 小标题样式 */
.eyebrow {
  margin: 0 0 20px;
  color: #b87b8b;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.hero-inner h1 {
  max-width: 780px;
  min-height: 156px;
  margin: 0;
  color: #151515;
  font-size: clamp(48px, 6.5vw, 86px);
  line-height: 1.08;
  font-weight: 800;
  letter-spacing: -3px;
  text-shadow: 0 8px 28px rgba(255, 255, 255, 0.74);
}

.subtitle {
  max-width: 680px;
  margin: 26px 0 0;
  color: #5d5558;
  font-size: 18px;
  line-height: 2;
  text-shadow: 0 4px 20px rgba(255, 255, 255, 0.72);
}

/* 首屏右侧音乐卡片 */
.hero-side-card {
  position: relative;
  z-index: 1;
  min-height: 260px;
  padding: 38px 34px;
  border: 1px solid rgba(90, 50, 64, 0.08);
  border-radius: 30px;
  background:
    radial-gradient(circle at 20% 18%, rgba(255, 237, 242, 0.95), transparent 30%),
    rgba(255, 255, 255, 0.7);
  box-shadow: 0 24px 70px rgba(90, 50, 64, 0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  overflow: hidden;
}

.flower-dot {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  margin-bottom: 34px;
  border-radius: 50%;
  color: #b87b8b;
  background: #fff1f5;
  border: 1px solid #efd1d9;
}

/* 音乐卡片里的装饰音符 */
.hero-side-card p {
  margin: 0 0 10px;
  color: #8b7c82;
  font-size: 13px;
}

.hero-side-card h2 {
  max-width: 260px;
  margin: 0;
  color: #202020;
  font-size: 30px;
  line-height: 1.42;
  letter-spacing: -0.8px;
}

.music-note {
  position: absolute;
  right: 34px;
  bottom: 24px;
  color: rgba(216, 154, 170, 0.34);
  font-size: 82px;
  line-height: 1;
}

/* 下滑提示箭头 */
.scroll-arrow {
  position: absolute;
  left: 50%;
  bottom: 34px;
  z-index: 2;
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(184, 123, 139, 0.28);
  border-radius: 50%;
  color: #b87b8b;
  font-size: 20px;
  background: rgba(255, 255, 255, 0.68);
  box-shadow: 0 14px 32px rgba(184, 123, 139, 0.14);
  transform: translateX(-50%);
  animation: arrowFloat 1.8s ease-in-out infinite;
}

/* 箭头轻微浮动动画 */
@keyframes arrowFloat {
  0% {
    transform: translate(-50%, 0);
    opacity: 0.45;
  }

  50% {
    transform: translate(-50%, 8px);
    opacity: 1;
  }

  100% {
    transform: translate(-50%, 0);
    opacity: 0.45;
  }
}

/* 第二屏心里话区域 */
.thought-section {
  position: relative;
  max-width: 1160px;
  margin: 0 auto;
  padding: 0 32px;
  display: grid;
  grid-template-columns: 180px minmax(0, 760px);
  align-items: center;
  gap: 56px;
}

/* 第二屏左侧花朵标记 */
.flower-mark {
  width: 132px;
  height: 132px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: #b87b8b;
  background:
    radial-gradient(circle, #ffffff 0%, #fff6f8 58%, rgba(248, 219, 226, 0.58) 100%);
  border: 1px solid rgba(216, 154, 170, 0.28);
  box-shadow: 0 18px 48px rgba(216, 154, 170, 0.16);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.flower-mark span {
  font-size: 56px;
}

/* 第二屏正文卡片 */
.thought-card {
  padding: 44px 48px;
  border: 1px solid rgba(90, 50, 64, 0.07);
  border-radius: 32px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 24px 72px rgba(90, 50, 64, 0.055);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.thought-card h2 {
  margin: 0 0 30px;
  color: #151515;
  font-size: 44px;
  line-height: 1.2;
  letter-spacing: -1.2px;
}

.thought-card p {
  margin: 0 0 22px;
  color: #4f464a;
  font-size: 18px;
  line-height: 2.05;
}

.thought-card p:last-child {
  margin-bottom: 0;
}

/* 首页移动端布局 */
@media (max-width: 900px) {
  .snap-section {
    min-height: calc(100vh - 52px);
  }

  .hero-section {
    grid-template-columns: 1fr;
    gap: 34px;
    padding: 78px 24px;
  }

  .hero-inner h1 {
    min-height: auto;
    font-size: clamp(42px, 12vw, 64px);
  }

  .scroll-arrow {
    display: none;
  }

  .thought-section {
    grid-template-columns: 1fr;
    gap: 28px;
    padding: 78px 24px;
  }

  .flower-mark {
    width: 86px;
    height: 86px;
  }

  .flower-mark span {
    font-size: 38px;
  }

  .thought-card {
    padding: 32px 26px;
  }

  .thought-card h2 {
    font-size: 34px;
  }
}
</style>
