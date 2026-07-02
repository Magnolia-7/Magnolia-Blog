<template>
  <div class="login-page">
    <h1>后端登录</h1>

    <form class="login-form" @submit.prevent="handleLogin">
      <div class="form-item">
        <label>用户名</label>
        <input
          v-model="form.username"
          type="text"
          placeholder="请输入用户名"
        />
      </div>

      <div class="form-item">
        <label>密码</label>
        <input
          v-model="form.password"
          type="password"
          placeholder="请输入密码"
        />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? "登录中..." : "登录" }}
      </button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../api/auth";

const router = useRouter();

const form = reactive({
  username: "",
  password: "",
});

const loading = ref(false);
const error = ref("");
const success = ref("");

async function handleLogin() {
  error.value = "";
  success.value = "";

  if (!form.username.trim() || !form.password.trim()) {
    error.value = "请输入用户名和密码";
    return;
  }

  loading.value = true;

  try {
    const response = await login({
      username: form.username,
      password: form.password,
    });

    console.log("登录接口返回：", response.data);

    const token = response.data.access_token;

    if (!token) {
      error.value = "登录成功但没有拿到 token，请检查后端返回字段";
      return;
    }

    localStorage.setItem("access_token", token);

    console.log("保存后的 token：", localStorage.getItem("access_token"));

    success.value = "登录成功，正在进入后台...";

    setTimeout(() => {
      router.push("/admin");
    }, 500);
  } catch (err) {
    console.error("登录失败：", err);
    error.value = "登录失败，请检查用户名或密码";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-page {
  max-width: 420px;
  margin: 60px auto;
}

.login-form {
  display: grid;
  gap: 16px;
  margin-top: 24px;
}

.form-item {
  display: grid;
  gap: 8px;
}

.form-item input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

button {
  padding: 10px 14px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.error {
  color: #c0392b;
  margin-top: 16px;
}

.success {
  color: #27ae60;
  margin-top: 16px;
}
</style>