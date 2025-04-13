<template>
    <div class="cadastro-container">
        <div class="form-group">
            <label for="tipoCadastro">Tipo de Cadastro*</label>
            <select 
                id="tipoCadastro" 
                v-model="selectedType" 
                @change="updateType"
                required
            >
                <option 
                    v-for="(value, key) in TipoCad" 
                    :key="key" 
                    :value="parseInt(key)"
                >
                    {{ value }}
                </option>
            </select>
        </div>

        <div v-show="selectedType !== 0">
            <Cadastro :type="selectedType"/>
        </div>
    </div>
</template>

<script>
import Cadastro from '../components/Cadastro.vue';

export default {
    name: 'Cadastros',
    data() {
        return {
            selectedType: 0, // Inicia com "Selecione o tipo de cadastro"
            TipoCad: {
                0: "Selecione o tipo de cadastro",
                1: "Cliente",
                2: "Autor",
                3: "Colaborador",
            },
        }
    },
    components: {
        Cadastro
    },
    methods: {
        updateType() {
            // Emitir evento para atualizar a prop se necessário
            this.$emit('update:type', this.selectedType);
        }
    }
}
</script>

<style scoped>
.cadastro-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

select:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}
</style>