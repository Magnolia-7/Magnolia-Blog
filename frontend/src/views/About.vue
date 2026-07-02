<template>
  <div class="about-page">
    <section class="about-card">
      <div class="profile-header">
        <div class="avatar-wrap">
          <img
            v-if="about.avatar"
            :src="about.avatar"
            alt="头像"
            class="avatar"
          />
          <div v-else class="avatar-placeholder">
            ✦
          </div>
        </div>

        <div class="profile-main">
          <p class="eyebrow">About me</p>
          <h1>{{ about.nickname || "Magnolia" }}</h1>
          <p class="signature">
            {{ about.signature || "在理性里，保留一点温柔。" }}
          </p>
        </div>
      </div>

      <div class="about-grid">
        <div class="info-block">
          <h2>个人说明</h2>
          <p>{{ about.bio || "暂无个人说明" }}</p>
        </div>

        <div class="info-block">
          <h2>兴趣爱好</h2>
          <p>{{ about.interests || "暂无兴趣信息" }}</p>
        </div>

        <div class="info-block">
          <h2>能力</h2>
          <p>{{ about.skills || "暂无能力信息" }}</p>
        </div>

        <div class="info-block">
          <h2>联系方式</h2>
          <p>{{ about.contacts || "暂无联系方式" }}</p>
        </div>
      </div>

      <section class="status-card">
        <div>
          <span>当前心情</span>
          <strong>{{ about.mood || "安静建设中" }}</strong>
        </div>

        <div>
          <span>短期目标</span>
          <strong>{{ about.short_goal || "继续完善博客" }}</strong>
        </div>

        <div>
          <span>长期目标</span>
          <strong>{{ about.long_goal || "成为更好的自己" }}</strong>
        </div>
      </section>

      <section class="tech-card">
        <h2>技术栈</h2>

        <div v-if="techLinks.length" class="tech-links">
          <a
            v-for="link in techLinks"
            :key="`${link.name}-${link.url}`"
            :href="link.url"
            target="_blank"
            rel="noopener noreferrer"
          >
            {{ link.name }}
          </a>
        </div>

        <p v-else>暂无技术栈</p>
      </section>

      <section class="social-card">
        <h2>社交链接</h2>

        <div v-if="socialLinks.length" class="social-links">
          <a
            v-for="link in socialLinks"
            :key="`${link.name}-${link.url}`"
            :href="link.url"
            target="_blank"
            rel="noopener noreferrer"
          >
            {{ link.name }}
          </a>
        </div>

        <p v-else>暂无社交链接</p>
      </section>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { getAbout } from "../api/about";

const about = ref({
  avatar: "",
  nickname: "",
  signature: "",
  bio: "",
  interests: "",
  skills: "",
  contacts: "",
  mood: "",
  short_goal: "",
  long_goal: "",
  social_links: "",
  tech_stack: "",
});

const socialLinks = computed(() => {
  return normalizeLinkEntries(about.value.social_links);
});

const techLinks = computed(() => {
  return normalizeLinkEntries(about.value.tech_stack);
});

function normalizeLinkEntries(value) {
  if (!value) {
    return [];
  }

  let entries = value;

  if (typeof value === "string") {
    try {
      entries = JSON.parse(value);
    } catch (error) {
      console.error("链接 JSON 解析失败：", error);
      return [];
    }
  }

  if (!Array.isArray(entries) && typeof entries === "object") {
    entries = Object.entries(entries).map(([name, url]) => ({ name, url }));
  }

  if (!Array.isArray(entries)) {
    return [];
  }

  return entries
    .map((link) => ({
      name: link.name || link.label || getSingleObjectKey(link) || "链接",
      url: link.url || link.href || getSingleObjectValue(link) || "",
    }))
    .filter((link) => link.url);
}

function getSingleObjectKey(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return "";
  }

  const keys = Object.keys(value);
  return keys.length === 1 ? keys[0] : "";
}

function getSingleObjectValue(value) {
  const key = getSingleObjectKey(value);
  return key ? value[key] : "";
}

async function loadAbout() {
  try {
    const response = await getAbout();
    if (response.data) {
      about.value = response.data;
    }
  } catch (error) {
    console.error(error);
  }
}

onMounted(() => {
  loadAbout();
});
</script>

<style scoped>
.about-page {
  max-width: 1080px;
  margin: 0 auto;
  padding: 72px 24px;
}

.about-card {
  padding: 42px;
  border: 1px solid rgba(90, 50, 64, 0.08);
  border-radius: 34px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 24px 72px rgba(90, 50, 64, 0.06);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 32px;
  margin-bottom: 42px;
}

.avatar-wrap {
  width: 132px;
  height: 132px;
  flex-shrink: 0;
  padding: 5px;
  border-radius: 50%;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 235, 241, 0.8));
  box-shadow: 0 18px 42px rgba(184, 123, 139, 0.18);
}

.avatar {
  width: 100%;
  height: 100%;
  display: block;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: #b87b8b;
  font-size: 42px;
  background: #fff1f5;
}

.eyebrow {
  margin: 0 0 10px;
  color: #b87b8b;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.profile-main h1 {
  margin: 0;
  color: #151515;
  font-size: 44px;
  line-height: 1.1;
  letter-spacing: -1.2px;
}

.signature {
  margin: 16px 0 0;
  color: #6f6065;
  font-size: 18px;
  line-height: 1.8;
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.info-block {
  padding: 24px;
  border: 1px solid rgba(90, 50, 64, 0.07);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.62);
}

.info-block h2,
.tech-card h2,
.social-card h2 {
  margin: 0 0 12px;
  color: #1f1f1f;
  font-size: 18px;
}

.info-block p,
.tech-card p,
.social-card p {
  margin: 0;
  color: #5d5558;
  line-height: 1.9;
  white-space: pre-line;
}

.status-card {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 18px;
}

.status-card div {
  padding: 22px;
  border-radius: 22px;
  background: rgba(255, 241, 245, 0.68);
  border: 1px solid rgba(216, 154, 170, 0.18);
}

.status-card span {
  display: block;
  margin-bottom: 10px;
  color: #9f6473;
  font-size: 13px;
}

.status-card strong {
  color: #2f2f2f;
  font-size: 16px;
  line-height: 1.6;
}

.tech-card {
  margin-top: 18px;
  padding: 24px;
  border: 1px solid rgba(90, 50, 64, 0.07);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.62);
}

.social-card {
  margin-top: 18px;
  padding: 24px;
  border: 1px solid rgba(90, 50, 64, 0.07);
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.62);
}

.tech-links,
.social-links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tech-links a,
.social-links a {
  display: inline-flex;
  align-items: center;
  min-height: 38px;
  padding: 8px 16px;
  border: 1px solid rgba(216, 154, 170, 0.28);
  border-radius: 999px;
  color: #9f6473;
  background: rgba(255, 247, 250, 0.78);
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition:
    color 0.2s ease,
    background 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease;
}

.tech-links a:hover,
.social-links a:hover {
  color: #fff;
  border-color: #b87b8b;
  background: #b87b8b;
  transform: translateY(-1px);
}

@media (max-width: 760px) {
  .about-page {
    padding: 42px 18px;
  }

  .about-card {
    padding: 26px;
  }

  .profile-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .about-grid,
  .status-card {
    grid-template-columns: 1fr;
  }

  .profile-main h1 {
    font-size: 34px;
  }
}
</style>
