<template>
    <div>
      <CabecalhoPessoa />
      <div class="payment-container"
      >
        <h2>Selecione o Método de Pagamento</h2>
        <div class="payment-cards">
          <!-- Card de Cartão -->
          <div
            :class="['payment-card', { selected: selectedPayment === 'cartao' }]"
            @click="selectPayment('cartao')"
          >
            <div class="circle" v-if="selectedPayment === 'cartao'"></div>
            <h3>Cartão de Crédito/Débito</h3>
            <p>Pague com seu cartão de crédito ou débito.</p>
          </div>
  
          <!-- Card de PIX -->
          <div
            :class="['payment-card', { selected: selectedPayment === 'pix' }]"
            @click="selectPayment('pix')"
          >
            <div class="circle" v-if="selectedPayment === 'pix'"></div>
            <h3>PIX</h3>
            <p>Pague instantaneamente com PIX.</p>
          </div>
  
          <!-- Card de Boleto -->
          <div
            :class="['payment-card', { selected: selectedPayment === 'boleto' }]"
            @click="selectPayment('boleto')"
          >
            <div class="circle" v-if="selectedPayment === 'boleto'"></div>
            <h3>Boleto Bancário</h3>
            <p>Pague com boleto bancário.</p>
          </div>
        </div>
  
        <!-- Botão de Continuar -->
        <button @click="continuarPagamento" class="btn-continuar">Continuar</button>
      </div>
      <br><div class="message">
        <Message :msg="message" v-if="messageVisible" /></div>
    </div>
  </template>
  
  <script>
  import CabecalhoPessoa from '../components/CabecalhoPessoa.vue';
  import Message from '../components/Message.vue';
  
  export default {
    name: 'TypePayment',
    components: {
      CabecalhoPessoa,
      Message,
    },
    data() {
      return {
        selectedPayment: null, // Armazena o método de pagamento selecionado
        message: '', // Mensagem a ser exibida
        messageVisible: false, // Controla a visibilidade da mensagem
      };
    },
    methods: {
      // Seleciona o método de pagamento
      selectPayment(metodo) {
        this.selectedPayment = metodo;
      },
  
      // Redireciona para a próxima etapa de pagamento
      continuarPagamento() {
        if (!this.selectedPayment) {
          alert('Selecione um método de pagamento.');
          return;
        }
  
        switch (this.selectedPayment) {
          case 'cartao':
            this.message = 'Pagamento no cartão do Vasco aprovado';
            this.messageVisible = true;
            break;
          case 'pix':
            this.message = 'Pagamento no Pix do Vasco aprovado';
            this.messageVisible = true;
            break;
          case 'boleto':
            this.message = 'Pagamento no Boleto Fiado do Flamengo aprovado';
            this.messageVisible = true;
            break;
          default:
            break;
        }
  
        setTimeout(() => {
          this.messageVisible = false;
            this.$router.push({ name: 'Client' });
        }, 3000);

      },
    },
  };
  </script>
  
  <style>
  .payment-container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    text-align: center;
  }
  
.message {
    margin-top: 30rem;
  }

  .payment-cards {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-top: 20px;
  }
  
  .payment-card {
    flex: 1;
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 20px;
    cursor: pointer;
    position: relative;
    transition: border-color 0.3s ease;
  }
  
  .payment-card.selected {
    border-color: #4caf50;
  }
  
  .payment-card h3 {
    margin: 0 0 10px;
    font-size: 1.5em;
  }
  
  .payment-card p {
    margin: 0;
    color: #666;
  }
  
  .circle {
    width: 20px;
    height: 20px;
    background-color: #4caf50;
    border-radius: 50%;
    position: absolute;
    top: 10px;
    right: 10px;
  }
  
  .btn-continuar {
    padding: 10px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 20px;
    font-size: 16px;
  }
  
  .btn-continuar:hover {
    background-color: #45a049;
  }
  </style>