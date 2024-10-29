<template>
  <div>
    <h1>Вес животных</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>ID Животного</th>
          <th>Дата</th>
          <th>Вес (кг)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="weight in weights" :key="weight.id">
          <td>{{ weight.id }}</td>
          <td>{{ weight.animal_id }}</td>
          <td>{{ formatDate(weight.date) }}</td>
          <td>{{ weight.weight_kg }}</td>
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
      weights: []
    };
  },
  mounted() {
    this.fetchWeights();
  },
  methods: {
    async fetchWeights() {
      try {
        const response = await axios.get('/api/weightings');
        this.weights = response.data.weightings; 
      } catch (error) {
        console.error("Ошибка при получении данных о весах животных:", error);
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
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
