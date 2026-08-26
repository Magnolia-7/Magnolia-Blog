<template>
  <div class="home-page">
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Magnolia Nook · Since 2026</p>
        <div class="hero-kicker">欢迎来到</div>
        <h1>{{ currentText }}</h1>
        <p class="hero-subtitle">
          {{ about.hero_subtitle || "一个安静的个人空间，用来记录学习、生活、思考，以及那些慢慢长大的瞬间。" }}
        </p>
        <div class="hero-actions">
          <RouterLink class="primary-link" to="/records">翻阅记录</RouterLink>
          <RouterLink class="text-link" to="/about">认识我 <span>↗</span></RouterLink>
        </div>
      </div>

      <aside class="now-card">
        <div class="now-top"><span>NOW PLAYING</span><i></i></div>
        <div class="album-mark">♪</div>
        <div>
          <small>此刻在听</small>
          <h2>
            <a v-if="about.current_song_url" :href="about.current_song_url" target="_blank" rel="noopener noreferrer">
              {{ about.current_song || "还没有分享歌曲" }}
            </a>
            <span v-else>{{ about.current_song || "还没有分享歌曲" }}</span>
          </h2>
        </div>
        <div class="sound-bars" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      </aside>

      <a class="scroll-cue" href="#thought"><span>SCROLL</span><i>↓</i></a>
    </section>

    <section id="thought" class="thought-section">
      <div class="thought-index">02</div>
      <div class="thought-copy">
        <p class="eyebrow">A note from me</p>
        <h2>写给此刻，也写给以后。</h2>
        <div class="thought-text">
          <p v-for="paragraph in thoughtParagraphs" :key="paragraph">{{ paragraph }}</p>
        </div>
        <p class="thought-sign">— Magnolia</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";
import { getAbout } from "../api/about";

const texts = ["我的个人博客", "这一本生长中的书"];
const currentText = ref(texts[0]);
const currentIndex = ref(0);
const about = ref({});
let timer;

const fallbackThought = "我想把这个网站当作一个长期维护的小窝。它不需要一开始就完美，但它会随着我的学习、生活和思考一点点生长。\n\n我会在这里记录技术上的收获，也记录生活里细小的瞬间。有些内容可能很理性，有些内容可能很感性，但它们都会是真实的我。\n\n最终成为一本介绍我的书。";
const thoughtParagraphs = computed(() => (about.value.home_thought || fallbackThought).split(/\n\s*\n/).filter(Boolean));

onMounted(async () => {
  try { about.value = (await getAbout()).data || {}; } catch (error) { console.error(error); }
  timer = window.setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % texts.length;
    currentText.value = texts[currentIndex.value];
  }, 3200);
});
onUnmounted(() => window.clearInterval(timer));
</script>

<style scoped>
.home-page { overflow: hidden; }
.hero { position: relative; width: min(1240px, calc(100% - 48px)); min-height: calc(100svh - 68px); margin: 0 auto; display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(300px, .65fr); align-items: center; gap: clamp(48px, 8vw, 110px); padding: 80px 0 100px; }
.hero::before { content: "M"; position: absolute; left: -7vw; top: 42%; z-index: -1; color: rgba(185,111,128,.055); font-family: Georgia, serif; font-size: min(52vw, 650px); line-height: .5; }
.hero-kicker { margin-bottom: 10px; color: var(--muted); font-family: "Songti SC", serif; font-size: 18px; }
.hero h1 { max-width: 780px; min-height: 1.1em; margin: 0; font-family: Georgia, "Songti SC", serif; font-size: clamp(56px, 7.2vw, 104px); font-weight: 500; line-height: 1.03; letter-spacing: -.06em; }
.hero-subtitle { max-width: 620px; margin: 30px 0 0; color: var(--muted-strong); font-size: clamp(16px, 1.5vw, 19px); line-height: 2; }
.hero-actions { display: flex; align-items: center; gap: 24px; margin-top: 36px; }
.primary-link { padding: 13px 24px; border-radius: 999px; color: #fff; background: var(--rose-600); text-decoration: none; box-shadow: 0 12px 30px rgba(158,88,106,.22); }
.text-link { color: var(--muted-strong); text-decoration: none; }
.text-link span { margin-left: 5px; color: var(--rose-600); }
.now-card { position: relative; min-height: 390px; padding: 28px; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid rgba(255,255,255,.84); border-radius: 180px 180px 28px 28px; background: linear-gradient(165deg, rgba(247,225,229,.9), rgba(255,253,249,.88) 55%, rgba(228,233,224,.7)); box-shadow: var(--shadow-lg); overflow: hidden; }
.now-card::after { content: ""; position: absolute; inset: 45% -30% -35%; border: 1px solid rgba(185,111,128,.16); border-radius: 50%; }
.now-top { display: flex; align-items: center; justify-content: center; gap: 8px; color: var(--rose-700); font-size: 10px; letter-spacing: .18em; }
.now-top i { width: 5px; height: 5px; border-radius: 50%; background: var(--rose-500); box-shadow: 0 0 0 5px rgba(185,111,128,.1); }
.album-mark { width: 116px; height: 116px; display: grid; place-items: center; align-self: center; border-radius: 50%; color: var(--rose-700); font-size: 38px; background: rgba(255,255,255,.65); box-shadow: inset 0 0 0 1px rgba(120,64,78,.12), 0 18px 50px rgba(120,64,78,.12); }
.now-card small { position: relative; color: var(--muted); }
.now-card h2 { position: relative; margin: 8px 0 0; font-family: Georgia, "Songti SC", serif; font-size: 23px; line-height: 1.45; }
.now-card h2 a { text-decoration: none; }
.sound-bars { position: absolute; right: 28px; bottom: 28px; display: flex; align-items: end; gap: 3px; height: 20px; }
.sound-bars i { width: 2px; background: var(--rose-500); animation: sound 1s ease-in-out infinite alternate; }
.sound-bars i:nth-child(1) { height: 8px; }.sound-bars i:nth-child(2) { height: 16px; animation-delay: -.3s; }.sound-bars i:nth-child(3) { height: 12px; animation-delay: -.6s; }.sound-bars i:nth-child(4) { height: 19px; animation-delay: -.15s; }
@keyframes sound { to { height: 5px; opacity: .45; } }
.scroll-cue { position: absolute; left: 0; bottom: 34px; display: flex; align-items: center; gap: 12px; color: var(--muted); font-size: 10px; letter-spacing: .18em; text-decoration: none; }
.scroll-cue i { width: 34px; height: 34px; display: grid; place-items: center; border: 1px solid var(--line); border-radius: 50%; font-style: normal; }
.thought-section { min-height: 80vh; padding: 120px max(24px, calc((100vw - 1060px) / 2)); display: grid; grid-template-columns: 120px minmax(0, 760px); align-items: start; gap: 70px; background: rgba(248,242,237,.8); border-block: 1px solid var(--line); }
.thought-index { color: var(--rose-300); font-family: Georgia, serif; font-size: 88px; line-height: 1; }
.thought-copy h2 { max-width: 700px; margin: 0 0 40px; font-family: Georgia, "Songti SC", serif; font-size: clamp(38px, 5vw, 64px); font-weight: 500; line-height: 1.25; letter-spacing: -.04em; }
.thought-text { padding-left: 26px; border-left: 1px solid var(--rose-300); }
.thought-text p { margin: 0 0 22px; color: var(--muted-strong); font-family: "Songti SC", serif; font-size: 18px; line-height: 2.15; }
.thought-sign { margin-top: 28px; color: var(--rose-600); font-family: Georgia, serif; font-style: italic; }
@media (max-width: 820px) {
  .hero { width: calc(100% - 32px); grid-template-columns: 1fr; padding: 72px 0; }
  .hero h1 { min-height: 2.1em; font-size: clamp(50px, 15vw, 76px); }
  .now-card { min-height: 330px; max-width: 360px; width: 100%; justify-self: center; }
  .scroll-cue { display: none; }
  .thought-section { grid-template-columns: 1fr; gap: 28px; padding: 84px 24px; }
  .thought-index { font-size: 54px; }
}
</style>
