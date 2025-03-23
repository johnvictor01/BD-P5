<template>
    <div>
      <CabecalhoPessoa />
      <br>
      <MyBiblio />
      <br /> 
      <h1>Vamos as compras?</h1>
      <div class="Filtros">
        <Filters @adicionar-ao-carrinho="adicionarAoCarrinho" />
      </div>
      <div class="Carrinho">
        <Carrinho :itens="itensCarrinho" />
      </div>
    </div>
  </template>
  
  <script>
  import CabecalhoPessoa from '../components/CabecalhoPessoa.vue';
  import Filters from '../components/Filters.vue';
  import Carrinho from '../components/Carrinho.vue';
  import MyBiblio from '../components/MyBiblio.vue';
  
  export default {
    name: 'ClientView',
    components: {
      CabecalhoPessoa,
      Filters,
      Carrinho,
        MyBiblio,
    },
    data() {
      return {
        itensCarrinho: [], // Armazena os itens do carrinho
      };
    },
    methods: {
      // Adiciona uma obra ao carrinho
      adicionarAoCarrinho(obra) {
        // Verifica se o item já existe no carrinho
        const itemExistente = this.itensCarrinho.find((item) => item.id === obra.id);
        if (!itemExistente) {
          this.itensCarrinho.push(obra); // Adiciona o item ao carrinho
        } else {
          alert('Este item já está no carrinho.'); // Ou você pode aumentar a quantidade
        }
      },
    },
  };
  </script>
  
  <style>
  .Filtros {
    margin-top: 2rem;
  }
  
  .Carrinho {
    margin-top: 2rem;
  }
  </style>