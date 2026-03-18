<template>
  <div id="members-field" v-show="visible">
    <label class="form-label">{{ label }}</label>
    <select
      :name="name"
      :id="'id_' + name"
      class="form-control"
      multiple
      v-model="selected"
    >
      <option
        v-for="opt in options"
        :key="opt.value"
        :value="opt.value"
      >
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  name: { type: String, default: 'members' },
  label: { type: String, default: 'Members' },
  options: { type: Array, default: () => [] },
  modelValue: { type: Array, default: () => [] },
  visible: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue'])

const selected = ref([...props.modelValue])

watch(selected, (val) => {
  emit('update:modelValue', val)
})

watch(
  () => props.modelValue,
  (val) => {
    selected.value = [...val]
  }
)
</script>
