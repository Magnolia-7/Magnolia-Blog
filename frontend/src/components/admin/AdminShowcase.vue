<template>
  <section>
    <div class="admin-section-head">
      <div><p class="eyebrow">Portfolio & neighbors</p><h2>作品与友链</h2></div>
      <p>维护项目档案和友邻站点；关闭“前台显示”即可暂时隐藏。</p>
    </div>
    <div class="subtabs">
      <button :class="{ active: active === 'projects' }" @click="active = 'projects'">项目展示 <span>{{ projects.length }}</span></button>
      <button :class="{ active: active === 'friend-links' }" @click="active = 'friend-links'">友链 <span>{{ friendLinks.length }}</span></button>
    </div>
    <AdminNotice :message="notice" :success="success" @close="notice = ''" />

    <section v-if="active === 'projects'" class="module-panel">
      <form class="card-form" @submit.prevent="createProject">
        <div class="form-grid three">
          <div class="field"><label>项目名称</label><input v-model.trim="projectDraft.title" required maxlength="160" placeholder="例如：Treeios" /></div>
          <div class="field"><label>项目类型</label><input v-model.trim="projectDraft.category" required maxlength="80" placeholder="应用 / 爬虫 / Skill" /></div>
          <div class="field"><label>当前状态</label><select v-model="projectDraft.status"><option value="building">构建中</option><option value="active">持续维护</option><option value="completed">已完成</option><option value="archived">已归档</option></select></div>
        </div>
        <div class="field"><label>项目描述</label><textarea v-model.trim="projectDraft.description" rows="4" required maxlength="3000" placeholder="它解决了什么问题，有哪些值得记录的设计？"></textarea></div>
        <div class="field"><label>标签</label><input v-model.trim="projectDraft.tags" maxlength="500" placeholder="Python, 自动化, 数据采集（用逗号分隔）" /></div>
        <div class="form-grid two">
          <div class="field"><label>GitHub 地址（可选）</label><input v-model.trim="projectDraft.github_url" type="url" placeholder="https://github.com/..." /></div>
          <div class="field"><label>项目 / 演示地址（可选）</label><input v-model.trim="projectDraft.demo_url" type="url" placeholder="https://..." /></div>
        </div>
        <div class="form-grid options-grid">
          <label class="check-field"><input v-model="projectDraft.featured" type="checkbox" /><span>设为精选项目</span></label>
          <label class="check-field"><input v-model="projectDraft.enabled" type="checkbox" /><span>在前台显示</span></label>
          <div class="field sort-field"><label>排序值</label><input v-model.number="projectDraft.sort_order" type="number" /></div>
          <button class="primary-button" :disabled="isBusy('create:projects')">{{ isBusy('create:projects') ? "添加中…" : "添加项目" }}</button>
        </div>
      </form>

      <div v-if="loading" class="admin-empty">正在读取项目…</div>
      <div v-else-if="!projects.length" class="admin-empty">还没有项目，先添加第一份作品档案吧。</div>
      <div v-else class="project-admin-list">
        <article v-for="project in projects" :key="project.id" :class="{ editing: editingProjectId === project.id, muted: !project.enabled }">
          <form v-if="editingProjectId === project.id" class="edit-form" @submit.prevent="saveProject(project)">
            <div class="form-grid three">
              <div class="field"><label>项目名称</label><input v-model.trim="projectEdit.title" required maxlength="160" /></div>
              <div class="field"><label>项目类型</label><input v-model.trim="projectEdit.category" required maxlength="80" /></div>
              <div class="field"><label>当前状态</label><select v-model="projectEdit.status"><option value="building">构建中</option><option value="active">持续维护</option><option value="completed">已完成</option><option value="archived">已归档</option></select></div>
            </div>
            <div class="field"><label>项目描述</label><textarea v-model.trim="projectEdit.description" rows="4" required maxlength="3000"></textarea></div>
            <div class="field"><label>标签</label><input v-model.trim="projectEdit.tags" maxlength="500" /></div>
            <div class="form-grid two">
              <div class="field"><label>GitHub 地址</label><input v-model.trim="projectEdit.github_url" type="url" /></div>
              <div class="field"><label>项目 / 演示地址</label><input v-model.trim="projectEdit.demo_url" type="url" /></div>
            </div>
            <div class="form-grid options-grid">
              <label class="check-field"><input v-model="projectEdit.featured" type="checkbox" /><span>精选项目</span></label>
              <label class="check-field"><input v-model="projectEdit.enabled" type="checkbox" /><span>前台显示</span></label>
              <div class="field sort-field"><label>排序值</label><input v-model.number="projectEdit.sort_order" type="number" /></div>
              <div class="edit-actions"><button class="primary-button" :disabled="isBusy(`save:projects:${project.id}`)">{{ isBusy(`save:projects:${project.id}`) ? "保存中…" : "保存修改" }}</button><button type="button" class="secondary-button" @click="editingProjectId = null">取消</button></div>
            </div>
          </form>
          <template v-else>
            <div class="project-mark">{{ projectSymbol(project.category) }}</div>
            <div class="item-copy">
              <div class="item-meta"><span>{{ project.category }}</span><span>{{ statusLabel(project.status) }}</span><span v-if="project.featured">精选</span><span v-if="!project.enabled">已隐藏</span></div>
              <h3>{{ project.title }}</h3>
              <p>{{ project.description }}</p>
              <small v-if="project.tags">{{ project.tags }}</small>
            </div>
            <div class="row-actions"><button @click="startProjectEdit(project)">编辑</button><button class="remove" :disabled="isBusy(`delete:projects:${project.id}`)" @click="remove('projects', project)">{{ isBusy(`delete:projects:${project.id}`) ? "删除中…" : "删除" }}</button></div>
          </template>
        </article>
      </div>
    </section>

    <section v-else class="module-panel">
      <form class="card-form" @submit.prevent="createFriend">
        <div class="form-grid two">
          <div class="field"><label>站点名称</label><input v-model.trim="friendDraft.name" required maxlength="100" placeholder="朋友的博客名" /></div>
          <div class="field"><label>站点地址</label><input v-model.trim="friendDraft.url" type="url" required placeholder="https://..." /></div>
        </div>
        <div class="field"><label>一句话介绍</label><input v-model.trim="friendDraft.description" maxlength="300" placeholder="这个小站在记录什么？" /></div>
        <div class="image-row">
          <div class="field"><label>头像地址（可选）</label><input v-model.trim="friendDraft.avatar_url" type="url" placeholder="https://..." /></div>
          <ImageUploader compact label="上传头像" @uploaded="friendDraft.avatar_url = $event.url" />
        </div>
        <div class="form-grid options-grid friend-options">
          <label class="check-field"><input v-model="friendDraft.enabled" type="checkbox" /><span>在前台显示</span></label>
          <div class="field sort-field"><label>排序值</label><input v-model.number="friendDraft.sort_order" type="number" /></div>
          <button class="primary-button" :disabled="isBusy('create:friend-links')">{{ isBusy('create:friend-links') ? "添加中…" : "添加友链" }}</button>
        </div>
      </form>

      <div v-if="loading" class="admin-empty">正在读取友链…</div>
      <div v-else-if="!friendLinks.length" class="admin-empty">还没有友链，花园里正等着第一位朋友。</div>
      <div v-else class="friend-admin-list">
        <article v-for="friend in friendLinks" :key="friend.id" :class="{ editing: editingFriendId === friend.id, muted: !friend.enabled }">
          <form v-if="editingFriendId === friend.id" class="edit-form" @submit.prevent="saveFriend(friend)">
            <div class="form-grid two"><div class="field"><label>站点名称</label><input v-model.trim="friendEdit.name" required maxlength="100" /></div><div class="field"><label>站点地址</label><input v-model.trim="friendEdit.url" type="url" required /></div></div>
            <div class="field"><label>一句话介绍</label><input v-model.trim="friendEdit.description" maxlength="300" /></div>
            <div class="image-row"><div class="field"><label>头像地址</label><input v-model.trim="friendEdit.avatar_url" type="url" /></div><ImageUploader compact label="重新上传头像" @uploaded="friendEdit.avatar_url = $event.url" /></div>
            <div class="form-grid options-grid friend-options">
              <label class="check-field"><input v-model="friendEdit.enabled" type="checkbox" /><span>前台显示</span></label>
              <div class="field sort-field"><label>排序值</label><input v-model.number="friendEdit.sort_order" type="number" /></div>
              <div class="edit-actions"><button class="primary-button" :disabled="isBusy(`save:friend-links:${friend.id}`)">{{ isBusy(`save:friend-links:${friend.id}`) ? "保存中…" : "保存修改" }}</button><button type="button" class="secondary-button" @click="editingFriendId = null">取消</button></div>
            </div>
          </form>
          <template v-else>
            <div class="friend-avatar"><img v-if="friend.avatar_url" :src="friend.avatar_url" :alt="friend.name" /><span v-else>{{ initial(friend.name) }}</span></div>
            <div class="item-copy"><div class="item-meta"><span v-if="!friend.enabled">已隐藏</span><span>排序 {{ friend.sort_order }}</span></div><h3>{{ friend.name }}</h3><p>{{ friend.description || "暂无介绍" }}</p><a :href="friend.url" target="_blank" rel="noopener noreferrer">{{ friend.url }}</a></div>
            <div class="row-actions"><button @click="startFriendEdit(friend)">编辑</button><button class="remove" :disabled="isBusy(`delete:friend-links:${friend.id}`)" @click="remove('friend-links', friend)">{{ isBusy(`delete:friend-links:${friend.id}`) ? "删除中…" : "删除" }}</button></div>
          </template>
        </article>
      </div>
    </section>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { createAdminResource, deleteAdminResource, getAdminResource, updateAdminResource } from "../../api/content";
import AdminNotice from "./AdminNotice.vue";
import ImageUploader from "../ImageUploader.vue";

const active = ref("projects");
const projects = ref([]);
const friendLinks = ref([]);
const loading = ref(true);
const notice = ref("");
const success = ref(false);
const busyKeys = reactive(new Set());
const editingProjectId = ref(null);
const editingFriendId = ref(null);

const projectDefaults = { title: "", description: "", category: "其他", tags: "", github_url: "", demo_url: "", status: "active", featured: false, sort_order: 0, enabled: true };
const friendDefaults = { name: "", url: "", description: "", avatar_url: "", sort_order: 0, enabled: true };
const projectDraft = reactive({ ...projectDefaults });
const projectEdit = reactive({ ...projectDefaults });
const friendDraft = reactive({ ...friendDefaults });
const friendEdit = reactive({ ...friendDefaults });

function isBusy(key) { return busyKeys.has(key); }
function initial(name = "M") { return name.trim().slice(0, 1).toUpperCase(); }
function statusLabel(value) { return ({ building: "构建中", active: "持续维护", completed: "已完成", archived: "已归档" })[value] || value; }
function projectSymbol(category = "") {
  const value = category.toLowerCase();
  if (/爬虫|crawler|spider/.test(value)) return "⌁";
  if (/skill|工具|tool/.test(value)) return "✦";
  if (/app|应用|treeios/.test(value)) return "◉";
  return "↗";
}
function projectPayload(source) { return { ...source, tags: source.tags || null, github_url: source.github_url || null, demo_url: source.demo_url || null }; }
function friendPayload(source) { return { ...source, description: source.description || null, avatar_url: source.avatar_url || null }; }
async function runAction(key, action, fallback) {
  if (busyKeys.has(key)) return null;
  busyKeys.add(key); notice.value = "";
  try { return await action(); }
  catch (error) { success.value = false; notice.value = error.response?.data?.detail || fallback; return null; }
  finally { busyKeys.delete(key); }
}
async function createProject() {
  const item = await runAction("create:projects", async () => (await createAdminResource("projects", projectPayload(projectDraft))).data, "项目添加失败。");
  if (!item) return;
  projects.value.push(item); Object.assign(projectDraft, projectDefaults); success.value = true; notice.value = "项目已添加。";
}
function startProjectEdit(item) { editingProjectId.value = item.id; Object.assign(projectEdit, projectDefaults, item, { tags: item.tags || "", github_url: item.github_url || "", demo_url: item.demo_url || "" }); }
async function saveProject(item) {
  const saved = await runAction(`save:projects:${item.id}`, async () => (await updateAdminResource("projects", item.id, projectPayload(projectEdit))).data, "项目保存失败。");
  if (!saved) return;
  Object.assign(item, saved); editingProjectId.value = null; success.value = true; notice.value = "项目已保存。";
}
async function createFriend() {
  const item = await runAction("create:friend-links", async () => (await createAdminResource("friend-links", friendPayload(friendDraft))).data, "友链添加失败。");
  if (!item) return;
  friendLinks.value.push(item); Object.assign(friendDraft, friendDefaults); success.value = true; notice.value = "友链已添加。";
}
function startFriendEdit(item) { editingFriendId.value = item.id; Object.assign(friendEdit, friendDefaults, item, { description: item.description || "", avatar_url: item.avatar_url || "" }); }
async function saveFriend(item) {
  const saved = await runAction(`save:friend-links:${item.id}`, async () => (await updateAdminResource("friend-links", item.id, friendPayload(friendEdit))).data, "友链保存失败。");
  if (!saved) return;
  Object.assign(item, saved); editingFriendId.value = null; success.value = true; notice.value = "友链已保存。";
}
async function remove(resource, item) {
  if (!window.confirm(`确定删除“${item.title || item.name}”吗？`)) return;
  const removed = await runAction(`delete:${resource}:${item.id}`, async () => { await deleteAdminResource(resource, item.id); return true; }, "删除失败。");
  if (!removed) return;
  if (resource === "projects") { projects.value = projects.value.filter((entry) => entry.id !== item.id); editingProjectId.value = null; }
  else { friendLinks.value = friendLinks.value.filter((entry) => entry.id !== item.id); editingFriendId.value = null; }
  success.value = true; notice.value = "内容已删除。";
}

onMounted(async () => {
  const [projectResult, friendResult] = await Promise.allSettled([getAdminResource("projects"), getAdminResource("friend-links")]);
  if (projectResult.status === "fulfilled") projects.value = projectResult.value.data;
  else { success.value = false; notice.value = "项目列表加载失败。"; }
  if (friendResult.status === "fulfilled") friendLinks.value = friendResult.value.data;
  else { success.value = false; notice.value = notice.value || "友链列表加载失败。"; }
  loading.value = false;
});
</script>

<style scoped>
.admin-section-head { margin-bottom: 22px; display: flex; justify-content: space-between; align-items: end; gap: 24px; }.admin-section-head h2 { margin: 0; font: 500 32px Georgia, "Songti SC", serif; }.admin-section-head > p { max-width: 420px; margin: 0; color: var(--muted); font-size: 12px; line-height: 1.7; }
.subtabs { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 20px; }.subtabs button { padding: 9px 14px; border: 1px solid var(--line); border-radius: 999px; background: #fff; }.subtabs button.active { color: #fff; border-color: var(--rose-600); background: var(--rose-600); }.subtabs span { margin-left: 6px; opacity: .7; }
.module-panel { display: grid; gap: 20px; }.card-form, .edit-form { padding: 18px; display: grid; gap: 14px; border: 1px solid var(--line); border-radius: 15px; background: rgba(255,255,255,.72); }.form-grid { display: grid; gap: 12px; }.form-grid.two { grid-template-columns: repeat(2, 1fr); }.form-grid.three { grid-template-columns: repeat(3, 1fr); }.image-row { display: grid; grid-template-columns: 1fr 240px; gap: 10px; align-items: end; }
.options-grid { grid-template-columns: auto auto minmax(110px, 160px) 1fr; align-items: end; }.friend-options { grid-template-columns: auto minmax(110px, 160px) 1fr; }.options-grid .primary-button { justify-self: end; }.check-field { min-height: 42px; padding: 0 4px; display: flex; align-items: center; gap: 8px; color: var(--muted-strong); font-size: 13px; }.check-field input { width: 17px; height: 17px; accent-color: var(--rose-600); }.sort-field input { min-width: 0; }
.project-admin-list, .friend-admin-list { display: grid; gap: 10px; }.project-admin-list article, .friend-admin-list article { padding: 15px; display: grid; grid-template-columns: 54px 1fr auto; gap: 14px; align-items: center; border: 1px solid var(--line); border-radius: 15px; background: #fff; }.project-admin-list article.editing, .friend-admin-list article.editing { display: block; padding: 0; border: 0; }.project-admin-list article.muted, .friend-admin-list article.muted { background: #f7f5f2; opacity: .72; }
.project-mark, .friend-avatar { width: 54px; height: 54px; display: grid; place-items: center; border-radius: 15px; color: var(--rose-700); background: var(--rose-50); font: 25px Georgia, serif; }.friend-avatar { padding: 3px; border-radius: 50%; }.friend-avatar img, .friend-avatar span { width: 100%; height: 100%; display: grid; place-items: center; border-radius: 50%; object-fit: cover; background: var(--rose-50); }
.item-copy { min-width: 0; }.item-meta { display: flex; flex-wrap: wrap; gap: 6px; }.item-meta span { padding: 3px 7px; border-radius: 999px; color: var(--rose-700); background: var(--rose-50); font-size: 9px; }.item-copy h3 { margin: 7px 0 4px; font: 500 18px Georgia, "Songti SC", serif; }.item-copy p { max-width: 700px; margin: 0; overflow: hidden; color: var(--muted-strong); font-size: 12px; line-height: 1.6; text-overflow: ellipsis; white-space: nowrap; }.item-copy small { display: block; margin-top: 5px; color: var(--muted); }.item-copy a { display: block; max-width: 520px; margin-top: 6px; overflow: hidden; color: var(--rose-600); font-size: 11px; text-overflow: ellipsis; white-space: nowrap; }
.row-actions, .edit-actions { display: flex; align-items: center; gap: 7px; }.row-actions button { padding: 8px; border: 0; color: var(--rose-700); background: transparent; }.row-actions .remove { color: #a84d4d; }.admin-empty { padding: 38px; color: var(--muted); text-align: center; }
@media (max-width: 800px) { .admin-section-head { display: block; }.admin-section-head > p { margin-top: 8px; }.form-grid.two, .form-grid.three, .image-row, .options-grid, .friend-options { grid-template-columns: 1fr; }.options-grid .primary-button { justify-self: stretch; }.project-admin-list article, .friend-admin-list article { grid-template-columns: 48px 1fr; }.row-actions { grid-column: 2; }.item-copy p { white-space: normal; } }
</style>
