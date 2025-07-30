<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <NavBar v-if="isAuthenticated" />
    
    <!-- Container principal com altura fixa -->
    <main class="w-full" :class="isAuthenticated ? 'min-h-[calc(100vh-80px)]' : 'min-h-screen'">
      <div v-if="isAuthenticated" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <router-view />
      </div>
      <div v-else class="w-full h-full">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

body {
  font-family: system-ui, -apple-system, sans-serif;
}
</style>