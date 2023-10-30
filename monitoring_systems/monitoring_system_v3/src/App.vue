<template>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="true">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <div v-if="logged_in">
    <div class="logo">
      <div class="logo-img">
        <img src="/logo.svg">
      </div>
    </div>
    <div class="outside-page">
      <div class="page">
        <div class="menu-bar">
          <div class="menu main" @click="setIsmain">
            <span class="material-icons">home</span>
            <div>메인</div>
          </div>
          <div class="menu statistics" @click="unsetIsmain">
            <span class="material-icons">bar_chart</span>
            <div>통계</div>
          </div>
        </div>
        <HomePage v-if="ismain" />
        <!-- <StatisticsPage v-else /> -->
        <GrafanaComp v-else />
      </div>
    </div>
  </div>
  <div v-else class="login-page">
    <div class="logo">
      <div class="logo-img">
        <img src="/logo.svg">
      </div>
    </div>
    <div class="loginbox">
      <div class="login-label">아이디</div>
      <input class="login-input" type="text" v-model="id">
    </div>
    <div class="loginbox">
      <div class="login-label">비밀번호</div>
      <input class="login-input" type="text" v-model="pw" @keyup.enter="login">
    </div>
    <div style="display: flex;">
      <button class="login-button" @click="login">로그인</button>
    </div>
  </div>
</template>

<script setup>
import HomePage from './components/HomePage.vue'
import GrafanaComp from './components/GrafanaComp.vue';
import { ref } from 'vue'

const ismain = ref(true)
const logged_in = ref(true)

const id = ref("")
const pw = ref("")

function setIsmain() {
  ismain.value = true
}
function unsetIsmain() {
  ismain.value = false
}
function login() {
  if (id.value == "admin" && pw.value == "1234") {
    logged_in.value = true
  }
  else {
    alert("로그인할 수 없습니다.")
  }
}
</script>

<style scoped>
/* @import "./assets/style.css"; */
</style>
