<template>
  <div>
    <h1>Животные</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Инвентарный номер</th>
          <th>Пол</th>
          <th>Имя</th>
          <th>Дата поступления</th>
          <th>Возраст прибытия (месяцы)</th>
          <th>Порода ID</th>
          <th>ID родителя</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="animal in animals" :key="animal.id">
          <td>{{ animal.id }}</td>
          <td>{{ animal.inventory_number }}</td>
          <td>{{ animal.gender }}</td>
          <td>{{ animal.name }}</td>
          <td>{{ animal.arrival_date }}</td>
          <td>{{ animal.age_months }}</td>
          <td>{{ animal.breed_id }}</td>
          <td>{{ animal.parent_id }}</td>
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
      animals: []
    };
  },
  mounted() {
    this.fetchAnimals();
  },
  methods: {
    async fetchAnimals() {
      try {
        const response = await axios.get('/api/animals');
        this.animals = response.data.animals; 
      } catch (error) {
        console.error("Ошибка при получении данных о животных:", error);
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
