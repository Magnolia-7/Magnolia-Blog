<template>
  <section>
    <div class="admin-section-head"><div><p class="eyebrow">Media center</p><h2>媒体中心</h2></div><span>{{ assets.length }} 张图片 · {{ totalSize }}</span></div>
    <ImageUploader multiple label="上传一张或多张图片" @uploaded="handleUploaded" />
    <div v-if="loading" class="admin-empty">正在读取媒体库…</div>
    <div v-else-if="!assets.length" class="admin-empty">还没有上传图片。</div>
    <div v-else class="media-grid">
      <article v-for="asset in assets" :key="asset.id">
        <img :src="asset.thumbnail_url || asset.url" :alt="asset.original_name" loading="lazy" />
        <div><strong :title="asset.original_name">{{ asset.original_name }}</strong><small>{{ asset.width }} × {{ asset.height }} · {{ formatSize(asset.size_bytes) }}</small></div>
        <button type="button" class="delete-media" aria-label="删除图片" @click="remove(asset)">×</button>
      </article>
    </div>
    <p v-if="error" class="error-text">{{ error }}</p>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import ImageUploader from "../ImageUploader.vue";
import { deleteMedia, getMedia } from "../../api/media";
const assets = ref([]); const loading = ref(true); const error = ref("");
const totalSize = computed(() => formatSize(assets.value.reduce((sum, item) => sum + item.size_bytes, 0)));
function formatSize(bytes = 0) { if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`; return `${(bytes / 1024 / 1024).toFixed(1)} MB`; }
function handleUploaded(asset) { assets.value.unshift(asset); }
async function remove(asset) { if (!window.confirm(`删除「${asset.original_name}」？`)) return; try { await deleteMedia(asset.id); assets.value = assets.value.filter((item) => item.id !== asset.id); } catch (err) { error.value = err.response?.data?.detail || "图片删除失败。"; } }
onMounted(async () => { try { assets.value = (await getMedia()).data; } catch { error.value = "媒体库加载失败。"; } finally { loading.value = false; } });
</script>

<style scoped>
.admin-section-head { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 22px; }.admin-section-head h2 { margin: 0; font: 500 32px Georgia, "Songti SC", serif; }.admin-section-head > span { color: var(--muted); font-size: 12px; }.media-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 22px; }.media-grid article { position: relative; border: 1px solid var(--line); border-radius: 14px; background: #fff; overflow: hidden; }.media-grid img { width: 100%; aspect-ratio: 1.25; display: block; object-fit: cover; }.media-grid article > div { padding: 10px; display: grid; gap: 3px; }.media-grid strong { overflow: hidden; font-size: 11px; text-overflow: ellipsis; white-space: nowrap; }.media-grid small { color: var(--muted); font-size: 9px; }.delete-media { position: absolute; top: 7px; right: 7px; width: 28px; height: 28px; border: 0; border-radius: 50%; color: #fff; background: rgba(40,35,34,.7); }.admin-empty { margin-top: 20px; padding: 24px; color: var(--muted); text-align: center; border: 1px dashed var(--line); border-radius: 14px; }
@media (max-width: 800px) { .media-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
