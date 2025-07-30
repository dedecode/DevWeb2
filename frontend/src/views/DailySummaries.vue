<template>
  <div class="w-full space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Resumos Diários</h1>
          <p class="text-gray-600 mt-2">Documente seu progresso de hoje</p>
        </div>
        <button
          @click="checkAndCreateSummary"
          class="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors shadow-sm"
        >
          {{ todaySummary ? 'Editar Resumo de Hoje' : 'Novo Resumo de Hoje' }}
        </button>
      </div>
    </div>

    <!-- Resumo de Hoje -->
    <div v-if="todaySummary" class="bg-white rounded-lg shadow">
      <div class="p-6">
        <div class="border-l-4 border-blue-400 pl-4 mb-4">
          <h3 class="font-semibold text-gray-900">Resumo de Hoje</h3>
          <p class="text-sm text-gray-500">{{ formatDateForDisplay(todaySummary.date) }}</p>
        </div>
        <h4 class="font-medium text-gray-900 mb-2">{{ todaySummary.title }}</h4>
        <div class="text-gray-700 whitespace-pre-wrap">{{ todaySummary.content }}</div>
        <div class="flex items-center space-x-2 mt-4">
          <button
            @click="editSummary(todaySummary)"
            class="px-3 py-1 text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            Editar
          </button>
          <button
            @click="deleteSummary(todaySummary.id)"
            class="px-3 py-1 text-sm text-red-600 hover:text-red-700 font-medium"
          >
            Excluir
          </button>
        </div>
      </div>
    </div>

    <!-- Resumos Anteriores -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Resumos Anteriores</h3>
        
        <div v-if="isLoading" class="text-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
        </div>
        
        <div v-else-if="pastSummaries.length === 0" class="text-center py-8">
          <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="text-gray-500">Nenhum resumo anterior encontrado</p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="summary in pastSummaries"
            :key="summary.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h4 class="font-medium text-gray-900 mb-2">{{ summary.title }}</h4>
                <p class="text-sm text-gray-500 mb-3">{{ formatDateForDisplay(summary.date) }}</p>
                <div class="text-gray-700 whitespace-pre-wrap line-clamp-3">{{ summary.content }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal || editingSummary"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
        <h2 class="text-xl font-bold text-gray-900 mb-4">
          {{ editingSummary ? 'Editar Resumo de Hoje' : 'Resumo de Hoje' }}
        </h2>
        
        <form @submit.prevent="saveSummary" class="space-y-4">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700 mb-1">
              Título
            </label>
            <input
              id="title"
              v-model="summaryForm.title"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 bg-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Digite o título do resumo"
            />
          </div>

          <div class="bg-blue-50 p-3 rounded-lg">
            <p class="text-sm text-blue-700">
              📅 Este resumo será criado para hoje ({{ formatDateForDisplay(new Date().toISOString().split('T')[0]) }})
            </p>
          </div>

          <div>
            <label for="content" class="block text-sm font-medium text-gray-700 mb-1">
              Conteúdo
            </label>
            <textarea
              id="content"
              v-model="summaryForm.content"
              rows="8"
              class="w-full px-3 py-2 border border-gray-300 bg-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Descreva seu dia, principais realizações, aprendizados..."
            ></textarea>
          </div>

          <!-- Mostrar erro de validação -->
          <div v-if="validationError" class="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-600">{{ validationError }}</p>
          </div>

          <div class="flex items-center justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="isSaving"
              class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
            >
              {{ isSaving ? 'Salvando...' : (editingSummary ? 'Atualizar' : 'Criar') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Notification Toast -->
    <NotificationToast
      :visible="notification.visible"
      :type="notification.type"
      :title="notification.title"
      :message="notification.message"
      @close="notification.visible = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { dailySummariesAPI } from '@/services/api'
import { formatDateForDisplay } from '@/utils/dateUtils'
import NotificationToast from '@/components/NotificationToast.vue'

const summaries = ref([])
const isLoading = ref(false)
const isSaving = ref(false)
const showCreateModal = ref(false)
const editingSummary = ref(null)
const validationError = ref('')

const notification = reactive({
  visible: false,
  type: 'success',
  title: '',
  message: ''
})

const summaryForm = reactive({
  title: '',
  content: ''
})

// Separar resumo de hoje dos anteriores
const todaySummary = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return summaries.value.find(summary => summary.date === today)
})

const pastSummaries = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return summaries.value.filter(summary => summary.date !== today)
})

const showNotification = (type, title, message = '') => {
  notification.type = type
  notification.title = title
  notification.message = message
  notification.visible = true
}

const loadSummaries = async () => {
  isLoading.value = true
  try {
    const response = await dailySummariesAPI.list()
    summaries.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar resumos:', error)
    showNotification('error', 'Erro ao carregar resumos', 'Tente novamente mais tarde.')
  } finally {
    isLoading.value = false
  }
}

const checkAndCreateSummary = () => {
  if (todaySummary.value) {
    editSummary(todaySummary.value)
  } else {
    showCreateModal.value = true
  }
}

const saveSummary = async () => {
  validationError.value = ''
  isSaving.value = true
  
  try {
    if (editingSummary.value) {
      await dailySummariesAPI.update(editingSummary.value.id, summaryForm)
      showNotification('success', 'Resumo atualizado com sucesso!')
    } else {
      await dailySummariesAPI.create(summaryForm)
      showNotification('success', 'Resumo criado com sucesso!')
    }
    closeModal()
    loadSummaries()
  } catch (error) {
    console.error('Erro ao salvar resumo:', error)
    const errorMsg = error.response?.data?.detail || 
                    error.response?.data?.message ||
                    'Erro ao salvar resumo'
    validationError.value = errorMsg
  } finally {
    isSaving.value = false
  }
}

const editSummary = (summary) => {
  editingSummary.value = summary
  summaryForm.title = summary.title
  summaryForm.content = summary.content
  showCreateModal.value = true
  validationError.value = ''
}

const deleteSummary = async (summaryId) => {
  if (confirm('Tem certeza que deseja excluir este resumo?')) {
    try {
      await dailySummariesAPI.delete(summaryId)
      showNotification('success', 'Resumo excluído com sucesso!')
      loadSummaries()
    } catch (error) {
      console.error('Erro ao excluir resumo:', error)
      showNotification('error', 'Erro ao excluir resumo')
    }
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingSummary.value = null
  summaryForm.title = ''
  summaryForm.content = ''
  validationError.value = ''
}

onMounted(() => {
  loadSummaries()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>