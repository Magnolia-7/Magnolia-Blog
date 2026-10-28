<template>
  <section :class="['time-calendar', 'surface', { 'calendar-standalone': standalone }]" aria-label="投入时间日历">
    <header class="calendar-title"><h2 class="comic">CALENDAR</h2><div class="calendar-controls"><button type="button" aria-label="上个月" @click="changeMonth(-1)">‹</button><span>{{ month.replace('-', '.') }}</span><button type="button" aria-label="下个月" :disabled="month >= today.slice(0, 7)" @click="changeMonth(1)">›</button></div></header>
    <div class="weekdays" aria-hidden="true"><span v-for="day in weekdays" :key="day">{{ day }}</span></div>
    <div class="calendar-days" role="group" aria-label="选择日期" :aria-busy="loading"><span v-for="blank in offset" :key="`blank-${blank}`" class="day-blank"></span><button v-for="day in days" :key="day.date" type="button" :data-intensity="day.intensity" :aria-pressed="selectedDate === day.date" :aria-label="`${day.date}，${formatMinutes(day.total)}`" :disabled="day.date > today || loading" @click="selectedDate = day.date">{{ day.day }}</button></div>
    <div class="calendar-legend"><span>投入时长 · 少</span><i v-for="level in 4" :key="level" :data-intensity="level - 1"></i><span>多</span></div>
    <div v-if="loading" class="calendar-detail" role="status">加载中…</div>
    <div v-else-if="error" class="calendar-detail error-text" role="alert">{{ error }} <button class="text-button" type="button" @click="load">重试</button></div>
    <div v-else class="calendar-detail" aria-live="polite"><div class="day-total"><h3>{{ selectedDate.replaceAll('-', '.') }}</h3><strong class="comic">{{ formatMinutes(selected.total_minutes) }}</strong></div><div v-for="entry in selected.entries" :key="entry.category" class="day-entry"><span>{{ entry.category }}</span><span>{{ formatMinutes(entry.minutes) }}</span></div><p v-if="!selected.entries.length" class="muted">暂无记录</p></div>
  </section>
</template>
<script setup>
import { computed, ref, watch } from 'vue';
import { getTimeLogs } from '../api/activity';
import { todayISO, formatMinutes } from '../utils/format';
defineProps({ standalone: Boolean });
const today = todayISO(), month = ref(today.slice(0, 7)), selectedDate = ref(today), logs = ref([]), loading = ref(false), error = ref('');
const weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];
let loadId = 0;
const logMap = computed(() => new Map(logs.value.map((log) => [log.date, log])));
const offset = computed(() => (new Date(`${month.value}-01T12:00:00Z`).getUTCDay() + 6) % 7);
const days = computed(() => {
  const [y, m] = month.value.split('-').map(Number);
  return Array.from({ length: new Date(Date.UTC(y, m, 0)).getUTCDate() }, (_, index) => {
    const date = `${month.value}-${String(index + 1).padStart(2, '0')}`, total = logMap.value.get(date)?.total_minutes || 0;
    return { day: index + 1, date, total, intensity: !total ? 0 : total < 180 ? 1 : total < 270 ? 2 : 3 };
  });
});
const selected = computed(() => logMap.value.get(selectedDate.value) || { entries: [], total_minutes: 0 });
function changeMonth(step) {
  const [y, m] = month.value.split('-').map(Number), date = new Date(Date.UTC(y, m - 1 + step, 1));
  month.value = `${date.getUTCFullYear()}-${String(date.getUTCMonth() + 1).padStart(2, '0')}`;
  selectedDate.value = month.value === today.slice(0, 7) ? today : `${month.value}-01`;
}
async function load() {
  const id = ++loadId;
  loading.value = true; error.value = ''; logs.value = [];
  try { const { data } = await getTimeLogs(month.value); if (id === loadId) logs.value = data; }
  catch { if (id === loadId) error.value = '日历加载失败。'; }
  finally { if (id === loadId) loading.value = false; }
}
watch(month, load, { immediate: true });
</script>
