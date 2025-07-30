<template>
  <div class="w-full space-y-8">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow p-6">
      <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-gray-600 mt-2">Acompanhe seu progresso diário e semanal</p>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Tarefas Realizadas</p>
            <p class="text-2xl font-bold text-gray-900">{{ todayTasks.length }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Resumos Diários</p>
            <p class="text-2xl font-bold text-gray-900">{{ currentWeekSummaries.length }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Resumos Semanais</p>
            <p class="text-2xl font-bold text-gray-900">{{ weeklySummaries.length }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Today's Tasks -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">Tarefas Recentes</h2>
          <router-link 
            to="/tasks" 
            class="text-primary-600 hover:text-primary-500 text-sm font-medium"
          >
            Ver todas
          </router-link>
        </div>
      </div>
      <div class="p-6">
        <div v-if="todayTasks.length === 0" class="text-center py-8">
          <p class="text-gray-500">Nenhuma tarefa para hoje</p>
          <router-link 
            to="/tasks" 
            class="mt-2 inline-block text-primary-600 hover:text-primary-500"
          >
            Adicionar tarefa
          </router-link>
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="task in todayTasks.slice(0, 5)" 
            :key="task.id"
            class="flex items-center p-3 bg-gray-50 rounded-lg"
          >
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">{{ task.title }}</p>
              <p class="text-xs text-gray-500">{{ formatDateForDisplay(task.date) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded-lg shadow">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">Resumos Recentes</h2>
            <router-link 
              to="/daily-summaries" 
              class="text-primary-600 hover:text-primary-500 text-sm font-medium"
            >
              Ver todos
            </router-link>
          </div>
        </div>
        <div class="p-6">
          <div v-if="recentDailySummaries.length === 0" class="text-center py-8">
            <p class="text-gray-500">Nenhum resumo ainda</p>
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="summary in recentDailySummaries.slice(0, 3)" 
              :key="summary.id"
              class="border-l-4 border-blue-400 pl-4"
            >
              <h3 class="text-sm font-medium text-gray-900">{{ summary.title }}</h3>
              <p class="text-xs text-gray-500">{{ formatDateForDisplay(summary.date) }}</p>
              <p class="text-sm text-gray-600 mt-1 line-clamp-2">
                {{ summary.content.substring(0, 100) }}...
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">Resumos Semanais</h2>
            <router-link 
              to="/weekly-summaries" 
              class="text-primary-600 hover:text-primary-500 text-sm font-medium"
            >
              Ver todos
            </router-link>
          </div>
        </div>
        <div class="p-6">
          <div v-if="recentWeeklySummaries.length === 0" class="text-center py-8">
            <p class="text-gray-500">Nenhum resumo semanal ainda</p>
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="summary in recentWeeklySummaries.slice(0, 2)" 
              :key="summary.id"
              class="border-l-4 border-purple-400 pl-4"
            >
              <h3 class="text-sm font-medium text-gray-900">{{ summary.title }}</h3>
              <p class="text-xs text-gray-500">
                {{ formatDateForDisplay(summary.week_start) }} - {{ formatDateForDisplay(summary.week_end) }}
              </p>
              <p class="text-sm text-gray-600 mt-1 line-clamp-2">
                {{ summary.content.substring(0, 100) }}...
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { tasksAPI, dailySummariesAPI, weeklySummariesAPI } from '@/services/api'
import { formatDateForDisplay } from '@/utils/dateUtils'

const todayTasks = ref([])
const currentWeekSummaries = ref([])
const weeklySummaries = ref([])
const recentDailySummaries = ref([])
const recentWeeklySummaries = ref([])
const isLoading = ref(true)

const loadDashboardData = async () => {
  try {
    const today = new Date().toISOString().split('T')[0]
    
    const tasksResponse = await tasksAPI.list({ date: today })
    todayTasks.value = tasksResponse.data.results || tasksResponse.data
    
    const currentWeekResponse = await dailySummariesAPI.currentWeek()
    currentWeekSummaries.value = currentWeekResponse.data
    
    const dailySummariesResponse = await dailySummariesAPI.list({ page_size: 5 })
    recentDailySummaries.value = dailySummariesResponse.data.results || dailySummariesResponse.data
    
    const weeklySummariesResponse = await weeklySummariesAPI.list({ page_size: 3 })
    weeklySummaries.value = weeklySummariesResponse.data.results || weeklySummariesResponse.data
    recentWeeklySummaries.value = weeklySummaries.value
    
  } catch (error) {
    console.error('Erro ao carregar dados do dashboard:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2; /* Propriedade padrão para compatibilidade */
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>