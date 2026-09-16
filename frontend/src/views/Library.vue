<template>
  <div class="page-shell library-page">
    <header class="page-heading">
      <p class="eyebrow">My library</p><h1>我的图书馆</h1>
      <p>读过的文字、看过的银幕和留住的瞬间，都在这里找到自己的位置。</p>
    </header>
    <div class="pill-tabs">
      <button v-for="tab in tabs" :key="tab.value" :class="{ active: activeTab === tab.value }" @click="activeTab = tab.value">{{ tab.label }}</button>
    </div>
    <div v-if="loading" class="state-card">正在整理书架…</div>
    <div v-else-if="activeTab !== 'album' && !filteredItems.length" class="state-card">这一格还在等待第一份收藏。</div>
    <section v-else-if="activeTab !== 'album'" class="shelf-grid">
      <a v-for="item in filteredItems" :key="item.id" class="shelf-item" :href="item.external_url || undefined" :target="item.external_url ? '_blank' : undefined" rel="noopener noreferrer">
        <div class="book-cover"><img v-if="item.cover_image" :src="item.cover_image" :alt="item.title" loading="lazy" /><span v-else>{{ item.title.slice(0, 1) }}</span></div>
        <div><small>{{ statusLabel(item.status) }}<template v-if="item.rating"> · {{ item.rating }}/10</template></small><h2>{{ item.title }}</h2><p v-if="item.note">{{ item.note }}</p></div>
      </a>
    </section>
    <div v-else-if="!albums.length" class="state-card">相册正在等待第一张照片。</div>
    <section v-else class="album-grid">
      <article v-for="album in albums" :key="album.id" class="album-card surface">
        <div class="album-cover">
          <img v-if="album.cover_image || album.photos?.[0]?.thumbnail_url" :src="album.cover_image || album.photos[0].thumbnail_url" :alt="album.title" loading="lazy" />
          <span v-else>✦</span>
        </div>
        <div class="album-copy"><small>{{ album.photos?.length || 0 }} 张照片</small><h2>{{ album.title }}</h2><p>{{ album.description || "一些值得保存的瞬间。" }}</p></div>
        <div v-if="album.photos?.length" class="photo-strip">
          <a v-for="photo in visiblePhotos(album)" :key="photo.id" :href="photo.image_url" target="_blank" rel="noopener noreferrer"><img :src="photo.thumbnail_url || photo.image_url" :alt="photo.caption || album.title" loading="lazy" /></a>
          <button v-if="album.photos.length > 4" type="button" class="album-toggle" @click="toggleAlbum(album.id)">
            {{ isAlbumExpanded(album.id) ? "收起照片" : `查看全部 ${album.photos.length} 张` }}
          </button>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { getAlbums, getLibraryItems } from "../api/content";
const tabs = [{ value: "book", label: "读过的书" }, { value: "movie", label: "看过的电影" }, { value: "anime", label: "看过的动漫" }, { value: "album", label: "相册" }];
const activeTab = ref("book"); const items = ref([]); const albums = ref([]); const loading = ref(true);
const expandedAlbumIds = ref(new Set());
const filteredItems = computed(() => items.value.filter((item) => item.item_type === activeTab.value));
function statusLabel(value) { return ({ wishlist: "想看", reading: "进行中", completed: "已完成" })[value] || "已收藏"; }
function isAlbumExpanded(albumId) { return expandedAlbumIds.value.has(albumId); }
function visiblePhotos(album) { return isAlbumExpanded(album.id) ? album.photos : album.photos.slice(0, 4); }
function toggleAlbum(albumId) { const next = new Set(expandedAlbumIds.value); if (next.has(albumId)) next.delete(albumId); else next.add(albumId); expandedAlbumIds.value = next; }
onMounted(async () => { const [library, albumResult] = await Promise.allSettled([getLibraryItems(), getAlbums()]); if (library.status === "fulfilled") items.value = library.value.data; if (albumResult.status === "fulfilled") albums.value = albumResult.value.data; loading.value = false; });
</script>

<style scoped>
.shelf-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 28px 20px; }
.shelf-item { display: block; text-decoration: none; }
.book-cover { aspect-ratio: 3 / 4.25; display: grid; place-items: center; border-radius: 9px 18px 18px 9px; color: var(--rose-700); font: 70px Georgia, serif; background: linear-gradient(145deg, var(--rose-100), #e8e9df); box-shadow: -7px 10px 24px rgba(67,45,40,.12); overflow: hidden; transition: .25s ease; }
.book-cover img { width: 100%; height: 100%; object-fit: cover; }.shelf-item:hover .book-cover { transform: translateY(-5px) rotate(.5deg); box-shadow: -9px 16px 32px rgba(67,45,40,.17); }
.shelf-item small { display: block; margin-top: 17px; color: var(--rose-600); font-size: 11px; }.shelf-item h2 { margin: 6px 0; font: 500 20px/1.4 Georgia, "Songti SC", serif; }.shelf-item p { margin: 0; color: var(--muted); font-size: 13px; line-height: 1.7; }
.album-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }.album-card { padding: 18px; display: grid; grid-template-columns: 180px 1fr; gap: 24px; align-content: start; }.album-cover { aspect-ratio: 1; display: grid; place-items: center; border-radius: 18px; color: var(--rose-500); font-size: 44px; background: var(--rose-50); overflow: hidden; }.album-cover img { width: 100%; height: 100%; object-fit: cover; }.album-copy { align-self: center; }.album-copy small { color: var(--rose-600); }.album-copy h2 { margin: 8px 0; font: 500 26px Georgia, "Songti SC", serif; }.album-copy p { color: var(--muted); line-height: 1.7; }.photo-strip { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }.photo-strip a { aspect-ratio: 1.3; border-radius: 9px; overflow: hidden; }.photo-strip img { width: 100%; height: 100%; object-fit: cover; }.album-toggle { grid-column: 1 / -1; min-height: 38px; border: 1px solid var(--rose-200); border-radius: 999px; color: var(--rose-700); background: var(--rose-50); transition: .2s ease; }.album-toggle:hover { border-color: var(--rose-400); background: var(--rose-100); }
@media (max-width: 900px) { .shelf-grid { grid-template-columns: repeat(3, 1fr); }.album-grid { grid-template-columns: 1fr; } }
@media (max-width: 620px) { .shelf-grid { grid-template-columns: repeat(2, 1fr); gap: 24px 14px; }.album-card { grid-template-columns: 120px 1fr; gap: 16px; } }
</style>
