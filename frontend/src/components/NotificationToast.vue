<template>
  <div
    v-if="visible"
    class="fixed top-4 right-4 z-50 max-w-sm w-full bg-white border border-gray-200 rounded-lg shadow-lg transform transition-all duration-300"
    :class="{
      'translate-x-0': visible,
      'translate-x-full': !visible
    }"
  >
    <div class="p-4">
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <!-- Ícone de sucesso  -->
          <svg
            v-if="type === 'success'"
            class="w-5 h-5 text-green-400"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"
            />
          </svg>
          
          <!-- Ícone de erro talvez troque--> 
          <svg
            v-else-if="type === 'error'"
            class="w-5 h-5 text-red-400"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clip-rule="evenodd"
            />
          </svg>
          
          <!-- Ícone de aviso -->
          <svg
            v-else
            class="w-5 h-5 text-yellow-400"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
              clip-rule="evenodd"
            />
          </svg>
        </div>
        
        <div class="ml-3 w-0 flex-1">
          <p class="text-sm font-medium text-gray-900">{{ title }}</p>
          <p v-if="message" class="mt-1 text-sm text-gray-500">{{ message }}</p>
        </div>
        
        <div class="ml-4 flex-shrink-0 flex">
          <button
            @click="close"
            class="inline-flex text-gray-400 hover:text-gray-500 focus:outline-none"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'success', 
    validator: (value) => ['success', 'error', 'warning'].includes(value)
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    default: ''
  },
  duration: {
    type: Number,
    default: 4000
  }
})

const emit = defineEmits(['close'])

let timeoutId = null

const close = () => {
  emit('close')
}

watch(() => props.visible, (newValue) => {
  if (newValue && props.duration > 0) {
    timeoutId = setTimeout(() => {
      close()
    }, props.duration)
  } else if (timeoutId) {
    clearTimeout(timeoutId)
  }
})
</script>