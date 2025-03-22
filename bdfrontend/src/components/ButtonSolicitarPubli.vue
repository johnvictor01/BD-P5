<template>
    <div>
        
        <h2>Deseja publicar outra obra? Clique aqui:</h2>

        <router-link to="/FormsPubli" class="Data_Publi">
            <Button class="btn-solicitar-publi">
            Solicitar Publicação
        </Button>
        
        </router-link>

    </div>
</template>

<script >
export default {
    name: 'ButtonSolicitarPubli',
   
}


</script>

<style>

.btn-solicitar-publi {
    background-color: rgb(255, 184, 51);

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