<template>
  <div class="page-shell about-page">
    <header class="page-heading">
      <p class="eyebrow">About me</p>
      <h1>关于我</h1>
      <p>一些身份之外的细节：我正在做什么、喜欢什么，以及想去哪里。</p>
    </header>

    <section class="profile-layout">
      <article class="identity-card">
        <div class="portrait-wrap">
          <img v-if="about.avatar" :src="about.avatar" :alt="`${about.nickname || 'Magnolia'} 的头像`" />
          <div v-else class="portrait-placeholder">M</div>
        </div>
        <p class="eyebrow">Profile</p>
        <h2>{{ about.nickname || "Magnolia" }}</h2>
        <p class="signature">{{ about.signature || "在理性里，保留一点温柔。" }}</p>
        <div class="tag-list">
          <span v-for="tag in profileTags" :key="tag">{{ tag }}</span>
        </div>
      </article>

      <article class="story-card surface">
        <span class="chapter-number">01</span>
        <h2>我的说明书</h2>
        <p>{{ about.bio || "这里会慢慢补全关于我的故事。" }}</p>
        <div class="story-grid">
          <div><small>兴趣爱好</small><p>{{ about.interests || "阅读、电影、编程与生活观察" }}</p></div>
          <div><small>正在培养</small><p>{{ about.skills || "持续学习和认真记录的能力" }}</p></div>
          <div><small>联系方式</small><p>{{ about.contacts || "可以通过下方社交账号找到我" }}</p></div>
        </div>
      </article>
    </section>

    <section class="status-section">
      <div class="section-title"><p class="eyebrow">Right now</p><h2>此刻状态</h2></div>
      <div class="status-grid">
        <article><span>心情</span><strong>{{ about.mood || "安静建设中" }}</strong><i>☁</i></article>
        <article><span>短期目标</span><strong>{{ about.short_goal || "完成博客 2.0" }}</strong><i>↗</i></article>
        <article><span>长期目标</span><strong>{{ about.long_goal || "成为更好的自己" }}</strong><i>∞</i></article>
        <article><span>正在听</span><strong>{{ about.current_song || "等待下一首歌" }}</strong><i>♪</i></article>
      </div>
    </section>

    <section class="split-section">
      <div class="social-section">
        <div class="section-title"><p class="eyebrow">Find me</p><h2>社交账号</h2></div>
        <div v-if="socialLinks.length" class="social-list">
          <a v-for="link in socialLinks" :key="link.id || link.url" :href="link.url" target="_blank" rel="noopener noreferrer">
            <span>{{ initial(link.name) }}</span><strong>{{ link.name }}</strong><i>↗</i>
          </a>
        </div>
        <p v-else class="empty-copy">社交账号正在整理。</p>
      </div>

      <div class="tech-section">
        <div class="section-title"><p class="eyebrow">Toolbox</p><h2>技术栈</h2></div>
        <div v-if="techStacks.length" class="tech-list">
          <a v-for="tech in techStacks" :key="tech.id || tech.name" :href="tech.url || undefined" :target="tech.url ? '_blank' : undefined" rel="noopener noreferrer">
            <strong>{{ tech.name }}</strong><span>{{ "●".repeat(tech.level || 3) }}{{ "○".repeat(5 - (tech.level || 3)) }}</span>
          </a>
        </div>
        <p v-else class="empty-copy">技术栈正在整理。</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { getAbout } from "../api/about";
import { getSocialLinks, getTechStacks } from "../api/content";

const about = ref({});
const socialLinks = ref([]);
const techStacks = ref([]);

const profileTags = computed(() => {
  const value = about.value.profile_tags;
  if (!value) return ["开发者", "记录者", "终身学习"];
  try { const parsed = JSON.parse(value); return Array.isArray(parsed) ? parsed : []; }
  catch { return value.split(/[,，]/).map((item) => item.trim()).filter(Boolean); }
});

function initial(name = "M") { return name.trim().slice(0, 1).toUpperCase(); }
function legacyLinks(value) {
  if (!value) return [];
  try {
    const parsed = typeof value === "string" ? JSON.parse(value) : value;
    if (Array.isArray(parsed)) return parsed;
    return Object.entries(parsed).map(([name, url]) => ({ name, url }));
  } catch { return []; }
}

onMounted(async () => {
  const results = await Promise.allSettled([getAbout(), getSocialLinks(), getTechStacks()]);
  about.value = results[0].status === "fulfilled" ? results[0].value.data || {} : {};
  socialLinks.value = results[1].status === "fulfilled" && results[1].value.data.length
    ? results[1].value.data : legacyLinks(about.value.social_links);
  techStacks.value = results[2].status === "fulfilled" && results[2].value.data.length
    ? results[2].value.data : legacyLinks(about.value.tech_stack).map((item) => ({ ...item, level: 3 }));
});
</script>

<style scoped>
.profile-layout { display: grid; grid-template-columns: minmax(280px, .72fr) minmax(0, 1.28fr); gap: 24px; }
.identity-card { position: relative; padding: 30px; border-radius: 180px 180px 24px 24px; text-align: center; color: #fff; background: linear-gradient(155deg, #9e6875, #714954); box-shadow: var(--shadow-lg); overflow: hidden; }
.identity-card::after { content: "✦"; position: absolute; right: 24px; bottom: 16px; color: rgba(255,255,255,.17); font-size: 72px; }
.portrait-wrap { width: min(240px, 80%); aspect-ratio: 1; margin: 0 auto 28px; padding: 8px; border: 1px solid rgba(255,255,255,.32); border-radius: 50%; }
.portrait-wrap img, .portrait-placeholder { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }
.portrait-placeholder { display: grid; place-items: center; font: 80px Georgia, serif; background: rgba(255,255,255,.14); }
.identity-card .eyebrow { color: rgba(255,255,255,.68); }
.identity-card h2 { margin: 0; font: 500 40px Georgia, "Songti SC", serif; }
.signature { margin: 13px 0 24px; color: rgba(255,255,255,.8); line-height: 1.8; }
.tag-list { position: relative; z-index: 1; display: flex; justify-content: center; flex-wrap: wrap; gap: 7px; }
.tag-list span { padding: 6px 11px; border: 1px solid rgba(255,255,255,.25); border-radius: 999px; font-size: 12px; }
.story-card { position: relative; padding: clamp(34px, 5vw, 68px); overflow: hidden; }
.chapter-number { position: absolute; right: 28px; top: 12px; color: var(--rose-100); font: 110px Georgia, serif; }
.story-card h2, .section-title h2 { position: relative; margin: 0; font: 500 clamp(29px, 4vw, 42px) Georgia, "Songti SC", serif; }
.story-card > p { position: relative; max-width: 680px; margin: 24px 0 38px; color: var(--muted-strong); font: 17px/2 "Songti SC", serif; white-space: pre-line; }
.story-grid { position: relative; display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; padding-top: 28px; border-top: 1px solid var(--line); }
.story-grid small, .status-grid span { color: var(--rose-600); font-size: 11px; font-weight: 750; letter-spacing: .12em; }
.story-grid p { margin: 9px 0 0; color: var(--muted-strong); line-height: 1.75; white-space: pre-line; }
.status-section, .split-section { margin-top: 88px; }
.section-title { margin-bottom: 28px; }
.status-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.status-grid article { position: relative; min-height: 170px; padding: 24px; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid var(--line); border-radius: 20px; background: rgba(255,253,249,.78); overflow: hidden; }
.status-grid strong { max-width: 85%; font: 500 19px/1.55 Georgia, "Songti SC", serif; }
.status-grid i { position: absolute; right: 17px; bottom: 10px; color: var(--rose-200); font: 42px Georgia, serif; }
.split-section { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; }
.social-list, .tech-list { display: grid; gap: 10px; }
.social-list a, .tech-list a { min-height: 70px; padding: 14px 18px; display: flex; align-items: center; gap: 14px; border-bottom: 1px solid var(--line); text-decoration: none; }
.social-list a > span { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 50%; color: var(--rose-700); background: var(--rose-50); font-family: Georgia, serif; }
.social-list strong { flex: 1; }.social-list i { color: var(--rose-500); }
.tech-list a { justify-content: space-between; }.tech-list span { color: var(--rose-500); font-size: 11px; letter-spacing: .12em; }
.empty-copy { color: var(--muted); }
@media (max-width: 840px) {
  .profile-layout, .split-section { grid-template-columns: 1fr; }
  .identity-card { max-width: 500px; width: 100%; margin: 0 auto; }
  .status-grid { grid-template-columns: repeat(2, 1fr); }
  .story-grid { grid-template-columns: 1fr; }
}
@media (max-width: 520px) { .status-grid { grid-template-columns: 1fr; } }
</style>
