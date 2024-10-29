<template>
  <div>
    <h1>Типы животных</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Название типа</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="type in types" :key="type.id">
          <td>{{ type.id }}</td>
          <td>{{ type.name }}</td>
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
      types: []
    };
  },
  mounted() {
    this.fetchAnimalTypes();
  },
  methods: {
    async fetchAnimalTypes() {
      try {
        const response = await axios.get('api/animaltypes');
        this.types = response.data.types; 
      } catch (error) {
        console.error("Ошибка при получении данных о типах животных:", error);
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
