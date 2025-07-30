<template>
  <nav class="bg-white shadow-lg">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center py-4">
        <!-- Logo -->
        <div class="flex items-center space-x-4">
          <div class="text-xl font-bold text-primary-600 cursor-default">
            Jornada
          </div>
        </div>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center space-x-6">
          <router-link 
            to="/dashboard" 
            class="nav-link"
            :class="{ 'text-primary-600': $route.path === '/dashboard' }"
          >
            Dashboard
          </router-link>
          <router-link 
            to="/tasks" 
            class="nav-link"
            :class="{ 'text-primary-600': $route.path === '/tasks' }"
          >
            Tarefas
          </router-link>
          <router-link 
            to="/daily-summaries" 
            class="nav-link"
            :class="{ 'text-primary-600': $route.path === '/daily-summaries' }"
          >
            Resumos Diários
          </router-link>
          <router-link 
            to="/weekly-summaries" 
            class="nav-link"
            :class="{ 'text-primary-600': $route.path === '/weekly-summaries' }"
          >
            Resumos Semanais
          </router-link>
        </div>

        <!-- User Menu -->
        <div class="flex items-center space-x-4">
          <button
            @click="logout"
            class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-gray-300"
          >
            Sair
          </button>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden">
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="text-gray-600 hover:text-gray-900"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden py-4 border-t">
        <div class="flex flex-col space-y-3">
          <router-link to="/dashboard" class="nav-link-mobile">Dashboard</router-link>
          <router-link to="/tasks" class="nav-link-mobile">Tarefas</router-link>
          <router-link to="/daily-summaries" class="nav-link-mobile">Resumos Diários</router-link>
          <router-link to="/weekly-summaries" class="nav-link-mobile">Resumos Semanais</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  @apply text-gray-600 hover:text-primary-600 transition-colors font-medium;
}

.nav-link-mobile {
  @apply block px-3 py-2 text-gray-600 hover:text-primary-600 hover:bg-gray-50 rounded;
}
</style>