<template>
    <div>
      <CabecalhoPessoa />
      <Message v-show="msgvisible" :msg="msg" />
      <div v-if="!isLoggedIn">
        <h2>Login</h2>
        <form @submit.prevent="login">
          <div class="input-container">
            <label for="usuario">Usuário</label>
            <input type="text" id="usuario" v-model="usuario" required />
          </div>
  
          <div class="input-container">
            <label for="senha">Senha</label>
            <input type="password" id="senha" v-model="senha" required />
          </div>
  
          <div class="input-container">
            <input type="submit" class="submit-btn" value="Entrar" />
          </div>
        </form>
      </div>
  
      <div v-else>
        <form id="obra-form" @submit="submitForm">
          <div class="input-container">
            <label for="titulo">Título da Obra</label>
            <input type="text" id="titulo" v-model="titulo" required />
          </div>
  
          <div class="input-container">
            <label for="descricao">Descrição</label>
            <textarea id="descricao" v-model="descricao" required></textarea>
          </div>
  
          <div class="input-container">
            <input type="submit" class="submit-btn" :value="isEditing ? 'Salvar Edição' : 'Publicar Obra'" />
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>

  import Message from "../components/Message.vue";
  import CabecalhoPessoa from '../components/CabecalhoPessoa.vue'
  
  export default {
    name: "FormsPubli",
    components: {
      Message,
      CabecalhoPessoa
    },
    data() {
      return {
        usuario: "",
        senha: "",
        isLoggedIn: false,
        titulo: "",
        descricao: "",
        msg: "",
        msgvisible: false,
        isEditing: false, // Indica se está no modo de edição
        obraId: null, // Armazena o ID da obra em edição
      };
    },
    computed: {
      // Verifica se há um ID na rota (modo de edição)
      idDaRota() {
        return this.$route.params.id || null;
      }
    },
    watch: {
      // Observa mudanças no ID da rota
      idDaRota(newId) {
        if (newId) {
          this.isEditing = true;
          this.obraId = newId;
          this.carregarObraParaEdicao();
        }
      }
    },
    mounted() {
      // Verifica se há um ID na rota ao carregar o componente
      if (this.idDaRota) {
        this.isEditing = true;
        this.obraId = this.idDaRota;
        this.carregarObraParaEdicao();
      }
    },
    methods: {
      async login() {
        // Simulação de um JSON fictício para teste
        const usuariosFicticios = [
          { id: 1, usuario: "admin", senha: "123456" },
          { id: 2, usuario: "joao", senha: "senha123" },
          { id: 3, usuario: "maria", senha: "maria456" }
        ];

        // Verifica se o usuário e senha correspondem
        const usuarioEncontrado = usuariosFicticios.find(
          (user) => user.usuario === this.usuario && user.senha === this.senha
        );

        if (usuarioEncontrado) {
          // Simula uma resposta de sucesso
          localStorage.setItem("userId", usuarioEncontrado.id);
          this.isLoggedIn = true;
          this.msg = "Login bem-sucedido!";
        } else {
          // Simula uma resposta de erro
          this.msg = "Usuário ou senha inválidos!";
        }

        this.msgvisible = true;
        setTimeout(() => (this.msgvisible = false), 3000);
      },

      async carregarObraParaEdicao() {
        // Simulação de uma requisição para carregar os dados da obra
        const obrasFicticias = [
          { id: 1, titulo: "Obra 1", descricao: "Descrição da Obra 1" },
          { id: 2, titulo: "Obra 2", descricao: "Descrição da Obra 2" },
          { id: 3, titulo: "Obra 3", descricao: "Descrição da Obra 3" }
        ];

        const obra = obrasFicticias.find(obra => obra.id === parseInt(this.obraId));
        if (obra) {
          this.titulo = obra.titulo;
          this.descricao = obra.descricao;
        } else {
          this.msg = "Obra não encontrada!";
          this.msgvisible = true;
          setTimeout(() => (this.msgvisible = false), 3000);
        }
      },

      async submitForm(e) {
        e.preventDefault();

        const userId = localStorage.getItem("userId");

        // Dados da obra
        const obra = {
          titulo: this.titulo,
          descricao: this.descricao,
          autor: userId,
        };

        if (this.isEditing) {
          // Modo de edição: atualiza a obra existente
          obra.id = this.obraId;
          console.log("Atualizando obra:", obra);
          this.msg = "Obra atualizada com sucesso!";
        } else {
          // Modo de criação: cria uma nova obra
          console.log("Criando nova obra:", obra);
          this.msg = "Obra publicada com sucesso!";
        }

        this.msgvisible = true;
        setTimeout(() => (this.msgvisible = false), 3000);

        // Limpa o formulário após o envio
        this.titulo = "";
        this.descricao = "";

        // Redireciona para a página /Autor
        this.$router.push({ name: 'Autor' });
      },
    },
  };
  </script>
  
  <style>
  #obra-form {
    max-width: 400px;
    margin: 0 auto;
  }
  
  .input-container {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
  }
  
  label {
    font-weight: bold;
    margin-bottom: 5px;
    color: #222;
  }
  
  input,
  textarea {
    padding: 5px;
    width: 100%;
  }
  
  .submit-btn {
    background-color: #222;
    color: #d49400;
    border: 2px solid #22222247;
    border-radius: 10px;
    font-weight: bold;
    font-size: 16px;
    padding: 10px;
    cursor: pointer;
    transition: 0.5s;
  }
  
  .submit-btn:hover {
    background-color: transparent;
    color: #222;
  }
  </style>