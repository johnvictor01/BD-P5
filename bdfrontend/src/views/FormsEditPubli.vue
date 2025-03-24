<template>
  <div>
    <CabecalhoPessoa />
    <h1><br></h1>
    <h1>Edite sua Obra</h1>
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
</template>

<script>
import axios from "axios";
import CabecalhoPessoa from "../components/CabecalhoPessoa.vue";

export default {
  name: "FormsPubli",
  components: {
    CabecalhoPessoa,
  },
  data() {
    return {
      titulo: "",
      descricao: "",
      isEditing: false, // Indica se está no modo de edição
      obraId: null, // Armazena o ID da obra em edição
      msg: "",
      msgvisible: false,
    };
  },
  mounted() {
    // Verifica se há uma obra na rota ao carregar o componente
    if (this.$route.params.obra) {
      this.isEditing = true;
      this.obraId = this.$route.params.obra.id; // Armazena o ID da obra
      this.titulo = this.$route.params.obra.nome; // Preenche o campo 'nome'
      this.descricao = this.$route.params.obra.informacoes; // Preenche o campo 'informacoes'
    }
  },
  methods: {
  async submitForm(e) {
    e.preventDefault();

    // Dados da obra
    const obra = {
      id: this.$route.params.id, // Obtém o ID da obra da URL
      Titulo: this.titulo, // Use o campo 'Titulo' (conforme esperado pelo backend)
      Descricao: this.descricao, // Use o campo 'Descricao' (conforme esperado pelo backend)
    };

    try {
      // Envia uma requisição POST para o backend
      const response = await axios.post("http://localhost:5000/editar-obra", obra);
      console.log("Obra atualizada:", response.data);

      // Exibe mensagem de sucesso
      this.msg = "Obra atualizada com sucesso!";
      this.msgvisible = true;
      setTimeout(() => (this.msgvisible = false), 3000);

      // Limpa o formulário após o envio
      this.titulo = "";
      this.descricao = "";

      // Redireciona para a página /Autor
      this.$router.push({ name: 'Autor' });
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