<template>
    <div class="biblio-container">
        <h1>Sua Biblioteca de Obras</h1>
        <div v-if="loading">
            <p>Carregando obras...</p>
        </div>
        <div v-else>
            <div v-if="obras.length === 0">
                <p>Nenhuma obra disponível na biblioteca.</p>
            </div>
            <div v-else class="imagens-container">
                <div v-for="(obra, index) in obras" :key="index" class="imagem-card">
                    <img 
  :src="obra.Imagem ? `data:${obra.TipoArquivo};base64,${obra.Imagem}` : 'https://via.placeholder.com/150?text=Sem+Imagem'" 
  :alt="obra.Titulo" 
/>                    <p>{{ obra.Titulo }}</p>
                    <small>{{ obra.Descricao }}</small>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
    name: 'MyBiblio',
    props: {
        obras: {
            type: Array,
            required: true,
            default: () => [] // Valor padrão como array vazio
        }
    },
    setup(props) {
        const loading = ref(false);  // Controla o estado de carregamento

        // Observa mudanças no props obras
        watch(
            () => props.obras,
            (newObras) => {
                if (newObras.length > 0) {
                    loading.value = false;  // Finaliza o estado de carregamento
                }
            },
            { immediate: true }
        );

        return { loading };
    }
};
</script>

<style scoped>
.biblio-container {
    padding: 20px;
    text-align: center;
}

.imagens-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
}

.imagem-card {
    width: 200px;
    text-align: center;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    background-color: white;
}

.imagem-card img {
    width: 100%;
    height: auto;
    border-radius: 5px;
}

.imagem-card p {
    font-weight: bold;
    margin: 10px 0 5px;
}

.imagem-card small {
    font-size: 12px;
    color: gray;
}
</style>