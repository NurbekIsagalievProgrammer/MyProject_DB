<template>
  <div>
    <h1>Вес животных</h1>
    <button @click="openAddModal">+</button>

    <!-- Таблица весов -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>ID Животного</th>
          <th>Дата</th>
          <th>Вес (кг)</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="weighting in weightings" :key="weighting.id">
          <td>{{ weighting.id }}</td>
          <td>{{ weighting.animal_id }}</td>
          <td>{{ formatDate(weighting.date) }}</td>
          <td>{{ weighting.weight_kg }}</td>
          <td>
            <button @click="openEditModal(weighting)">Редактировать</button>
            <button @click="deleteWeighting(weighting.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно для добавления/редактирования записи веса -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ isEditMode ? "Редактировать запись веса" : "Добавить запись веса" }}</h2>

        <select v-model="currentWeighting.animal_id" required>
          <option disabled value="">Выберите животное</option>
          <option v-for="animal in animals" :key="animal.id" :value="animal.id">
            {{ animal.name }} (ID: {{ animal.id }})
          </option>
        </select>

        <input type="date" v-model="currentWeighting.date" required />
        <input type="number" step="0.01" v-model="currentWeighting.weight_kg" placeholder="Вес (кг)" required />
        <button @click="saveWeighting">{{ isEditMode ? "Сохранить" : "Добавить" }}</button>
        <button @click="closeModal">Отмена</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      weightings: [],
      animals: [], 
      showModal: false,
      isEditMode: false,
      currentWeighting: {
        id: null,
        animal_id: null,
        date: "",
        weight_kg: null,
      },
    };
  },
  mounted() {
    this.fetchWeights();
    this.fetchAnimals(); 
  },
  methods: {
    async fetchWeights() {
      try {
        const response = await axios.get('/api/weightings');
        this.weightings = response.data.weightings; 
      } catch (error) {
        console.error("Ошибка при получении данных о весах:", error);
      }
    },
    
    async fetchAnimals() {
      try {
        const response = await axios.get('/api/animals');
        this.animals = response.data.animals;
      } catch (error) {
        console.error("Ошибка при получении данных о животных:", error);
      }
    },
    
    openAddModal() {
      this.currentWeighting = { id: null, animal_id: null, date: "", weight_kg: null };
      this.isEditMode = false;
      this.showModal = true;
    },
    
    openEditModal(weighting) {
      this.currentWeighting = { ...weighting };
      this.isEditMode = true;
      this.showModal = true;
    },
    
    async saveWeighting() {
      if (!this.currentWeighting.animal_id || !this.currentWeighting.date || this.currentWeighting.weight_kg == null) {
        console.error("Ошибка: Все поля должны быть заполнены.");
        return;
      }

      console.log("Данные для отправки:", this.currentWeighting);

      try {
        const config = {
          headers: {
            'Content-Type': 'application/json',
          },
        };
        
        if (this.isEditMode) {
          await axios.put(`/api/weightings/${this.currentWeighting.id}`, JSON.stringify(this.currentWeighting), config);
        } else {
          await axios.post('/api/weightings', JSON.stringify(this.currentWeighting), config);
        }

        this.fetchWeights();
        this.closeModal();
      } catch (error) {
        console.error("Ошибка при сохранении записи веса:", error.response ? error.response.data : error.message);
      }
    },
    
    async deleteWeighting(id) {
      try {
        await axios.delete(`/api/weightings/${id}`);
        this.fetchWeights();
      } catch (error) {
        console.error("Ошибка при удалении записи веса:", error);
      }
    },
   
    closeModal() {
      this.showModal = false;
      this.currentWeighting = { id: null, animal_id: null, date: "", weight_kg: null };
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
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
  width: 100%;
}
</style>
