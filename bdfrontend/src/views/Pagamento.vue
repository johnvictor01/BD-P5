<template>
  <div class="pagamento-container">
    <div class="metodos-pagamento">
      <TypePayment/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import TypePayment from '../components/TypePayment.vue';

axios.defaults.withCredentials = true;

export default {
  name: 'Pagamento',
  components: {
    TypePayment
  },
};
</script>

<style scoped>
.pagamento-container {
  display: flex;
  justify-content: center; /* Alinha no centro horizontalmente */
  align-items: center;     /* Alinha no centro verticalmente */
  min-height: 100vh;
  padding: 1rem;
  background-color: #f5f5f5;
}


.metodos-pagamento {
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.carregando {
  padding: 1rem;
  text-align: center;
  color: #666;
}

@media (max-width: 768px) {
  .pagamento-container {
    grid-template-columns: 1fr;
  }
}
</style>