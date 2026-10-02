<template>
  <div class="showcase-page">
    <section class="showcase-hero">
      <div class="hero-copy">
        <p class="eyebrow">Things I build · People I follow</p>
        <h1>作品与友邻</h1>
        <p class="hero-lead">把做过的东西认真收好，也把互联网上值得常去的小站放在这里。</p>
        <div class="hero-actions">
          <a href="#projects">浏览项目 <span>↓</span></a>
          <a href="#friends">拜访友邻 <span>↘</span></a>
        </div>
      </div>
      <div class="hero-orbit" aria-hidden="true">
        <span class="orbit orbit-one"></span>
        <span class="orbit orbit-two"></span>
        <span class="orbit-dot dot-one">⌘</span>
        <span class="orbit-dot dot-two">↗</span>
        <strong>{{ String(projects.length).padStart(2, "0") }}</strong>
        <small>PROJECTS</small>
      </div>
    </section>

    <section id="projects" class="projects-section content-section">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Selected work</p>
          <h2>项目档案</h2>
        </div>
        <p>爬虫、独立项目、自建 Skill，以及所有从一个念头慢慢长成的东西。</p>
      </div>

      <div v-if="categories.length > 1" class="category-filter" aria-label="项目分类">
        <button :class="{ active: activeCategory === '全部' }" @click="activeCategory = '全部'">全部</button>
        <button v-for="category in categories" :key="category" :class="{ active: activeCategory === category }" @click="activeCategory = category">
          {{ category }}
        </button>
      </div>

      <div v-if="projectsLoading" class="showcase-state">正在整理项目档案…</div>
      <div v-else-if="projectsError" class="showcase-state error">{{ projectsError }}</div>
      <div v-else-if="!projects.length" class="showcase-state">
        <span>✦</span>
        <strong>作品集正在装订</strong>
        <p>项目会在整理好之后陆续出现在这里。</p>
      </div>
      <div v-else class="project-grid">
        <article v-for="(project, index) in filteredProjects" :key="project.id" :class="['project-card', { featured: project.featured }]">
          <div class="project-topline">
            <span class="project-number">{{ String(index + 1).padStart(2, "0") }}</span>
            <span class="project-category">{{ project.category }}</span>
            <span class="project-status"><i></i>{{ statusLabel(project.status) }}</span>
          </div>
          <div class="project-symbol" aria-hidden="true">{{ projectSymbol(project.category) }}</div>
          <div class="project-copy">
            <h3>{{ project.title }}</h3>
            <p>{{ project.description }}</p>
          </div>
          <div v-if="projectTags(project.tags).length" class="project-tags">
            <span v-for="tag in projectTags(project.tags)" :key="tag">{{ tag }}</span>
          </div>
          <div v-if="project.github_url || project.demo_url" class="project-links">
            <a v-if="project.github_url" :href="project.github_url" target="_blank" rel="noopener noreferrer">GitHub <span>↗</span></a>
            <a v-if="project.demo_url" :href="project.demo_url" target="_blank" rel="noopener noreferrer">查看项目 <span>↗</span></a>
          </div>
          <span v-if="project.featured" class="featured-label">FEATURED</span>
        </article>
      </div>
    </section>

    <section id="friends" class="friends-section">
      <div class="friends-inner">
        <div class="section-heading friends-heading">
          <div>
            <p class="eyebrow">A quiet neighborhood</p>
            <h2>友链花园</h2>
          </div>
          <p>沿着链接散步，去看看朋友们正在记录怎样的世界。</p>
        </div>

        <div v-if="friendsLoading" class="showcase-state">正在寻找友邻…</div>
        <div v-else-if="friendsError" class="showcase-state error">{{ friendsError }}</div>
        <div v-else-if="!friendLinks.length" class="showcase-state friends-empty">
          <span>❀</span>
          <strong>花园里还留着空位</strong>
          <p>新的朋友到来时，会在这里拥有一张小小的名片。</p>
        </div>
        <div v-else class="friend-grid">
          <a v-for="(friend, index) in friendLinks" :key="friend.id" :href="friend.url" target="_blank" rel="noopener noreferrer" class="friend-card">
            <span class="friend-index">{{ String(index + 1).padStart(2, "0") }}</span>
            <div class="friend-avatar">
              <img v-if="friend.avatar_url" :src="friend.avatar_url" :alt="`${friend.name} 的头像`" />
              <span v-else>{{ initial(friend.name) }}</span>
            </div>
            <div class="friend-copy">
              <h3>{{ friend.name }}</h3>
              <p>{{ friend.description || "去看看这个安静生长的小站。" }}</p>
              <small>{{ hostname(friend.url) }}</small>
            </div>
            <span class="friend-arrow">↗</span>
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { getFriendLinks, getProjects } from "../api/content";

const projects = ref([]);
const friendLinks = ref([]);
const activeCategory = ref("全部");
const projectsLoading = ref(true);
const friendsLoading = ref(true);
const projectsError = ref("");
const friendsError = ref("");

const categories = computed(() => [...new Set(projects.value.map((item) => item.category).filter(Boolean))]);
const filteredProjects = computed(() => activeCategory.value === "全部"
  ? projects.value
  : projects.value.filter((item) => item.category === activeCategory.value));

function projectTags(value) {
  if (!value) return [];
  try {
    const parsed = JSON.parse(value);
    if (Array.isArray(parsed)) return parsed.map(String).filter(Boolean);
  } catch {}
  return value.split(/[,，]/).map((item) => item.trim()).filter(Boolean);
}

function statusLabel(status) {
  return ({ building: "构建中", active: "持续维护", completed: "已完成", archived: "已归档" })[status] || "持续维护";
}

function projectSymbol(category = "") {
  const value = category.toLowerCase();
  if (/爬虫|crawler|spider/.test(value)) return "⌁";
  if (/skill|工具|tool/.test(value)) return "✦";
  if (/web|网站|前端/.test(value)) return "◇";
  if (/app|应用|treeios/.test(value)) return "◉";
  return "↗";
}

function initial(name = "M") { return name.trim().slice(0, 1).toUpperCase(); }
function hostname(url) {
  try { return new URL(url).hostname.replace(/^www\./, ""); }
  catch { return url; }
}

onMounted(async () => {
  const [projectResult, friendResult] = await Promise.allSettled([getProjects(), getFriendLinks()]);
  if (projectResult.status === "fulfilled") projects.value = projectResult.value.data || [];
  else projectsError.value = "项目档案暂时无法读取，请稍后再来看看。";
  if (friendResult.status === "fulfilled") friendLinks.value = friendResult.value.data || [];
  else friendsError.value = "友链花园暂时无法读取，请稍后再来看看。";
  projectsLoading.value = false;
  friendsLoading.value = false;
});
</script>

<style scoped>
.showcase-page { overflow: hidden; }
.showcase-hero { position: relative; width: min(1180px, calc(100% - 40px)); min-height: 570px; margin: 0 auto; padding: 104px 0 90px; display: grid; grid-template-columns: minmax(0, 1fr) 390px; align-items: center; gap: 80px; }
.showcase-hero::before { content: ""; position: absolute; width: 430px; height: 430px; left: -270px; top: -120px; border: 1px solid var(--rose-100); border-radius: 50%; box-shadow: 0 0 0 78px rgba(247,225,229,.25), 0 0 0 156px rgba(247,225,229,.12); }
.hero-copy { position: relative; z-index: 1; }
.hero-copy h1 { margin: 0; font: 500 clamp(56px, 8vw, 104px)/1.02 Georgia, "Songti SC", serif; letter-spacing: -.065em; }
.hero-lead { max-width: 600px; margin: 28px 0 0; color: var(--muted-strong); font: 18px/2 "Songti SC", serif; }
.hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 36px; }
.hero-actions a { padding: 12px 18px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted-strong); text-decoration: none; background: rgba(255,255,255,.62); transition: .2s ease; }
.hero-actions a:first-child { color: #fff; border-color: var(--rose-600); background: var(--rose-600); }
.hero-actions a:hover { transform: translateY(-2px); box-shadow: var(--shadow-sm); }
.hero-actions span { margin-left: 12px; }
.hero-orbit { position: relative; width: 360px; aspect-ratio: 1; display: grid; place-items: center; justify-self: end; border-radius: 50%; background: radial-gradient(circle, rgba(255,253,249,.92) 0 34%, transparent 35%), linear-gradient(145deg, rgba(247,225,229,.82), rgba(229,235,225,.62)); box-shadow: inset 0 0 0 1px rgba(255,255,255,.86), var(--shadow-lg); }
.hero-orbit::before, .hero-orbit::after { content: ""; position: absolute; border: 1px solid rgba(120,64,78,.16); border-radius: 50%; }
.hero-orbit::before { inset: 46px; }.hero-orbit::after { inset: 90px; border-style: dashed; }
.hero-orbit strong { z-index: 1; margin-top: -18px; color: var(--rose-700); font: 500 70px/1 Georgia, serif; }
.hero-orbit small { position: absolute; z-index: 1; top: 56%; color: var(--muted); font-size: 9px; letter-spacing: .24em; }
.orbit { position: absolute; left: 50%; top: 50%; border-radius: 50%; border: 1px solid rgba(158,88,106,.25); transform-origin: left center; }
.orbit-one { width: 145px; transform: rotate(28deg); }.orbit-two { width: 164px; transform: rotate(152deg); }
.orbit-dot { position: absolute; width: 42px; height: 42px; display: grid; place-items: center; border-radius: 50%; color: var(--rose-700); background: var(--paper); box-shadow: var(--shadow-sm); }
.dot-one { top: 52px; right: 54px; }.dot-two { left: 28px; bottom: 88px; }
.content-section { width: min(1180px, calc(100% - 40px)); margin: 0 auto; padding: 105px 0 120px; }
.section-heading { display: grid; grid-template-columns: 1fr minmax(280px, 430px); align-items: end; gap: 48px; margin-bottom: 40px; }
.section-heading h2 { margin: 0; font: 500 clamp(40px, 5vw, 62px)/1.1 Georgia, "Songti SC", serif; letter-spacing: -.04em; }
.section-heading > p { margin: 0; color: var(--muted-strong); line-height: 1.9; }
.category-filter { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 28px; }
.category-filter button { padding: 9px 16px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted-strong); background: rgba(255,255,255,.68); }
.category-filter button.active { color: #fff; border-color: var(--ink); background: var(--ink); }
.project-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
.project-card { position: relative; min-height: 390px; padding: 28px; display: flex; flex-direction: column; border: 1px solid var(--line); border-radius: 26px; background: rgba(255,253,249,.84); box-shadow: var(--shadow-sm); overflow: hidden; transition: transform .25s ease, box-shadow .25s ease; }
.project-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }
.project-card::before { content: ""; position: absolute; width: 230px; height: 230px; right: -90px; top: -110px; border: 1px solid var(--rose-100); border-radius: 50%; box-shadow: 0 0 0 28px rgba(247,225,229,.25), 0 0 0 56px rgba(247,225,229,.1); }
.project-card.featured { min-height: 430px; grid-column: span 2; color: #fff; border-color: transparent; background: linear-gradient(135deg, #704853 0%, #9e6875 58%, #837b71 100%); }
.project-card.featured::before { width: 420px; height: 420px; right: -70px; top: -180px; border-color: rgba(255,255,255,.16); box-shadow: 0 0 0 58px rgba(255,255,255,.05), 0 0 0 116px rgba(255,255,255,.025); }
.project-topline { position: relative; z-index: 1; display: flex; align-items: center; gap: 10px; color: var(--muted); font-size: 10px; letter-spacing: .12em; }
.project-number { font: 22px Georgia, serif; letter-spacing: 0; color: var(--rose-400, var(--rose-500)); }
.project-category { padding-right: 10px; border-right: 1px solid var(--line); text-transform: uppercase; }
.project-status { margin-left: auto; display: flex; align-items: center; gap: 7px; letter-spacing: .08em; }
.project-status i { width: 6px; height: 6px; border-radius: 50%; background: #76917b; box-shadow: 0 0 0 4px rgba(118,145,123,.12); }
.featured .project-topline { color: rgba(255,255,255,.62); }.featured .project-number { color: #f0cbd3; }.featured .project-category { border-color: rgba(255,255,255,.18); }.featured .project-status i { background: #c5d8c7; }
.project-symbol { position: absolute; z-index: 0; right: 28px; top: 76px; color: var(--rose-100); font: 110px/1 Georgia, serif; opacity: .75; }
.featured .project-symbol { right: 54px; top: 95px; color: rgba(255,255,255,.1); font-size: 190px; }
.project-copy { position: relative; z-index: 1; max-width: 760px; margin-top: auto; }
.project-copy h3 { margin: 0; font: 500 clamp(28px, 4vw, 46px)/1.15 Georgia, "Songti SC", serif; letter-spacing: -.03em; }
.project-copy p { max-width: 680px; margin: 17px 0 0; color: var(--muted-strong); line-height: 1.85; white-space: pre-line; }
.featured .project-copy p { color: rgba(255,255,255,.74); font-size: 16px; }
.project-tags { position: relative; z-index: 1; display: flex; flex-wrap: wrap; gap: 7px; margin-top: 22px; }
.project-tags span { padding: 6px 10px; border: 1px solid var(--line); border-radius: 999px; color: var(--muted); font-size: 11px; background: rgba(255,255,255,.46); }
.featured .project-tags span { color: rgba(255,255,255,.72); border-color: rgba(255,255,255,.18); background: rgba(255,255,255,.06); }
.project-links { position: relative; z-index: 1; display: flex; flex-wrap: wrap; gap: 18px; margin-top: 24px; }
.project-links a { padding-bottom: 3px; border-bottom: 1px solid currentColor; color: var(--rose-700); font-size: 13px; text-decoration: none; }
.project-links span { margin-left: 7px; }.featured .project-links a { color: #fff; }
.featured-label { position: absolute; right: 25px; bottom: 25px; color: rgba(255,255,255,.36); font-size: 9px; letter-spacing: .22em; writing-mode: vertical-rl; }
.friends-section { padding: 110px 0 120px; background: linear-gradient(150deg, rgba(248,242,237,.96), rgba(237,239,232,.78)); border-block: 1px solid var(--line); }
.friends-inner { width: min(1180px, calc(100% - 40px)); margin: 0 auto; }
.friend-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 13px; }
.friend-card { position: relative; min-height: 210px; padding: 24px; display: grid; grid-template-columns: 58px 1fr; align-content: center; gap: 17px; border: 1px solid rgba(76,57,52,.1); border-radius: 22px; text-decoration: none; background: rgba(255,253,249,.72); transition: .22s ease; overflow: hidden; }
.friend-card:hover { transform: translateY(-3px); border-color: var(--rose-200); background: var(--paper); box-shadow: var(--shadow-sm); }
.friend-index { position: absolute; right: 16px; top: 12px; color: var(--rose-200); font: 29px Georgia, serif; }
.friend-avatar { width: 58px; height: 58px; padding: 3px; border: 1px solid var(--rose-200); border-radius: 50%; }
.friend-avatar img, .friend-avatar > span { width: 100%; height: 100%; display: grid; place-items: center; object-fit: cover; border-radius: 50%; color: var(--rose-700); background: var(--rose-50); font: 22px Georgia, serif; }
.friend-copy { min-width: 0; }.friend-copy h3 { margin: 1px 0 7px; font: 500 21px Georgia, "Songti SC", serif; }
.friend-copy p { min-height: 3.2em; margin: 0; color: var(--muted-strong); font-size: 13px; line-height: 1.65; }
.friend-copy small { display: block; max-width: 100%; margin-top: 14px; overflow: hidden; color: var(--rose-600); text-overflow: ellipsis; white-space: nowrap; }
.friend-arrow { position: absolute; right: 18px; bottom: 16px; color: var(--rose-500); }
.showcase-state { min-height: 220px; padding: 40px; display: grid; place-items: center; align-content: center; gap: 8px; border: 1px dashed var(--rose-200); border-radius: 24px; color: var(--muted); text-align: center; background: rgba(255,255,255,.45); }
.showcase-state > span { color: var(--rose-400, var(--rose-500)); font-size: 30px; }.showcase-state strong { color: var(--ink); font: 500 23px Georgia, "Songti SC", serif; }.showcase-state p { margin: 0; }.showcase-state.error { color: #a84d4d; }
@media (max-width: 900px) {
  .showcase-hero { grid-template-columns: 1fr 300px; gap: 30px; }.hero-orbit { width: 290px; }.friend-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 720px) {
  .showcase-hero { min-height: auto; grid-template-columns: 1fr; padding: 72px 0 84px; }.hero-orbit { width: min(300px, 86vw); justify-self: center; }.section-heading { grid-template-columns: 1fr; gap: 18px; }.content-section, .friends-section { padding-block: 78px; }.project-grid, .friend-grid { grid-template-columns: 1fr; }.project-card, .project-card.featured { min-height: 380px; grid-column: span 1; }.featured .project-symbol { right: 24px; font-size: 140px; }.friend-card { min-height: 190px; }
}
@media (max-width: 430px) {
  .showcase-hero, .content-section, .friends-inner { width: calc(100% - 28px); }.hero-copy h1 { font-size: 54px; }.project-card { padding: 22px; }.project-topline { align-items: flex-start; flex-wrap: wrap; }.project-status { width: 100%; margin-left: 0; }.featured-label { display: none; }
}
</style>
