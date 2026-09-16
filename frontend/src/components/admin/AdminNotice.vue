<template>
  <div v-if="message" :class="['admin-notice', success ? 'success' : 'error']" :role="success ? 'status' : 'alert'">
    <span>{{ message }}</span>
    <button type="button" aria-label="关闭提示" @click="$emit('close')">×</button>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, default: "" },
  success: Boolean,
});
defineEmits(["close"]);
</script>

<style scoped>
.admin-notice { margin: 0 0 16px; padding: 11px 13px; display: flex; align-items: center; justify-content: space-between; gap: 12px; border: 1px solid; border-radius: 12px; font-size: 13px; }
.admin-notice.success { color: #55745c; border-color: rgba(85,116,92,.2); background: rgba(233,243,235,.7); }
.admin-notice.error { color: #a84d4d; border-color: rgba(168,77,77,.2); background: rgba(255,241,241,.82); }
.admin-notice button { width: 26px; height: 26px; padding: 0; flex: 0 0 auto; border: 0; border-radius: 50%; color: currentColor; background: transparent; font-size: 18px; }
.admin-notice button:hover { background: rgba(0,0,0,.05); }
</style>
