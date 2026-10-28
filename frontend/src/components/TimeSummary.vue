<template>
  <section class="time-summary surface" aria-label="投入时间统计">
    <header class="section-row"><h2 class="comic">TIME LOG</h2><div class="pill-tabs" aria-label="统计范围"><button v-for="item in periods" :key="item.value" type="button" :class="{ active: period === item.value }" :aria-pressed="period === item.value" @click="period = item.value">{{ item.label }}</button></div></header>
    <div v-if="loading" class="state-card" role="status">加载中…</div>
    <div v-else-if="error" class="state-card error" role="alert">{{ error }} <button type="button" class="text-button" @click="load">重试</button></div>
    <template v-else>
      <div class="time-total" aria-live="polite"><strong class="comic">{{ formatMinutes(summary.total_minutes) }}</strong><span>{{ range }}</span></div>
      <table class="time-table"><thead><tr><th scope="col">投入项目</th><th scope="col">时长</th><th scope="col">天数</th></tr></thead><tbody><tr v-for="row in summary.categories" :key="row.category"><td>{{ row.category }}</td><td>{{ formatMinutes(row.minutes) }}</td><td>{{ row.days }} 天</td></tr><tr v-if="!summary.categories.length"><td colspan="3" class="empty-cell">暂无记录</td></tr></tbody><tfoot><tr><td>总计</td><td>{{ formatMinutes(summary.total_minutes) }}</td><td>{{ summary.tracked_days }} 天</td></tr></tfoot></table>
      <div class="ledger-note"><span>每日记录自动汇总</span><RouterLink class="text-link" to="/records?view=calendar">查看每日记录 ↗</RouterLink></div>
    </template>
  </section>
</template>
<script setup>
import { computed, ref, watch } from 'vue';
import { getTimeSummary } from '../api/activity';
import { formatMinutes, formatDate } from '../utils/format';
const periods = [{ value: 'week', label: '本周' }, { value: 'month', label: '本月' }, { value: 'all', label: '累计' }];
const period = ref('month'), summary = ref({ categories: [], total_minutes: 0, tracked_days: 0 }), loading = ref(true), error = ref('');
let loadId = 0;
const range = computed(() => summary.value.start_date ? `${formatDate(summary.value.start_date)} — ${formatDate(summary.value.end_date)}` : '');
async function load() {
  const id = ++loadId;
  loading.value = true; error.value = '';
  try { const { data } = await getTimeSummary(period.value); if (id === loadId) summary.value = data; }
  catch { if (id === loadId) error.value = '投入时间加载失败。'; }
  finally { if (id === loadId) loading.value = false; }
}
watch(period, load, { immediate: true });
</script>
