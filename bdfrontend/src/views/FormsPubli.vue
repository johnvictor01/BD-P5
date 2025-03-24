<template>
    <div>
      <CabecalhoPessoa/>
      <Message v-show="msgvisible" :msg="msg" />
     =
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
            <label for="imagem">Imagem</label>
            <input type="file" id="imagem" @change="handleFileUpload" />
          </div>
  
          <div class="input-container">
            <label for="tipoArquivo">Tipo de Arquivo</label>
            <input type="text" id="tipoArquivo" v-model="tipoArquivo" required />
          </div>
  
          <div class="input-container">
            <label for="dataPublicacao">Data de Publicação</label>
            <input type="date" id="dataPublicacao" v-model="dataPublicacao" required />
          </div>
  
          <div class="input-container">
            <label for="estilo">Estilo de Arte</label>
            <input type="text" id="estilo" v-model="estilo" required />
          </div>
  
          <div class="input-container">
            <label for="paisGaleria">País da Galeria</label>
            <input type="text" id="paisGaleria" v-model="paisGaleria" required />
          </div>
  
          <div class="input-container">
            <label for="altura">Altura (cm)</label>
            <input type="number" id="altura" v-model="altura" required />
          </div>
  
          <div class="input-container">
            <label for="largura">Largura (cm)</label>
            <input type="number" id="largura" v-model="largura" required />
          </div>
  
          <div class="input-container">
            <input type="submit" class="submit-btn" value="Publicar Obra" />
          </div>
        </form>
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
        titulo: "",
        descricao: "",
        imagem: null,
        tipoArquivo: "",
        dataPublicacao: "",
        estilo: "",
        paisGaleria: "",
        altura: "",
        largura: "",
        msg: "",
        msgvisible: false,
      };
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

      handleFileUpload(event) {
        this.imagem = event.target.files[0];
      },

      async submitForm(e) {
        e.preventDefault();

        const userId = localStorage.getItem("userId");

        // Simulação de uma obra enviada
        const obra = {
          titulo: this.titulo,
          descricao: this.descricao,
          tipoArquivo: this.tipoArquivo,
          dataPublicacao: this.dataPublicacao,
          estilo: this.estilo,
          autor: userId, // ID automático
          paisGaleria: this.paisGaleria,
          altura: parseFloat(this.altura),
          largura: parseFloat(this.largura),
        };

        // Simulação de uma resposta da API
        console.log("Enviando JSON:", obra);

        // Simula uma resposta de sucesso
        this.msg = "Obra publicada com sucesso!";
        this.msgvisible = true;
        setTimeout(() => (this.msgvisible = false), 3000);

        // Limpa o formulário após o envio
        this.titulo = "";
        this.descricao = "";
        this.tipoArquivo = "";
        this.dataPublicacao = "";
        this.estilo = "";
        this.paisGaleria = "";
        this.altura = "";
        this.largura = "";
        
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