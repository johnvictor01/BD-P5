<template>
  <div>
    <h2>Deseja Solicitar uma edição de alguma informação de suas obras?</h2>

    <div class="SelectObra">
      <p>Selecione sua Obra:</p>
      <select v-model="selectedObraId">
        <option v-for="obra in obras" :key="obra.id" :value="obra.id">
          {{ obra.nome }} <!-- Use o campo 'nome' da obra -->
        </option>
      </select>
    </div>
    <router-link
      v-if="selectedObraId"
      :to="{ name: 'FormsEditPubli', params: { id: selectedObraId } }"
      class="Data_Publi"
    >
      <button class="btn-solicitar-publi">
        Solicitar Edição de Publicação
      </button>
    </router-link>
  </div>
</template>

<script>
export default {
  name: "ButtonSolicitarEditPubli",
  props: {
    obras: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      selectedObraId: null, // Para armazenar o ID selecionado
    };
  },
};
</script>

<style>
.SelectObra {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px; /* Espaçamento entre o texto e o select */
}

.SelectObra select {
  padding: 10px;
  border-radius: 12px;
  border: 1px solid #ccc;
  font-size: 16px;
  width: 300px;
  text-align: center;
}

.btn-solicitar-publi {
  background-color: rgb(255, 184, 51);
  text-align: center;
  border: none;
  color: rgb(255, 245, 245);
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 12px;
  box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.3);
}

.btn-solicitar-publi:hover {
  transition-duration: 0.5s all;
  background-color: rgb(227, 154, 18);
}

.Data_Publi {
  text-align: center;
}
</style>