<template>
  <router-view/>
</template>


<script>
import HomeView from './views/HomeView.vue'
export default {
  name: 'App',
  components: {
    HomeView
  }
}

</script>
<style>
/*    <router-link to="/about">About</router-link> */ 
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
