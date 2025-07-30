<template>
  <div class="w-full space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Tarefas</h1>
          <p class="text-gray-600 mt-2">Gerencie suas tarefas</p>
        </div>
        <button
          @click="showCreateModal = true"
          class="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors shadow-sm"
        >
          Nova Tarefa
        </button>
      </div>
    </div>

    <!-- Tasks List -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6">
        <div v-if="isLoading" class="text-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
        </div>
        
        <div v-else-if="tasks.length === 0" class="text-center py-8">
          <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p class="text-gray-500">Nenhuma tarefa para hoje</p>
          <button
            @click="showCreateModal = true"
            class="mt-3 text-primary-600 hover:text-primary-700 font-medium"
          >
            Criar primeira tarefa
          </button>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div class="flex-1">
              <h3 class="font-medium text-gray-900">{{ task.title }}</h3>
              <p class="text-sm text-gray-500">Hoje, {{ formatDateForDisplay(task.date) }}</p>
            </div>
            <div class="flex items-center space-x-2">
              <button
                @click="editTask(task)"
                class="p-2 text-gray-400 hover:text-primary-600 transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                @click="deleteTask(task.id)"
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

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal || editingTask"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg max-w-md w-full p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">
          {{ editingTask ? 'Editar Tarefa' : 'Nova Tarefa' }}
        </h2>
        
        <form @submit.prevent="saveTask" class="space-y-4">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700 mb-1">
              Título
            </label>
            <input
              id="title"
              v-model="taskForm.title"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 bg-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Digite o título da tarefa"
            />
          </div>

          <div class="bg-blue-50 p-3 rounded-lg">
            <p class="text-sm text-blue-700">
              📅 Esta tarefa será criada para hoje
            </p>
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
              {{ isSaving ? 'Salvando...' : (editingTask ? 'Atualizar' : 'Criar') }}
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
import { tasksAPI } from '@/services/api'
import { formatDateForDisplay } from '@/utils/dateUtils'
import NotificationToast from '@/components/NotificationToast.vue'

const tasks = ref([])
const isLoading = ref(false)
const isSaving = ref(false)
const showCreateModal = ref(false)
const editingTask = ref(null)
const validationError = ref('')

const notification = reactive({
  visible: false,
  type: 'success',
  title: '',
  message: ''
})

const taskForm = reactive({
  title: ''
})

const showNotification = (type, title, message = '') => {
  notification.type = type
  notification.title = title
  notification.message = message
  notification.visible = true
}

const loadTasks = async () => {
  isLoading.value = true
  try {
    const today = new Date().toISOString().split('T')[0]
    const response = await tasksAPI.list({ date: today })
    tasks.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar tarefas:', error)
    showNotification('error', 'Erro ao carregar tarefas', 'Tente novamente mais tarde.')
  } finally {
    isLoading.value = false
  }
}

const saveTask = async () => {
  validationError.value = ''
  isSaving.value = true
  
  try {
    if (editingTask.value) {
      await tasksAPI.update(editingTask.value.id, taskForm)
      showNotification('success', 'Tarefa atualizada com sucesso!')
    } else {
      await tasksAPI.create(taskForm)
      showNotification('success', 'Tarefa criada com sucesso!')
    }
    closeModal()
    loadTasks()
  } catch (error) {
    console.error('Erro ao salvar tarefa:', error)
    const errorMsg = error.response?.data?.detail || 'Erro ao salvar tarefa'
    showNotification('error', 'Erro ao salvar', errorMsg)
  } finally {
    isSaving.value = false
  }
}

const editTask = (task) => {
  editingTask.value = task
  taskForm.title = task.title
  validationError.value = ''
}

const deleteTask = async (taskId) => {
  if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
    try {
      await tasksAPI.delete(taskId)
      showNotification('success', 'Tarefa excluída com sucesso!')
      loadTasks()
    } catch (error) {
      console.error('Erro ao excluir tarefa:', error)
      showNotification('error', 'Erro ao excluir tarefa')
    }
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingTask.value = null
  taskForm.title = ''
  validationError.value = ''
}

onMounted(() => {
  loadTasks()
})
</script>