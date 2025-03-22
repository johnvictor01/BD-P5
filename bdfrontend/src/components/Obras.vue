<template>
    <div>
        <div class="imagens-container">
            <div v-for="(obra, index) in fakeObras" :key="index" class="imagem-card">
                <img :src="obra.imagem" :alt="obra.nome">
                <p>{{ obra.nome }}</p>
                <small>{{ obra.informacoes }}</small>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    name: 'Obras',
    setup() {
        const fakeObras = ref([
            {
                imagem: 'https://via.placeholder.com/150',
                nome: 'Mona Lisa',
                informacoes: 'Uma das pinturas mais famosas de Leonardo da Vinci.'
            },
            {
                imagem: 'https://via.placeholder.com/150',
                nome: 'A Noite Estrelada',
                informacoes: 'Obra-prima de Vincent van Gogh.'
            },
            {
                imagem: 'https://via.placeholder.com/150',
                nome: 'O Grito',
                informacoes: 'Pintura expressionista de Edvard Munch.'
            },
            {
                imagem: 'https://via.placeholder.com/150',
                nome: 'A Criação de Adão',
                informacoes: 'Afresco famoso de Michelangelo na Capela Sistina.'
            },
            {
                imagem: 'https://via.placeholder.com/150',
                nome: 'Moça com Brinco de Pérola',
                informacoes: 'Pintura de Johannes Vermeer, conhecida como a "Mona Lisa do Norte".'
            },
            {
                imagem: 'https://via.placeholder.com/150',
                nome: 'O Jardim das Delícias Terrenas',
                informacoes: 'Tríptico surrealista de Hieronymus Bosch.'
            }
        ]);

        return { fakeObras };
    }
};
</script>

<style>
.imagens-container {
    margin-top: 70px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
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
