<template>
    <div class="biblio-container">
        <h1>Minha Biblioteca de Obras</h1>
        <div class="imagens-container">
            <div v-for="(obra, index) in obras" :key="index" class="imagem-card">
                <img :src="obra.imagem" :alt="obra.nome" />
                <p>{{ obra.nome }}</p>
                <small>{{ obra.informacoes }}</small>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
    name: 'MyBiblio',
    setup() {
        const obras = ref([]);  // Inicializa o array de obras

        // Função para simular a resposta do backend com dados fictícios
        const fetchObras = async () => {
    const response = [
        {
            id: 1,
            imagem: "https://via.placeholder.com/150?text=Mona+Lisa",
            nome: "Mona Lisa",
            informacoes: "Uma das pinturas mais famosas de Leonardo da Vinci."
        },
        {
            id: 2,
            imagem: "https://via.placeholder.com/150?text=A+Noite+Estrelada",
            nome: "A Noite Estrelada",
            informacoes: "Obra-prima de Vincent van Gogh."
        },
        // Mais itens...
    ];
    obras.value = response;
    console.log('Obras carregadas:', obras.value);  // Verificando os dados no console
};


        // Chama a função de buscar as obras assim que o componente for montado
        onMounted(() => {
            fetchObras();
        });

        return { obras };
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
