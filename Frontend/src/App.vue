<template>
  <router-view></router-view>
</template>
<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
@media (max-width: 768px) {
  .upload-section {
    flex-direction: column;
  }
  
  .upload-card {
    width: 100%;
  }
  
  .compare-button {
    transform: rotate(90deg);
  }
}
</style>
