<template>
  <div class="page-shell about-page">
    <header class="page-heading"><h1>ABOUT</h1></header>
    <div v-if="loading" class="state-card" role="status">加载中…</div>
    <div v-else-if="error" class="state-card error" role="alert">
      {{ error }} <button type="button" class="text-button" @click="load">重试</button>
    </div>
    <template v-else>
      <section class="profile-layout">
        <div class="profile-picture"><img :src="avatar" :alt="about.nickname || 'Magnolia'" /></div>
        <div class="profile-copy">
          <h2 class="comic">{{ about.nickname || 'MAGNOLIA' }}</h2>
          <p v-if="about.signature">{{ about.signature }}</p>
          <p v-if="about.bio" class="profile-bio">{{ about.bio }}</p>
          <div v-if="profileTags.length" class="profile-tags"><span v-for="tag in profileTags" :key="tag">{{ tag }}</span></div>
        </div>
      </section>
      <dl v-if="about.interests || about.skills || about.contacts" class="profile-details">
        <div v-if="about.interests"><dt>兴趣</dt><dd>{{ about.interests }}</dd></div>
        <div v-if="about.skills"><dt>正在培养</dt><dd>{{ about.skills }}</dd></div>
        <div v-if="about.contacts"><dt>联系</dt><dd>{{ about.contacts }}</dd></div>
      </dl>
    </template>
    <section class="about-status-section" aria-label="当前状态">
      <header class="section-row"><h2 class="comic">STATUS</h2></header>
      <div class="about-status-grid">
        <article class="surface"><span>心情</span><p>{{ about.mood || '—' }}</p></article>
        <article class="surface"><span>短期目标</span><p>{{ about.short_goal || '—' }}</p></article>
        <article class="surface"><span>长期目标</span><p>{{ about.long_goal || '—' }}</p></article>
        <article class="surface"><span>正在听</span><p><a v-if="songUrl" :href="songUrl" target="_blank" rel="noopener noreferrer">{{ about.current_song || '—' }} ↗</a><template v-else>{{ about.current_song || '—' }}</template></p></article>
      </div>
    </section>
    <section class="about-social surface" aria-label="社交账号">
      <header class="section-row"><h2 class="comic">SOCIALS</h2></header>
      <p v-if="loading" class="muted" role="status">加载中…</p>
      <p v-else-if="socialError" class="error-text" role="alert">社交账号加载失败。 <button type="button" class="text-button" @click="load">重试</button></p>
      <div v-else-if="socials.length" class="about-social-links">
        <a v-for="link in socials" :key="link.id || link.url" :href="link.url" :target="/^https?:/i.test(link.url) ? '_blank' : undefined" rel="noopener noreferrer">
          <span class="social-initial comic" aria-hidden="true">{{ link.name.slice(0, 1) }}</span><span>{{ link.name }}</span><span aria-hidden="true">↗</span>
        </a>
      </div>
      <p v-else class="muted">暂无社交账号</p>
    </section>
    <TimeSummary />
  </div>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue';
import { getAbout } from '../api/about';
import { getSocialLinks } from '../api/content';
import { useSite } from '../composables/site';
import TimeSummary from '../components/TimeSummary.vue';

const { avatar } = useSite();
const about = ref({}), socials = ref([]), loading = ref(true), error = ref(''), socialError = ref(false);
const songUrl = computed(() => /^https?:\/\//i.test(about.value.current_song_url || '') ? about.value.current_song_url : '');
const profileTags = computed(() => {
  try {
    const value = JSON.parse(about.value.profile_tags || '[]');
    return Array.isArray(value) ? value.filter((tag) => typeof tag === 'string') : [];
  } catch {
    return (about.value.profile_tags || '').split(/[,，]/).map((tag) => tag.trim()).filter(Boolean);
  }
});
function legacyLinks(value) {
  try {
    const parsed = typeof value === 'string' ? JSON.parse(value || '[]') : value;
    if (!parsed || typeof parsed !== 'object') return [];
    return Array.isArray(parsed) ? parsed : Object.entries(parsed).map(([name, url]) => ({ name, url }));
  } catch { return []; }
}
function normalizeLinks(links) {
  return links.filter((link) => link && link.enabled !== false && typeof link.url === 'string')
    .map((link) => ({ ...link, name: String(link.name || link.url).trim(), url: link.url.trim() }))
    .filter((link) => /^(https?:\/\/|mailto:|tel:)/i.test(link.url));
}
async function load() {
  loading.value = true; error.value = ''; socialError.value = false;
  const [profile, links] = await Promise.allSettled([getAbout(), getSocialLinks()]);
  if (profile.status === 'fulfilled') about.value = profile.value.data || {};
  else error.value = '个人资料加载失败。';
  const source = links.status === 'fulfilled' && links.value.data.length ? links.value.data : legacyLinks(about.value.social_links);
  socials.value = normalizeLinks(source);
  socialError.value = links.status === 'rejected' && !socials.value.length;
  loading.value = false;
}
onMounted(load);
</script>
