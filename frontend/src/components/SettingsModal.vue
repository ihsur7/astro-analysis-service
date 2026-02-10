<script setup lang="ts">
import { ref, watch } from 'vue'
import { X, Database, AlertCircle, CheckCircle2 } from 'lucide-vue-next'
import { useCatalogStore } from '../stores/catalog'

const props = defineProps<{
  show: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const store = useCatalogStore()
const maxRecords = ref(store.maxRecords)
const loading = ref(false)
const error = ref<string | null>(null)
const success = ref(false)

watch(() => props.show, (newVal) => {
  if (newVal) {
    maxRecords.value = store.maxRecords
    error.value = null
    success.value = false
  }
})

async function handleApply() {
  const limit = maxRecords.value
  
  if (limit < 10 || limit > 1000) {
    error.value = 'Limit must be between 10 and 1000'
    return
  }

  loading.value = true
  error.value = null
  success.value = false

  try {
    await store.updateMaxRecords(limit)
    success.value = true
    setTimeout(() => {
      emit('close')
    }, 1500)
  } catch (e: any) {
    error.value = e.message || 'Failed to update settings'
  } finally {
    loading.value = false
  }
}

function handleClose() {
  if (!loading.value) {
    emit('close')
  }
}
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="modal-backdrop" @click.self="handleClose">
        <div class="modal-container">
          <div class="modal-header">
            <div class="header-title">
              <Database :size="20" />
              <h2>Settings</h2>
            </div>
            <button @click="handleClose" class="close-btn" :disabled="loading">
              <X :size="20" />
            </button>
          </div>

          <div class="modal-body">
            <div class="setting-group">
              <label for="max-records" class="setting-label">
                <span class="label-text">Maximum Records</span>
                <span class="label-hint">Number of objects to fetch from NASA (10-1000)</span>
              </label>
              <input
                id="max-records"
                v-model.number="maxRecords"
                type="number"
                min="10"
                max="1000"
                step="50"
                :disabled="loading"
                class="setting-input"
              />
            </div>

            <div v-if="error" class="alert alert-error">
              <AlertCircle :size="18" />
              <span>{{ error }}</span>
            </div>

            <div v-if="success" class="alert alert-success">
              <CheckCircle2 :size="18" />
              <span>Settings updated successfully! Refreshing data...</span>
            </div>

            <div class="info-box">
              <AlertCircle :size="16" />
              <p>
                Changing this value will trigger a new data fetch from the NASA Exoplanet Archive.
                Higher values may take longer to load but provide more comprehensive data.
              </p>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="handleClose" class="btn-secondary" :disabled="loading">
              Cancel
            </button>
            <button @click="handleApply" class="btn-primary" :disabled="loading || success">
              {{ loading ? 'Applying...' : 'Apply & Refresh' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(10, 14, 26, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--primary);
}

.header-title h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  background: transparent;
  border: none;
  border-radius: 0.375rem;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover:not(:disabled) {
  background: var(--surface-hover);
  color: var(--text-secondary);
}

.close-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.setting-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.setting-label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label-text {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-primary);
}

.label-hint {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

.setting-input {
  padding: 0.75rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  color: var(--text-primary);
  font-size: 0.9375rem;
  transition: all 0.2s;
}

.setting-input:focus {
  outline: none;
  border-color: var(--border-focus);
  background: var(--surface);
}

.setting-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: var(--error);
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: var(--success);
}

.info-box {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: var(--primary-light);
  border: 1px solid var(--primary-border);
  border-radius: 0.5rem;
}

.info-box p {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid var(--border);
  justify-content: flex-end;
}

.btn-secondary {
  padding: 0.75rem 1.25rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover:not(:disabled) {
  background: var(--surface-hover);
  border-color: var(--text-tertiary);
}

.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  padding: 0.75rem 1.25rem;
  background: var(--primary);
  border: none;
  border-radius: 0.5rem;
  color: white;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(136, 136, 136, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.2s, opacity 0.2s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
  opacity: 0;
}
</style>
