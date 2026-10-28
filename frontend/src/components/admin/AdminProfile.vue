<template>
  <section>
    <div class="admin-section-head"><div><p class="eyebrow">Identity & status</p><h2>个人资料</h2></div><span v-if="notice" :class="success ? 'success-text' : 'error-text'">{{ notice }}</span></div>
    <form class="profile-form" @submit.prevent="saveAbout">
      <div class="form-grid two"><div class="field"><label>昵称</label><input v-model="form.nickname" /></div><div class="field"><label>个性签名</label><input v-model="form.signature" /></div></div>
      <div class="field"><label>个人标签（逗号分隔）</label><input v-model="profileTagsText" placeholder="逗号分隔" /></div>
      <div class="field"><label>个人说明</label><textarea v-model="form.bio" rows="5"></textarea></div>
      <div class="form-grid two"><div class="field"><label>兴趣爱好</label><textarea v-model="form.interests" rows="4"></textarea></div><div class="field"><label>正在培养</label><textarea v-model="form.skills" rows="4"></textarea></div></div>
      <div class="field"><label>联系方式</label><textarea v-model="form.contacts" rows="3"></textarea></div>
      <div class="form-grid three"><div class="field"><label>当前心情</label><input v-model="form.mood" /></div><div class="field"><label>短期目标</label><input v-model="form.short_goal" /></div><div class="field"><label>长期目标</label><input v-model="form.long_goal" /></div></div>
      <div class="form-grid two"><div class="field"><label>关于页正在听的歌</label><input v-model="form.current_song" /></div><div class="field"><label>歌曲链接</label><input v-model="form.current_song_url" type="url" /></div></div>
      <button class="primary-button" :disabled="saving || !loaded">{{ saving ? "正在保存…" : "保存个人资料" }}</button>
    </form>

    <div class="resource-columns">
      <section class="resource-box"><h3>社交账号</h3><form class="quick-form" @submit.prevent="addSocial"><input v-model="socialDraft.name" required placeholder="平台名称" /><input v-model="socialDraft.url" required type="url" placeholder="主页链接" /><button class="primary-button">添加</button></form><div class="resource-list"><article v-for="item in socialLinks" :key="item.id"><input v-model="item.name" /><input v-model="item.url" /><label><input v-model="item.enabled" type="checkbox" /> 显示</label><button @click="saveResource('social-links', item)">保存</button><button class="remove" @click="removeResource('social-links', item)">删除</button></article></div></section>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { getAdminAbout, updateAdminAbout } from "../../api/about";
import { createAdminResource, deleteAdminResource, getAdminResource, updateAdminResource } from "../../api/content";
import { apiError } from "../../utils/format";
const defaults = { nickname: "", signature: "", bio: "", interests: "", skills: "", contacts: "", mood: "", short_goal: "", long_goal: "", current_song: "", current_song_url: "", profile_tags: "" };
const form = reactive({ ...defaults }), saving = ref(false), notice = ref(""), success = ref(false), socialLinks = ref([]), loaded = ref(false);
const socialDraft = reactive({ name: "", url: "", icon: "", enabled: true, sort_order: 0 });
const profileTagsText = computed({ get() { try { const tags = JSON.parse(form.profile_tags || "[]"); return Array.isArray(tags) ? tags.join(", ") : ""; } catch { return form.profile_tags || ""; } }, set(value) { form.profile_tags = JSON.stringify(value.split(/[,，]/).map((tag) => tag.trim()).filter(Boolean)); } });
async function saveAbout() { if (!loaded.value) return; saving.value = true; notice.value = ""; try { const payload = Object.fromEntries(Object.keys(defaults).map((key) => [key, form[key] || null])); await updateAdminAbout(payload); success.value = true; notice.value = "个人资料已保存。"; } catch (error) { success.value = false; notice.value = apiError(error); } finally { saving.value = false; } }
async function addSocial() { try { const { data } = await createAdminResource("social-links", socialDraft); socialLinks.value.push(data); Object.assign(socialDraft, { name: "", url: "", icon: "", enabled: true, sort_order: socialLinks.value.length }); } catch (error) { success.value = false; notice.value = apiError(error); } }
async function saveResource(resource, item) { try { await updateAdminResource(resource, item.id, item); success.value = true; notice.value = "条目已保存。"; } catch (error) { success.value = false; notice.value = apiError(error); } }
async function removeResource(resource, item) { if (!window.confirm(`删除「${item.name}」？`)) return; try { await deleteAdminResource(resource, item.id); socialLinks.value = socialLinks.value.filter((entry) => entry.id !== item.id); } catch (error) { success.value = false; notice.value = apiError(error); } }
onMounted(async () => { const [about, social] = await Promise.allSettled([getAdminAbout(), getAdminResource("social-links")]); if (about.status === "fulfilled") { for (const key of Object.keys(defaults)) form[key] = about.value.data?.[key] || ""; loaded.value = true; } else notice.value = "个人资料加载失败，请刷新重试。"; if (social.status === "fulfilled") socialLinks.value = social.value.data; });
</script>

<style scoped>
.admin-section-head { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 22px; }.admin-section-head h2 { margin: 0; font: 500 32px Georgia, "Songti SC", serif; }.profile-form { padding: 24px; display: grid; gap: 17px; border: 1px solid var(--line); border-radius: 18px; background: rgba(255,255,255,.7); }.form-grid { display: grid; gap: 14px; }.form-grid.two { grid-template-columns: 1fr 1fr; }.form-grid.three { grid-template-columns: repeat(3, 1fr); }.avatar-editor { display: grid; grid-template-columns: 110px 1fr; gap: 18px; align-items: center; }.avatar-preview { width: 110px; height: 110px; display: grid; place-items: center; border-radius: 50%; color: var(--rose-700); background: var(--rose-50); font: 42px Georgia, serif; overflow: hidden; }.avatar-preview img { width: 100%; height: 100%; object-fit: cover; }.avatar-controls { display: grid; grid-template-columns: 1fr 220px; align-items: end; gap: 10px; }.resource-columns { display: grid; grid-template-columns: 1fr; gap: 20px; margin-top: 26px; }.resource-box { padding: 20px; border: 1px solid var(--line); border-radius: 18px; background: #fff; }.resource-box h3 { margin-top: 0; font: 500 23px Georgia, "Songti SC", serif; }.quick-form { display: grid; grid-template-columns: 1fr 1fr auto; gap: 7px; }.quick-form input, .quick-form select, .resource-list input, .resource-list select { min-width: 0; padding: 9px; border: 1px solid var(--line); border-radius: 9px; }.resource-list { display: grid; gap: 8px; margin-top: 14px; }.resource-list article { padding-top: 8px; display: grid; grid-template-columns: 1fr 1.4fr auto auto auto; gap: 6px; align-items: center; border-top: 1px solid var(--line); }.resource-list label { color: var(--muted); font-size: 11px; white-space: nowrap; }.resource-list button { padding: 7px; border: 0; color: var(--rose-700); background: transparent; }.resource-list .remove { color: #a84d4d; }
@media (max-width: 900px) { .resource-columns { grid-template-columns: 1fr; } .form-grid.three { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 650px) { .form-grid.two, .form-grid.three, .avatar-controls { grid-template-columns: 1fr; }.avatar-editor { grid-template-columns: 1fr; }.quick-form { grid-template-columns: 1fr; }.resource-list article { grid-template-columns: 1fr 1fr; } }
</style>
