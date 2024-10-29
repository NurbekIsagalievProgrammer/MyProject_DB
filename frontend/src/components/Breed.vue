<template>
  <div>
    <h1>Породы животных</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Название породы</th>
          <th>ID типа животного</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="breed in breeds" :key="breed.id">
          <td>{{ breed.id }}</td>
          <td>{{ breed.name }}</td>
          <td>{{ breed.animaltype_id }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      breeds: []
    };
  },
  mounted() {
    this.fetchBreeds();
  },
  methods: {
    async fetchBreeds() {
      try {
        const response = await axios.get('/api/breeds');
        this.breeds = response.data.breeds; 
      } catch (error) {
        console.error("Ошибка при получении данных о породах животных:", error);
      }
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
}
</style>
