<template>
  <div>
    <CabecalhoPessoa />
    <h1><br><br></h1>
    <h1>Vamos Publicar algo novo? <br></h1>
    <Message v-show="msgvisible" :msg="msg" />

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
import CabecalhoPessoa from '../components/CabecalhoPessoa.vue';
import axios from "axios";

// Configura o Axios para enviar cookies
axios.defaults.withCredentials = true;

export default {
  name: "FormsPubli",
  components: {
    Message,
    CabecalhoPessoa,
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
    // Método para lidar com o upload da imagem
    handleFileUpload(event) {
      this.imagem = event.target.files[0];
      console.log("Imagem selecionada:", this.imagem);
    },

    // Método para enviar o formulário
    async submitForm(e) {
      e.preventDefault();
      console.log("Iniciando envio do formulário...");

      // Verifica se uma imagem foi selecionada
      if (!this.imagem) {
        this.msg = "Por favor, selecione uma imagem.";
        this.msgvisible = true;
        setTimeout(() => (this.msgvisible = false), 3000);
        console.log("Nenhuma imagem selecionada.");
        return;
      }

      try {
        console.log("Obtendo informações do usuário logado...");
        const response = await axios.get("http://localhost:5000/autor-logado");
        const usuarioLogado = response.data;
        console.log("Dados do usuário logado:", usuarioLogado);

        if (!usuarioLogado || !usuarioLogado.NomeUsuario) {
          this.msg = "Usuário não autenticado.";
          this.msgvisible = true;
          setTimeout(() => (this.msgvisible = false), 3000);
          console.log("Usuário não autenticado.");
          return;
        }

        const nomeUsuario = usuarioLogado.NomeUsuario;
        console.log("Nome do usuário logado:", nomeUsuario);

        // Converte a imagem para base64
        const reader = new FileReader();
        reader.readAsDataURL(this.imagem);
        reader.onload = async () => {
          const base64Image = reader.result.split(",")[1]; // Remove o prefixo "data:image/..."
          console.log("Imagem convertida para base64.");

          // Dados da obra
          const obra = {
            imagem: base64Image, // Imagem em base64
            tipoarquivo: this.tipoArquivo,
            titulo: this.titulo,
            descricao: this.descricao,
            dataPublicacao: this.dataPublicacao,
            estiloArte: this.estilo,
            usuario: nomeUsuario, // Nome do usuário logado
            paisGaleria: this.paisGaleria,
            altura: parseFloat(this.altura),
            largura: parseFloat(this.largura),
          };

          console.log("Dados da obra a serem enviados:", obra);

          // Envia os dados para o backend
          const response = await axios.post("http://localhost:5000/inserir-obra", obra);
          console.log("Resposta do backend:", response.data);

          // Exibe mensagem de sucesso
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
          this.imagem = null;

          console.log("Formulário limpo e redirecionando para a página /Autor...");

          // Redireciona para a página /Autor
          this.$router.push({ name: 'Autor' });
        };
      } catch (error) {
        console.error("Erro ao salvar obra:", error);
        this.msg = "Erro ao salvar a obra!";
        this.msgvisible = true;
        setTimeout(() => (this.msgvisible = false), 3000);
      }
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