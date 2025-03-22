<template>
    <div>
        <h2>Editando a obra com ID: {{ obraId }}</h2>
        <!-- Lógica para editar a obra baseada no ID -->
    </div>
</template>

<script>
export default {
    name: 'FormsEditPubli',

    props: ['obraId'], // Aqui você recebe o parâmetro da URL

    mounted() {
        console.log('ID da obra selecionada:', this.obraId);
        // Agora você pode fazer o que for necessário com esse ID
    }
};
</script>

<script>
export default {
  name: "FormsEditPubli",
  computed: {
    obraId() {
      return this.$route.params.id;
    }
  }
};
</script>
