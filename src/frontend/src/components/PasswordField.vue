<template>
  <div class="input-group">
    <input
      :type="visible ? 'text' : 'password'"
      :name="name"
      :id="id"
      class="form-control"
      :placeholder="placeholder"
      :required="required"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <button
      class="btn btn-outline-secondary"
      type="button"
      @click="visible = !visible"
    >
      <i :class="visible ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  name: { type: String, required: true },
  id: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  required: { type: Boolean, default: false },
  modelValue: { type: String, default: '' },
})

defineEmits(['update:modelValue'])

const visible = ref(false)
</script>
