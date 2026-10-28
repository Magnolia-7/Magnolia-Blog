import { computed, reactive } from 'vue';
import { getSiteSettings, recordVisit } from '../api/activity';

const site = reactive({ avatar_url: '', hero_image_url: '' });
let pending;
export function useSite() {
  return {
    site,
    avatar: computed(() => site.avatar_url || '/images/sanji.jpg'),
    heroImage: computed(() => site.hero_image_url || '/images/manga-crew.jpg'),
  };
}
export function loadSite(force = false) {
  if (!pending || force) pending = getSiteSettings().then(({ data }) => Object.assign(site, data)).catch(() => { pending = null; });
  return pending;
}
export async function trackPage(path) {
  if (path.startsWith('/admin') || path.startsWith('/login')) return;
  try {
    let visitor = localStorage.getItem('magnolia_visitor');
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(visitor || '')) {
      visitor = crypto.randomUUID();
      localStorage.setItem('magnolia_visitor', visitor);
    }
    await recordVisit({ visitor_id: visitor, event_id: crypto.randomUUID(), path });
    window.dispatchEvent(new Event('site-stats-updated'));
  } catch { /* A blocked visitor counter must not interrupt navigation. */ }
}
