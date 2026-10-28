export const categoryLabel = (value) => ({ life: '记录贴', study: '技术贴', thought: '说说贴' })[value] || '记录贴';
export const formatMinutes = (value = 0) => `${Math.floor(value / 60)}h ${String(value % 60).padStart(2, '0')}m`;
export function todayISO() {
  const parts = new Intl.DateTimeFormat('en', { timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(new Date());
  const part = (key) => parts.find((item) => item.type === key).value;
  return `${part('year')}-${part('month')}-${part('day')}`;
}
export function formatDate(value) {
  return value ? String(value).slice(0, 10).replaceAll('-', '.') : '';
}
export function tags(value) {
  return (value || '').split(/[,，]/).map((tag) => tag.trim()).filter(Boolean);
}
export function apiError(error, fallback = '操作失败，请稍后重试。') {
  const detail = error.response?.data?.detail;
  return typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.map((item) => item.msg).join('；') : fallback;
}
