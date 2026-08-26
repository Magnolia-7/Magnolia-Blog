<template>
  <div
    :class="['uploader', { dragging, compact }]"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="handleDrop"
  >
    <input ref="inputRef" type="file" accept="image/jpeg,image/png,image/webp" :multiple="multiple" @change="handleFiles" />
    <button type="button" class="upload-trigger" :disabled="uploading" @click="inputRef?.click()">
      <span>{{ uploading ? `${progress}%` : "＋" }}</span>
      <div><strong>{{ uploading ? "正在上传并压缩" : label }}</strong><small>支持拖拽、JPEG / PNG / WebP，单张不超过 10 MB</small></div>
    </button>
    <p v-if="error" class="error-text">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { uploadImage } from "../api/media";

const props = defineProps({ label: { type: String, default: "选择或拖入图片" }, multiple: Boolean, compact: Boolean });
const emit = defineEmits(["uploaded"]);
const inputRef = ref(null); const uploading = ref(false); const dragging = ref(false); const progress = ref(0); const error = ref("");

async function uploadFiles(files) {
  const selected = Array.from(files || []); if (!selected.length) return;
  uploading.value = true; error.value = "";
  try {
    for (const file of (props.multiple ? selected : selected.slice(0, 1))) {
      const { data } = await uploadImage(file, (event) => { if (event.total) progress.value = Math.round(event.loaded / event.total * 100); });
      emit("uploaded", data);
    }
  } catch (err) { error.value = err.response?.data?.detail || "图片上传失败，请检查格式和大小。"; }
  finally { uploading.value = false; dragging.value = false; progress.value = 0; if (inputRef.value) inputRef.value.value = ""; }
}
function handleFiles(event) { uploadFiles(event.target.files); }
function handleDrop(event) { uploadFiles(event.dataTransfer.files); }
</script>

<style scoped>
.uploader { padding: 14px; border: 1px dashed var(--rose-300); border-radius: 16px; background: rgba(252,240,242,.45); transition: .18s ease; }.uploader.dragging { border-color: var(--rose-600); background: var(--rose-50); transform: scale(1.005); }.uploader input { display: none; }.upload-trigger { width: 100%; padding: 4px; display: flex; align-items: center; gap: 13px; border: 0; text-align: left; background: transparent; }.upload-trigger > span { width: 42px; height: 42px; display: grid; place-items: center; flex: 0 0 auto; border-radius: 12px; color: #fff; background: var(--rose-600); font-size: 19px; }.upload-trigger div { display: grid; gap: 3px; }.upload-trigger strong { color: var(--ink); font-size: 13px; }.upload-trigger small { color: var(--muted); font-size: 10px; }.uploader.compact .upload-trigger small { display: none; }.error-text { margin: 9px 0 0; font-size: 12px; }
</style>
