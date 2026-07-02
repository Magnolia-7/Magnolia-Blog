<template>
  <div class="admin-page">
    <div class="header">
      <h1>后台管理</h1>
      <button @click="logout">退出登录</button>
    </div>

    <p v-if="loading">加载中...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="!token" class="notice">
      你还没有登录，请先前往
      <RouterLink to="/login">登录页</RouterLink>
    </div>

    <div v-if="token">
      <section class="about-admin-box">
        <h2>关于页编辑</h2>

        <p v-if="aboutLoading">关于页信息加载中...</p>
        <p v-if="aboutError" class="error">{{ aboutError }}</p>
        <p v-if="aboutMessage" class="success">{{ aboutMessage }}</p>

        <form class="about-form" @submit.prevent="handleSaveAbout">
          <div class="form-item">
            <label>头像地址</label>
            <input
              v-model="aboutForm.avatar"
              type="text"
              placeholder="请输入头像图片 URL"
            />
          </div>

          <div class="form-row">
            <div class="form-item">
              <label>昵称</label>
              <input
                v-model="aboutForm.nickname"
                type="text"
                placeholder="请输入昵称"
              />
            </div>

            <div class="form-item">
              <label>个性签名</label>
              <input
                v-model="aboutForm.signature"
                type="text"
                placeholder="请输入个性签名"
              />
            </div>
          </div>

          <div class="form-item">
            <label>个人说明</label>
            <textarea
              v-model="aboutForm.bio"
              rows="4"
              placeholder="请输入个人说明"
            ></textarea>
          </div>

          <div class="form-item">
            <label>兴趣爱好</label>
            <textarea
              v-model="aboutForm.interests"
              rows="3"
              placeholder="例如：编程、阅读、电影、动漫、写作"
            ></textarea>
          </div>

          <div class="form-item">
            <label>能力</label>
            <textarea
              v-model="aboutForm.skills"
              rows="3"
              placeholder="例如：Python, FastAPI, Vue, JavaScript, MySQL"
            ></textarea>
          </div>

          <div class="form-item">
            <label>联系方式</label>
            <textarea
              v-model="aboutForm.contacts"
              rows="3"
              placeholder="例如：email: xxx@example.com"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-item">
              <label>当前心情</label>
              <input
                v-model="aboutForm.mood"
                type="text"
                placeholder="例如：认真开发博客中"
              />
            </div>

            <div class="form-item">
              <label>短期目标</label>
              <input
                v-model="aboutForm.short_goal"
                type="text"
                placeholder="例如：完成个人博客 MVP"
              />
            </div>
          </div>

          <div class="form-item">
            <label>长期目标</label>
            <input
              v-model="aboutForm.long_goal"
              type="text"
              placeholder="例如：持续维护个人空间"
            />
          </div>

          <div class="form-item">
            <label>社交链接 JSON</label>
            <textarea
              v-model="aboutForm.social_links"
              rows="4"
              placeholder='例如：[{"name":"GitHub","url":"https://github.com/yourname"}]'
            ></textarea>
          </div>

          <div class="form-item">
            <label>技术栈 JSON</label>
            <textarea
              v-model="aboutForm.tech_stack"
              rows="4"
              placeholder='例如：{"FastAPI":"https://fastapi.tiangolo.com/","Vue":"https://vuejs.org/"}'
            ></textarea>
          </div>

          <button type="submit" :disabled="aboutSaving">
            {{ aboutSaving ? "保存中..." : "保存关于页" }}
          </button>
        </form>
      </section>
      <section class = "create-box" ref="postFormRef">
        <h2>{{ editingId ? '编辑文章' : '新增文章' }}</h2>

        <form class="post-form" @submit.prevent="handleSubmitPost">
          <div class="form-item">
            <label>标题：</label>
            <input v-model="form.title" type="text" placeholder="请输入文章标题" />
          </div>

          <div class="form-item">
            <label>摘要：</label>
            <input v-model="form.summary" type="text" placeholder="请输入文章摘要（可选）" />
          </div>

          <div class="form-item">
            <label>封面图地址：</label>
            <input v-model="form.cover_image" type="text" placeholder="请输入封面图片URL（可选）" />
          </div>

          <div class="form-row">
            <div class="form-item">
              <label>分类</label>
              <select v-model="form.category">
                <option value="life">生活记录</option>
                <option value="study">学习笔记</option>
              </select>
            </div>
            
            <div class="form-item">
              <label>状态</label>
              <select v-model="form.status">
                <option value="draft">草稿</option>
                <option value="published">已发布</option>
              </select>
            </div>
          </div>

          <div class="form-item markdown-field">
            <label>正文（Markdown）</label>
            <p class="markdown-help">
              支持标题、列表、引用、代码块、链接和图片 URL，例如：![说明](https://example.com/a.jpg)
            </p>

            <div class="markdown-editor">
              <textarea
                v-model="form.content"
                class="markdown-input"
                rows="14"
                placeholder="请输入 Markdown 正文"
              ></textarea>

              <div class="markdown-preview-panel">
                <div class="preview-title">实时预览</div>
                <div
                  v-if="form.content.trim()"
                  class="markdown-preview"
                  v-html="markdownPreview"
                ></div>
                <div v-else class="empty-preview">
                  这里会显示 Markdown 预览
                </div>
              </div>
            </div>
          </div>

          <button type="submit" :disabled="creating || updating">
            {{ editingId ? (updating ? "保存中..." : "保存修改" ) : (creating ? "发布中..." : "新增文章") }}
          </button>
          <button
            v-if="editingId"
            type="button"
            @click="cancelEdit"
            :disabled="updating"
          >取消编辑
        </button>
        </form>
      </section>
      <h2>文章列表</h2>

      <div v-if="posts.length === 0 && !loading">
        暂无文章
      </div>

      <div class="post-list">
        <div v-for="post in posts" :key="post.id" class="post-card">
          <div>
            <h3>{{ post.title }}</h3>
            <p>{{ post.summary }}</p>
            <p class="meta">
              ID：{{ post.id }} ｜ 分类：{{ formatCategory(post.category) }} ｜ 状态：{{ formatStatus(post.status) }}
            </p>
          </div>

          <div class="actions">
            <button @click="startEdit(post)">编辑</button>
            <button @click="handleDelete(post.id)">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { 
  deleteAdminPost, 
  getAdminPosts, 
  createAdminPost,
  updateAdminPost,
} from "../api/posts";
import { getAdminAbout, updateAdminAbout } from "../api/about";
import { renderMarkdown } from "../utils/markdown";


const router = useRouter();

const postFormRef = ref(null);
const token = ref(localStorage.getItem("access_token"));
const posts = ref([]);
const form = ref({
  title: "",
  summary: "",
  content: "",
  cover_image: "",
  category: "life",
  status: "draft",
});
const aboutForm = ref({
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

const aboutLoading = ref(false);
const aboutSaving = ref(false);
const aboutMessage = ref("");
const aboutError = ref("");

const editingId = ref(null);
const updating = ref(false);

const creating = ref(false);
const loading = ref(false);
const error = ref("");
const markdownPreview = computed(() => renderMarkdown(form.value.content));

async function loadAdminPosts() {
  if (!token.value) {
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const response = await getAdminPosts();
    posts.value = response.data;
  } catch (err) {
    console.error(err);

    if (err.response?.status === 401 || err.response?.status === 403) {
      error.value = "登录已过期，请重新登录。";
      localStorage.removeItem("access_token");
      token.value = null;
    } else {
      error.value = "后台文章加载失败。";
    }
  } finally {
    loading.value = false;
  }
}

async function handleSubmitPost(){
  error.value = "";
  
  if (!form.value.title.trim()){
    error.value = "标题不能为空。";
    return;
  }

  if(!form.value.content.trim()){
    error.value = "内容不能为空。";
    return;
  }

  const payload = {
    title: form.value.title,
    summary: form.value.summary || "",
    content: form.value.content,
    cover_image: form.value.cover_image || "",
    category: form.value.category,
    status: form.value.status,
  };

  try{
    if (editingId.value){
      updating.value = true;
      
      const response = await updateAdminPost(editingId.value, payload);

      posts.value = posts.value.map((post) =>
        post.id === editingId.value ? response.data : post
      );

      editingId.value = null;
    }else{
      creating.value = true;

      const response = await createAdminPost(payload);

      posts.value.unshift(response.data);
    }
    form.value = {
      title: "",
      summary: "",
      content: "",
      cover_image: "",
      category: "life",
      status: "draft",
    };
  }catch(err){
    console.error(err);
    error.value = editingId.value
    ? "编辑文章失败，请检查表单内容或登录状态"
    : "新增文章失败，请检查表单内容或登录状态";
  }finally{
    updating.value = false;
    creating.value = false;
  }
}

async function loadAdminAbout() {
  if (!token.value) {
    return;
  }

  aboutLoading.value = true;
  aboutError.value = "";
  aboutMessage.value = "";

  try {
    const response = await getAdminAbout();

    if (response.data) {
      aboutForm.value = {
        avatar: response.data.avatar || "",
        nickname: response.data.nickname || "",
        signature: response.data.signature || "",
        bio: response.data.bio || "",
        interests: response.data.interests || "",
        skills: response.data.skills || "",
        contacts: response.data.contacts || "",
        mood: response.data.mood || "",
        short_goal: response.data.short_goal || "",
        long_goal: response.data.long_goal || "",
        social_links: response.data.social_links || "",
        tech_stack: response.data.tech_stack || "",
      };
    }
  } catch (err) {
    console.error(err);

    if (err.response?.status === 401 || err.response?.status === 403) {
      aboutError.value = "登录已过期，请重新登录。";
      localStorage.removeItem("access_token");
      token.value = null;
    } else {
      aboutError.value = "关于页信息加载失败。";
    }
  } finally {
    aboutLoading.value = false;
  }
}

async function handleSaveAbout() {
  aboutSaving.value = true;
  aboutError.value = "";
  aboutMessage.value = "";

  try {
    const payload = {
      avatar: aboutForm.value.avatar || null,
      nickname: aboutForm.value.nickname || null,
      signature: aboutForm.value.signature || null,
      bio: aboutForm.value.bio || null,
      interests: aboutForm.value.interests || null,
      skills: aboutForm.value.skills || null,
      contacts: aboutForm.value.contacts || null,
      mood: aboutForm.value.mood || null,
      short_goal: aboutForm.value.short_goal || null,
      long_goal: aboutForm.value.long_goal || null,
      social_links: aboutForm.value.social_links || null,
      tech_stack: aboutForm.value.tech_stack || null,
    };

    const response = await updateAdminAbout(payload);

    aboutForm.value = {
      avatar: response.data.avatar || "",
      nickname: response.data.nickname || "",
      signature: response.data.signature || "",
      bio: response.data.bio || "",
      interests: response.data.interests || "",
      skills: response.data.skills || "",
      contacts: response.data.contacts || "",
      mood: response.data.mood || "",
      short_goal: response.data.short_goal || "",
      long_goal: response.data.long_goal || "",
      social_links: response.data.social_links || "",
      tech_stack: response.data.tech_stack || "",
    };

    aboutMessage.value = "关于页保存成功";
  } catch (err) {
    console.error(err);
    aboutError.value = "关于页保存失败，请检查登录状态或表单内容。";
  } finally {
    aboutSaving.value = false;
  }
}

async function handleDelete(id) {
  const confirmed = window.confirm("确定要删除这篇文章吗？");

  if (!confirmed) return;

  try {
    await deleteAdminPost(id);
    posts.value = posts.value.filter((post) => post.id !== id);
  } catch (err) {
    console.error(err);
    error.value = "删除失败，请稍后重试。";
  }
}

function startEdit(post){
  editingId.value = post.id;

  form.value = {
    title:post.title || "",
    summary: post.summary || "",
    content: post.content || "",
    cover_image: post.cover_image || "",
    category: post.category || "life",
    status: post.status || "draft",
  }

  setTimeout(() => {
    postFormRef.value?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }, 0);
}

function cancelEdit(){
  editingId.value = null;

  form.value = {
    title: "",
    summary: "",
    content: "",
    cover_image: "",
    category: "life",
    status: "draft",
  };
}
function logout() {
  localStorage.removeItem("access_token");
  token.value = null;
  router.push("/login");
}

function formatCategory(category) {
  if (category === "life") return "生活记录";
  if (category === "study") return "学习笔记";
  return category;
}

function formatStatus(status) {
  if (status === "draft") return "草稿";
  if (status === "published") return "已发布";
  return status;
}

onMounted(() => {
  loadAdminPosts();
  loadAdminAbout();
});
</script>

<style scoped>
.admin-page {
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.notice {
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #fafafa;
}

.post-list {
  display: grid;
  gap: 16px;
  margin-top: 20px;
}

.post-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 10px;
}

.post-card h3 {
  margin: 0 0 8px;
}

.meta {
  color: #777;
  font-size: 14px;
}

.actions {
  display: flex;
  gap: 8px;
}

button {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background: #f5f5f5;
}

.error {
  color: #c0392b;
}

.success {
  color: #27ae60;
}

.create-box {
  margin: 24px 0;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 12px;
  background: #fafafa;
}

.post-form {
  display: grid;
  gap: 16px;
}

.form-item {
  display: grid;
  gap: 8px;
}

.form-item input,
.form-item select,
.form-item textarea {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.about-admin-box {
  margin: 24px 0;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 12px;
  background: #fafafa;
}

.about-form {
  display: grid;
  gap: 16px;
}

.markdown-field {
  gap: 10px;
}

.markdown-help {
  margin: 0;
  color: #777;
  font-size: 13px;
  line-height: 1.6;
}

.markdown-editor {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 16px;
}

.markdown-input {
  min-height: 360px;
  resize: vertical;
  line-height: 1.7;
}

.markdown-preview-panel {
  min-height: 360px;
  overflow: auto;
  border: 1px solid #eee;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.72);
}

.preview-title {
  position: sticky;
  top: 0;
  padding: 10px 14px;
  border-bottom: 1px solid #eee;
  color: #777;
  font-size: 13px;
  background: rgba(250, 250, 250, 0.94);
}

.markdown-preview,
.empty-preview {
  padding: 16px;
}

.empty-preview {
  color: #999;
}

.markdown-preview :deep(h1),
.markdown-preview :deep(h2),
.markdown-preview :deep(h3) {
  margin: 1.2em 0 0.55em;
  color: #202020;
  line-height: 1.3;
}

.markdown-preview :deep(h1:first-child),
.markdown-preview :deep(h2:first-child),
.markdown-preview :deep(h3:first-child),
.markdown-preview :deep(p:first-child) {
  margin-top: 0;
}

.markdown-preview :deep(p),
.markdown-preview :deep(li) {
  color: #444;
  line-height: 1.8;
}

.markdown-preview :deep(blockquote) {
  margin: 16px 0;
  padding: 10px 14px;
  border-left: 3px solid #b87b8b;
  color: #6f6065;
  background: #fff7fa;
}

.markdown-preview :deep(pre) {
  overflow: auto;
  padding: 14px;
  border-radius: 8px;
  color: #f8f8f2;
  background: #2f2a2c;
}

.markdown-preview :deep(code) {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}

.markdown-preview :deep(:not(pre) > code) {
  padding: 2px 5px;
  border-radius: 5px;
  color: #9f6473;
  background: #fff1f5;
}

.markdown-preview :deep(a) {
  color: #9f6473;
}

.markdown-preview :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

@media (max-width: 860px) {
  .markdown-editor {
    grid-template-columns: 1fr;
  }
}
</style>
