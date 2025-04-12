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
import axios from 'axios';
import CabecalhoPessoa from '../components/CabecalhoPessoa.vue';
import Message from '../components/Message.vue';

// Configuração global do Axios
const api = axios.create({
  baseURL: 'http://localhost:5000',
  withCredentials: true,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

export default {
  name: 'TypePayment',
  components: {
    CabecalhoPessoa,
    Message,
  },
  data() {
    return {
      selectedPayment: null,
      message: '',
      messageVisible: false,
      isProcessing: false
    };
  },
  methods: {
    selectPayment(metodo) {
      this.selectedPayment = metodo;
    },

    async continuarPagamento() {
      if (this.isProcessing) return;
      
      if (!this.selectedPayment) {
        this.showMessage('Selecione um método de pagamento.');
        return;
      }

      this.isProcessing = true;
      this.showMessage('Processando seu pagamento...');

      try {
        const response = await api.post('/finalizar-compra', {
          metodo_pagamento: this.selectedPayment
        });

        if (response.data.sucesso) {
          const successMessages = {
            'cartao': 'Pagamento no cartão aprovado! Redirecionando...',
            'pix': 'Pagamento via PIX aprovado! Redirecionando...',
            'boleto': 'Boleto gerado com sucesso! Redirecionando...'
          };
          
          this.showMessage(successMessages[this.selectedPayment]);
          
          setTimeout(() => {
            this.$router.push({ 
              name: 'Client',
              query: { 
                venda_id: response.data.venda_id,
                success: 'true'
              }
            });
          }, 3000);
        }
      } catch (error) {
        console.error('Erro detalhado:', error);
        
        let errorMessage = 'Erro ao processar pagamento';
        if (error.response) {
          if (error.response.status === 401) {
            errorMessage = 'Sessão expirada. Faça login novamente.';
            setTimeout(() => this.$router.push('/login'), 2000);
          } else if (error.response.data?.erro) {
            errorMessage = error.response.data.erro;
          }
        }
        
        this.showMessage(errorMessage);
      } finally {
        this.isProcessing = false;
      }
    },

    showMessage(msg) {
      this.message = msg;
      this.messageVisible = true;
      setTimeout(() => {
        this.messageVisible = false;
      }, 5000);
    }
  }
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