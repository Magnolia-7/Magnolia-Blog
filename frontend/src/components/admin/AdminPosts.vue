<template>
  <section>
    <div class="admin-section-head"><div><p class="eyebrow">Writing desk</p><h2>文章管理</h2></div><button class="primary-button" type="button" :disabled="saving || deletingId !== null" @click="startCreate">写新文章</button></div>
    <AdminNotice :message="notice" :success="success" @close="notice = ''" />
    <form v-if="showEditor" class="editor-panel" @submit.prevent="savePost">
      <div class="form-grid two"><div class="field"><label>文章标题</label><input v-model="form.title" required maxlength="200" /></div><div class="field"><label>标签（逗号分隔）</label><input v-model="form.tags" placeholder="Vue, 学习记录" /></div></div>
      <div class="field"><label>摘要</label><textarea v-model="form.summary" rows="2"></textarea></div>
      <div class="form-grid three"><div class="field"><label>分类</label><select v-model="form.category"><option value="life">生活记录</option><option value="study">学习笔记</option></select></div><div class="field"><label>状态</label><select v-model="form.status"><option value="draft">草稿</option><option value="published">已发布</option></select></div><div class="field"><label>发布时间</label><input v-model="form.published_at" type="datetime-local" /></div></div>
      <label class="check-row"><input v-model="form.is_pinned" type="checkbox" /> 置顶这篇文章</label>
      <div class="cover-field">
        <div class="field"><label>封面地址</label><input v-model="form.cover_image" placeholder="上传后自动填写，也可以从媒体库选择" /></div>
        <ImageUploader compact label="上传封面" @uploaded="setCover" />
      </div>
      <div v-if="form.cover_image" class="cover-preview"><img :src="form.cover_image" alt="文章封面预览" /><button type="button" @click="form.cover_image = ''">移除</button></div>
      <div v-if="media.length" class="media-picker"><small>从媒体库选择封面</small><div><button v-for="asset in media.slice(0, 12)" :key="asset.id" type="button" :class="{ selected: form.cover_image === asset.url }" @click="form.cover_image = asset.url"><img :src="asset.thumbnail_url || asset.url" :alt="asset.original_name" /></button></div></div>
      <div class="markdown-toolbar"><strong>Markdown 正文</strong><ImageUploader compact label="上传并插入图片" @uploaded="insertImage" /></div>
      <div class="markdown-editor"><textarea ref="contentInput" v-model="form.content" rows="20" required placeholder="# 从这里开始书写…"></textarea><div class="markdown-preview"><div v-if="form.content" v-html="preview"></div><p v-else>正文预览会显示在这里。</p></div></div>
      <div class="form-actions"><button class="primary-button" :disabled="saving">{{ saving ? "正在保存…" : editingId ? "保存修改" : "创建文章" }}</button><button class="secondary-button" type="button" :disabled="saving" @click="cancelEdit">取消</button></div>
    </form>

    <form class="admin-filters" @submit.prevent="applyFilters">
      <div class="field filter-keyword"><label>搜索文章</label><input v-model.trim="filterDraft.keyword" placeholder="输入标题、摘要或标签" /></div>
      <div class="field"><label>分类</label><select v-model="filterDraft.category"><option value="">全部分类</option><option value="life">生活记录</option><option value="study">学习笔记</option></select></div>
      <div class="field"><label>状态</label><select v-model="filterDraft.status"><option value="">全部状态</option><option value="draft">草稿</option><option value="published">已发布</option></select></div>
      <button class="primary-button" :disabled="loading">{{ loading ? "读取中…" : "筛选" }}</button><button class="secondary-button" type="button" :disabled="loading" @click="resetFilters">重置</button>
      <span class="result-count">共 {{ pagination.total }} 篇</span>
    </form>

    <div v-if="loading" class="admin-empty">正在读取文章…</div>
    <div v-else-if="!posts.length" class="admin-empty">没有找到符合条件的文章。</div>
    <div v-else class="admin-list">
      <article v-for="post in posts" :key="post.id"><img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" /><div class="list-copy"><small>{{ post.category === "life" ? "生活记录" : "学习笔记" }} · {{ post.status === "published" ? "已发布" : "草稿" }}</small><h3>{{ post.title }}</h3><p>{{ post.summary || "没有摘要" }}</p></div><div class="row-actions"><button class="secondary-button" :disabled="deletingId !== null" @click="editPost(post)">编辑</button><button class="danger-button" :disabled="deletingId !== null" @click="removePost(post)">{{ deletingId === post.id ? "删除中…" : "删除" }}</button></div></article>
    </div>
    <AdminPagination class="post-pagination" :page="pagination.page" :total-pages="pagination.totalPages" :loading="loading" label="文章分页" @change="loadPosts" />
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, reactive, ref } from "vue";
import AdminNotice from "./AdminNotice.vue";
import AdminPagination from "./AdminPagination.vue";
import ImageUploader from "../ImageUploader.vue";
import { renderMarkdown } from "../../utils/markdown";
import { createAdminPost, deleteAdminPost, getAdminPosts, updateAdminPost } from "../../api/posts";
import { getMedia } from "../../api/media";
const posts = ref([]); const media = ref([]); const loading = ref(true); const saving = ref(false); const deletingId = ref(null); const showEditor = ref(false); const editingId = ref(null); const contentInput = ref(null); const notice = ref(""); const success = ref(false);
const filterDraft = reactive({ keyword: "", category: "", status: "" });
const filters = reactive({ keyword: "", category: "", status: "" });
const pagination = reactive({ page: 1, pageSize: 10, total: 0, totalPages: 0 });
const defaults = () => ({ title: "", summary: "", content: "", cover_image: "", category: "life", status: "draft", tags: "", is_pinned: false, published_at: "" });
const form = reactive(defaults()); const preview = computed(() => renderMarkdown(form.content));
function toLocalInput(value) { if (!value) return ""; const date = new Date(value); const local = new Date(date.getTime() - date.getTimezoneOffset() * 60000); return local.toISOString().slice(0, 16); }
function reset() { Object.assign(form, defaults()); editingId.value = null; notice.value = ""; }
function startCreate() { reset(); showEditor.value = true; window.scrollTo({ top: 0, behavior: "smooth" }); }
function editPost(post) { Object.assign(form, { ...defaults(), ...post, published_at: toLocalInput(post.published_at) }); editingId.value = post.id; showEditor.value = true; window.scrollTo({ top: 0, behavior: "smooth" }); }
function cancelEdit() { showEditor.value = false; reset(); }
function setCover(asset) { form.cover_image = asset.url; media.value.unshift(asset); }
async function loadPosts(page = 1) { loading.value = true; try { const { data } = await getAdminPosts({ page, page_size: pagination.pageSize, keyword: filters.keyword || undefined, category: filters.category || undefined, status: filters.status || undefined }); if (!data.items.length && data.total > 0 && page > data.total_pages) { await loadPosts(data.total_pages); return; } posts.value = data.items; Object.assign(pagination, { page: data.page, pageSize: data.page_size, total: data.total, totalPages: data.total_pages }); } catch (error) { posts.value = []; success.value = false; notice.value = error.response?.data?.detail || "文章列表加载失败。"; } finally { loading.value = false; } }
function applyFilters() { Object.assign(filters, filterDraft); loadPosts(1); }
function resetFilters() { Object.assign(filterDraft, { keyword: "", category: "", status: "" }); Object.assign(filters, filterDraft); loadPosts(1); }
async function insertImage(asset) { media.value.unshift(asset); const markdown = `\n![${asset.original_name}](${asset.url})\n`; const input = contentInput.value; if (!input) { form.content += markdown; return; } const start = input.selectionStart; form.content = form.content.slice(0, start) + markdown + form.content.slice(input.selectionEnd); await nextTick(); input.focus(); input.setSelectionRange(start + markdown.length, start + markdown.length); }
async function savePost() { saving.value = true; notice.value = ""; const targetPage = editingId.value ? pagination.page : 1; try { const payload = { ...form, published_at: form.published_at ? new Date(form.published_at).toISOString() : null }; if (editingId.value) await updateAdminPost(editingId.value, payload); else await createAdminPost(payload); showEditor.value = false; Object.assign(form, defaults()); editingId.value = null; success.value = true; notice.value = "文章已保存。"; await loadPosts(targetPage); } catch (error) { success.value = false; notice.value = error.response?.data?.detail || "文章保存失败。"; } finally { saving.value = false; } }
async function removePost(post) { if (!window.confirm(`删除「${post.title}」？`)) return; deletingId.value = post.id; try { await deleteAdminPost(post.id); const targetPage = posts.value.length === 1 && pagination.page > 1 ? pagination.page - 1 : pagination.page; success.value = true; notice.value = "文章已删除。"; await loadPosts(targetPage); } catch (error) { notice.value = error.response?.data?.detail || "文章删除失败。"; success.value = false; } finally { deletingId.value = null; } }
onMounted(async () => { const [, mediaResult] = await Promise.allSettled([loadPosts(), getMedia()]); if (mediaResult.status === "fulfilled") media.value = mediaResult.value.data; });
</script>

<style scoped>
.admin-section-head { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 22px; }.admin-section-head h2 { margin: 0; font: 500 32px Georgia, "Songti SC", serif; }.editor-panel { margin-bottom: 30px; padding: 24px; display: grid; gap: 18px; border: 1px solid var(--rose-200); border-radius: 18px; background: rgba(252,240,242,.3); }.form-grid { display: grid; gap: 14px; }.form-grid.two { grid-template-columns: 1.4fr .6fr; }.form-grid.three { grid-template-columns: repeat(3, 1fr); }.check-row { color: var(--muted-strong); font-size: 13px; }.cover-field { display: grid; grid-template-columns: 1fr 260px; gap: 12px; align-items: end; }.cover-preview { position: relative; width: 220px; }.cover-preview img { width: 100%; aspect-ratio: 1.6; object-fit: cover; border-radius: 12px; }.cover-preview button { position: absolute; right: 7px; top: 7px; border: 0; border-radius: 999px; color: #fff; background: rgba(0,0,0,.65); }.media-picker > small { color: var(--muted); }.media-picker > div { display: flex; gap: 7px; margin-top: 7px; overflow-x: auto; }.media-picker button { width: 70px; height: 52px; padding: 0; flex: 0 0 auto; border: 2px solid transparent; border-radius: 8px; overflow: hidden; }.media-picker button.selected { border-color: var(--rose-600); }.media-picker img { width: 100%; height: 100%; object-fit: cover; }.markdown-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 18px; }.markdown-editor { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--line); border-radius: 14px; overflow: hidden; background: #fff; }.markdown-editor > textarea { width: 100%; padding: 18px; border: 0; border-right: 1px solid var(--line); outline: 0; resize: vertical; font: 13px/1.75 "SFMono-Regular", Consolas, monospace; }.markdown-preview { max-height: 550px; padding: 18px; overflow: auto; color: var(--muted-strong); line-height: 1.8; }.markdown-preview :deep(img) { max-width: 100%; border-radius: 10px; }.markdown-preview :deep(pre) { padding: 12px; color: #fff; background: #2e2928; border-radius: 8px; overflow: auto; }.form-actions { display: flex; align-items: center; gap: 10px; }.admin-filters { margin-bottom: 18px; padding: 14px; display: grid; grid-template-columns: minmax(220px, 1fr) 150px 150px auto auto auto; gap: 10px; align-items: end; border: 1px solid var(--line); border-radius: 14px; background: rgba(255,255,255,.72); }.admin-filters input, .admin-filters select { width: 100%; }.result-count { align-self: center; color: var(--muted); font-size: 12px; white-space: nowrap; }.admin-list { display: grid; gap: 10px; }.admin-list article { padding: 13px; display: grid; grid-template-columns: 90px 1fr auto; gap: 16px; align-items: center; border: 1px solid var(--line); border-radius: 14px; background: #fff; }.admin-list article > img { width: 90px; height: 68px; object-fit: cover; border-radius: 9px; }.list-copy small { color: var(--rose-600); }.list-copy h3 { margin: 5px 0; }.list-copy p { margin: 0; color: var(--muted); font-size: 12px; }.row-actions { display: flex; gap: 7px; }.row-actions button { min-height: 34px; padding: 0 11px; }.post-pagination { margin-top: 18px; }.admin-empty { padding: 24px; text-align: center; color: var(--muted); border: 1px dashed var(--line); border-radius: 14px; }
@media (max-width: 980px) { .admin-filters { grid-template-columns: 1fr 1fr 1fr; }.result-count { justify-self: end; } }
@media (max-width: 760px) { .form-grid.two, .form-grid.three, .cover-field, .markdown-editor, .admin-filters { grid-template-columns: 1fr; }.admin-filters .primary-button, .admin-filters .secondary-button { width: 100%; }.result-count { justify-self: start; }.markdown-editor > textarea { border-right: 0; border-bottom: 1px solid var(--line); }.admin-list article { grid-template-columns: 1fr; }.admin-list article > img { width: 100%; height: 160px; }.row-actions { justify-content: flex-end; } }
</style>
