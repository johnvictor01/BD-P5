<template>
  <div class="backdrop">
    <div class="container">
      <div
        class="circle"
        :class="{ spinning: isSpinning, filled: isFilled }"
      >
        <span v-if="isFilled" class="checkmark">✔</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: Boolean
})

const isSpinning = ref(false)
const isFilled = ref(false)

watch(() => props.show, (newVal) => {
  console.log('Prop show mudou:', newVal) // 👈 teste aqui
  if (newVal) {
    startAnimation()
  }
})

const startAnimation = () => {
  isSpinning.value = true
  isFilled.value = false
  
  setTimeout(() => {
    isSpinning.value = false
    isFilled.value = true
  }, 1500)
}
</script>

<style scoped>
.backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.circle {
  width: 200px;
  height: 200px;
  border: 10px solid #4caf50;
  border-radius: 50%;
  border-top-color: transparent;
  transition: all 0.5s ease-in-out;
  position: relative;
}

.spinning {
  animation: spin 1s linear infinite;
}

.filled {
  border: none;
  background-color: #4caf50;
}

.checkmark {
  position: absolute;
  font-size: 5rem;
  color: white;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>