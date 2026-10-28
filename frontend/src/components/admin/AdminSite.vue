<template>
  <section><header class="section-row"><h2>站点设置</h2></header><p v-if="loading" role="status">加载中…</p><form v-else class="site-settings-form" @submit.prevent="save"><div class="field"><label for="site-start">原始上线日期</label><input id="site-start" v-model="form.started_on" type="date" :max="today" required /><small>首页运行天数从此日期计算。</small></div><div class="field"><label for="site-avatar">头像地址</label><input id="site-avatar" v-model.trim="form.avatar_url" /><small>留空使用当前山治头像。</small><img class="site-avatar-preview" :src="form.avatar_url || '/images/sanji.jpg'" alt="头像预览" /><ImageUploader compact label="上传头像" @uploaded="form.avatar_url = $event.url" /></div><div class="field"><label for="site-hero">漫画背景图地址</label><input id="site-hero" v-model.trim="form.hero_image_url" /><small>留空使用当前合照。</small><img class="site-hero-preview" :src="form.hero_image_url || '/images/manga-crew.jpg'" alt="背景图预览" /><ImageUploader compact label="上传背景图" @uploaded="form.hero_image_url = $event.url" /></div><button class="primary-button" :disabled="saving || !!loadError">{{ saving ? '保存中…' : '保存站点设置' }}</button></form><p v-if="loadError" class="error-text" role="alert">{{ loadError }} <button class="text-button" type="button" @click="load">重试</button></p><p v-if="notice" :class="success ? 'success-text' : 'error-text'" role="status">{{ notice }}</p></section>
</template>
<script setup>
import { onMounted, reactive, ref } from 'vue';
import { getSiteSettings, saveSiteSettings } from '../../api/activity';
import { loadSite } from '../../composables/site';
import { apiError, todayISO } from '../../utils/format';
import ImageUploader from '../ImageUploader.vue';
const today = todayISO(), form = reactive({ started_on: today, avatar_url: '', hero_image_url: '' }), loading = ref(true), saving = ref(false), loadError = ref(''), notice = ref(''), success = ref(false);
async function load() { loading.value = true; loadError.value = ''; try { const { data } = await getSiteSettings(); Object.assign(form, { ...data, avatar_url: data.avatar_url || '', hero_image_url: data.hero_image_url || '' }); } catch (error) { loadError.value = apiError(error, '站点设置加载失败。'); } finally { loading.value = false; } }
async function save() { saving.value = true; notice.value = ''; try { await saveSiteSettings({ ...form }); await loadSite(true); success.value = true; notice.value = '站点设置已保存。'; } catch (error) { success.value = false; notice.value = apiError(error); } finally { saving.value = false; } }
onMounted(load);
</script>
<style scoped>
h2{font-size:25px;font-weight:500}.site-settings-form{display:grid;gap:24px;max-width:640px;margin-top:24px}.site-settings-form>.primary-button{justify-self:start}.site-avatar-preview{width:100px;height:100px;object-fit:cover;border-radius:50%;border:2px solid var(--ink);margin:12px 0}.site-hero-preview{max-height:220px;object-fit:contain;object-position:left;margin:12px 0}section>p{margin-top:18px}
</style>
