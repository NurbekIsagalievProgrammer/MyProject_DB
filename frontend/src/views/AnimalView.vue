<template>
  <div>
    <h1>Животные</h1>
    <button @click="openAddModal">+</button>

    <!-- Таблица животных -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Номер инвентаря</th>
          <th>Пол</th>
          <th>Имя</th>
          <th>Дата поступления</th>
          <th>Возраст (мес)</th>
          <th>ID Породы</th>
          <th>ID Родителя</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="animal in animals" :key="animal.id">
          <td>{{ animal.id }}</td>
          <td>{{ animal.inventory_number }}</td>
          <td>{{ animal.gender }}</td>
          <td>{{ animal.name }}</td>
          <td>{{ formatDate(animal.arrival_date) }}</td>
          <td>{{ animal.age_months }}</td>
          <td>{{ animal.breed_id }}</td>
          <td>{{ animal.parent_id }}</td>
          <td>
            <button @click="openEditModal(animal)">Редактировать</button>
            <button @click="deleteAnimal(animal.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно для добавления/редактирования -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ isEditMode ? "Редактировать животное" : "Добавить животное" }}</h2>
        <input type="text" v-model="currentAnimal.inventory_number" placeholder="Номер инвентаря" required />
        <select v-model="currentAnimal.gender" required>
          <option disabled value="">Выберите пол</option>
          <option value="male">Мужской</option>
          <option value="female">Женский</option>
        </select>
        <input type="text" v-model="currentAnimal.name" placeholder="Имя" required />
        <input type="date" v-model="currentAnimal.arrival_date" placeholder="Дата поступления" required />
        <input type="number" v-model="currentAnimal.age_months" placeholder="Возраст (мес)" min="0" required />

        <select v-model="currentAnimal.breed_id" required>
          <option disabled value="">Выберите породу</option>
          <option v-for="breed in breeds" :key="breed.id" :value="breed.id">
            {{ breed.name }}
          </option>
        </select>

        <select v-model="currentAnimal.parent_id">
          <option :value="null">Нет родителя</option>
          <option v-for="animal in animals" :key="animal.id" :value="animal.id">
            {{ animal.name }}
          </option>
        </select>

        <button @click="saveAnimal">{{ isEditMode ? "Сохранить" : "Добавить" }}</button>
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
      animals: [],
      breeds: [],
      showModal: false,
      isEditMode: false,
      currentAnimal: {
        id: null,
        inventory_number: "",
        gender: "",
        name: "",
        arrival_date: "",
        age_months: 0,
        breed_id: null,
        parent_id: null,
      },
    };
  },
  mounted() {
    this.fetchAnimals();
    this.fetchBreeds();
  },
  methods: {
    async fetchAnimals() {
      try {
        const response = await axios.get('/api/animals');
        this.animals = response.data.animals || [];
      } catch (error) {
        console.error("Ошибка при получении данных о животных:", error);
      }
    },
    async fetchBreeds() {
      try {
        const response = await axios.get('/api/breeds');
        this.breeds = response.data.breeds || [];
      } catch (error) {
        console.error("Ошибка при получении данных о породах:", error);
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    openAddModal() {
      this.currentAnimal = {
        id: null,
        inventory_number: "",
        gender: "",
        name: "",
        arrival_date: "",
        age_months: 0,
        breed_id: null,
        parent_id: null,
      };
      this.isEditMode = false;
      this.showModal = true;
    },
    openEditModal(animal) {
      this.currentAnimal = { ...animal };
      this.isEditMode = true;
      this.showModal = true;
    },
    async saveAnimal() {
      if (!this.currentAnimal.name || !this.currentAnimal.inventory_number) {
        console.error("Ошибка: Необходимо указать имя и номер инвентаря животного.");
        return;
      }

      try {
        if (this.isEditMode) {
          await axios.put(`/api/animals/${this.currentAnimal.id}`, {
            inventory_number: this.currentAnimal.inventory_number,
            gender: this.currentAnimal.gender,
            name: this.currentAnimal.name,
            arrival_date: this.currentAnimal.arrival_date,
            age_months: this.currentAnimal.age_months,
            breed_id: this.currentAnimal.breed_id,
            parent_id: this.currentAnimal.parent_id,
          });
          console.log("Животное успешно отредактировано.");
        } else {
          await axios.post('/api/animals', {
            inventory_number: this.currentAnimal.inventory_number,
            gender: this.currentAnimal.gender,
            name: this.currentAnimal.name,
            arrival_date: this.currentAnimal.arrival_date,
            age_months: this.currentAnimal.age_months,
            breed_id: this.currentAnimal.breed_id,
            parent_id: this.currentAnimal.parent_id,
          });
          console.log("Животное успешно добавлено.");
        }
        await this.fetchAnimals();
        this.closeModal();
      } catch (error) {
        console.error("Ошибка при сохранении данных о животном:", error.response ? error.response.data : error.message);
      }
    },
    async deleteAnimal(id) {
      if (confirm("Вы уверены, что хотите удалить это животное?")) {
        try {
          await axios.delete(`/api/animals/${id}`);
          console.log("Животное успешно удалено.");
          await this.fetchAnimals();
        } catch (error) {
          console.error("Ошибка при удалении животного:", error.response ? error.response.data : error.message);
        }
      }
    },
    closeModal() {
      this.showModal = false;
      this.currentAnimal = {
        id: null,
        inventory_number: "",
        gender: "",
        name: "",
        arrival_date: "",
        age_months: 0,
        breed_id: null,
        parent_id: null,
      };
    },
  }
};
</script>

<style scoped>
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
