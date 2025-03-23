<template>
    <div class="carrinho-container">
      <h2>Carrinho</h2>
      <div v-if="itens.length > 0">
        <div v-for="item in itens" :key="item.id" class="item-carrinho">
          <p>{{ item.nome }} - R$ {{ item.valor }}</p>
          <button @click="removerDoCarrinho(item.id)" class="btn-remover">Remover</button>
        </div>
        <p><strong>Total:</strong> R$ {{ total }}</p>
        <button @click="irParaPagamento" class="btn-pagamento">Ir para Pagamento</button>
      </div>
      <div v-else>
        <p>O carrinho está vazio.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'Carrinho',
    props: {
      itens: {
        type: Array,
        required: true,
      },
    },
    setup(props) {
      const router = useRouter();
  
      // Calcula o total do carrinho
      const total = computed(() => {
        return props.itens.reduce((sum, item) => sum + item.valor, 0);
      });
  
      // Remove um item do carrinho
      const removerDoCarrinho = (id) => {
        const index = props.itens.findIndex((item) => item.id === id);
        if (index !== -1) {
          props.itens.splice(index, 1);
        }
      };
  
      // Redireciona para a tela de pagamento
      const irParaPagamento = () => {
        router.push({ name: 'Pagamento' }); // Navega para a rota de pagamento
      };
  
      return {
        total,
        removerDoCarrinho,
        irParaPagamento,
      };
    },
  };
  </script>
  
  <style>
  .carrinho-container {
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin-top: 20px;
  }
  
  .item-carrinho {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #ccc;
  }
  
  .btn-remover {
    padding: 5px 10px;
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-remover:hover {
    background-color: #e53935;
  }
  
  .btn-pagamento {
    padding: 10px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  .btn-pagamento:hover {
    background-color: #45a049;
  }
  </style>