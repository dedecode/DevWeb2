<template>
  <div class="w-full space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Resumos Semanais</h1>
          <p class="text-gray-600 mt-2">Documente seu progresso da semana</p>
        </div>
        <button
          @click="showCreateModal = true"
          class="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors shadow-sm"
        >
          Novo Resumo Semanal
        </button>
      </div>
    </div>

    <!-- Summaries List -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6">
        <div v-if="isLoading" class="text-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
        </div>
        
        <div v-else-if="summaries.length === 0" class="text-center py-8">
          <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <p class="text-gray-500">Nenhum resumo semanal encontrado</p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="summary in summaries"
            :key="summary.id"
            class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="font-semibold text-gray-900 mb-2">{{ summary.title }}</h3>
                <p class="text-sm text-gray-500 mb-3">
                  {{ formatDate(summary.week_start) }} - {{ formatDate(summary.week_end) }}
                </p>
                <div class="text-gray-700 whitespace-pre-wrap">{{ summary.content }}</div>
              </div>
              <div class="flex items-center space-x-2 ml-4">
                <button
                  @click="shareOnLinkedIn(summary)"
                  class="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                  title="Compartilhar no LinkedIn"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                  </svg>
                </button>
                <button
                  @click="editSummary(summary)"
                  class="p-2 text-gray-400 hover:text-primary-600 transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  @click="deleteSummary(summary.id)"
                  class="p-2 text-gray-400 hover:text-red-600 transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
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
          {{ editingSummary ? 'Editar Resumo Semanal' : 'Novo Resumo Semanal' }}
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
              placeholder="Digite o título do resumo semanal"
            />
          </div>

          <div class="bg-blue-50 p-4 rounded-lg">
            <p class="text-sm text-blue-700">
              Registre seus feitos da semana!
            </p>
          </div>

          <div>
            <label for="content" class="block text-sm font-medium text-gray-700 mb-1">
              Conteúdo
            </label>
            <textarea
              id="content"
              v-model="summaryForm.content"
              rows="10"
              class="w-full px-3 py-2 border border-gray-300 bg-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Reflita sobre sua semana: principais conquistas, desafios enfrentados, lições aprendidas..."
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
import { ref, reactive, onMounted } from 'vue'
import { weeklySummariesAPI } from '@/services/api'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
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

const formatDate = (dateStr) => {
  return format(new Date(dateStr), 'dd/MM/yyyy', { locale: ptBR })
}

const showNotification = (type, title, message = '') => {
  notification.type = type
  notification.title = title
  notification.message = message
  notification.visible = true
}

const shareOnLinkedIn = (summary) => {
  const postText = `${summary.title}

📅 Período: ${formatDate(summary.week_start)} - ${formatDate(summary.week_end)}

${summary.content}

#produtividade #crescimentoprofissional #reflexaosemanal #linkedin`

  const userChoice = confirm(
    'Como você gostaria de compartilhar?\n\n' +
    'OK = Abrir LinkedIn com texto pré-formatado\n' +
    'Cancelar = Copiar texto e você cola manualmente'
  )

  if (userChoice) {
    const text = encodeURIComponent(postText)
    const url = `https://www.linkedin.com/sharing/share-offsite/?text=${text}`
    window.open(url, '_blank', 'width=600,height=600,scrollbars=yes,resizable=yes')
  } else {
    navigator.clipboard.writeText(postText).then(() => {
      showNotification('success', '✅ Texto copiado!', 'Agora você pode colar no LinkedIn.')
      window.open('https://www.linkedin.com/feed/', '_blank')
    }).catch(() => {
      prompt('Copie este texto para o LinkedIn:', postText)
    })
  }
}

const loadSummaries = async () => {
  isLoading.value = true
  try {
    const response = await weeklySummariesAPI.list()
    summaries.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar resumos semanais:', error)
    showNotification('error', 'Erro ao carregar resumos', 'Tente novamente mais tarde.')
  } finally {
    isLoading.value = false
  }
}

const saveSummary = async () => {
  validationError.value = ''
  isSaving.value = true
  
  try {
    if (editingSummary.value) {
      await weeklySummariesAPI.update(editingSummary.value.id, summaryForm)
      showNotification('success', 'Resumo semanal atualizado!')
    } else {
      await weeklySummariesAPI.create(summaryForm)
      showNotification('success', 'Resumo semanal criado!')
    }
    closeModal()
    loadSummaries()
  } catch (error) {
    console.error('Erro ao salvar resumo semanal:', error)
    const errorMsg = error.response?.data?.detail || 
                    error.response?.data?.message || 
                    'Erro ao salvar resumo semanal'
    validationError.value = errorMsg
  } finally {
    isSaving.value = false
  }
}

const editSummary = (summary) => {
  editingSummary.value = summary
  summaryForm.title = summary.title
  summaryForm.content = summary.content
  validationError.value = ''
}

const deleteSummary = async (summaryId) => {
  if (confirm('Tem certeza que deseja excluir este resumo semanal?')) {
    try {
      await weeklySummariesAPI.delete(summaryId)
      showNotification('success', 'Resumo semanal excluído!')
      loadSummaries()
    } catch (error) {
      console.error('Erro ao excluir resumo semanal:', error)
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