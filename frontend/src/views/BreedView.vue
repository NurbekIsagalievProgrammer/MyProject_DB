<template>
  <div>
    <h1>Породы животных</h1>
    <button @click="openAddModal">+</button>

    <!-- Таблица пород животных -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Название</th>
          <th>ID Типа Животного</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="breed in breeds" :key="breed.id">
          <td>{{ breed.id }}</td>
          <td>{{ breed.name }}</td>
          <td>{{ breed.animaltype_id }}</td>
          <td>
            <button @click="openEditModal(breed)">Редактировать</button>
            <button @click="deleteBreed(breed.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно для добавления/редактирования -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ isEditMode ? "Редактировать породу" : "Добавить породу" }}</h2>
        <input type="text" v-model="currentBreed.name" placeholder="Название породы" />
        
        <!-- Выпадающий список для выбора типа животного -->
        <select v-model="currentBreed.animaltype_id">
          <option v-for="type in types" :key="type.id" :value="type.id">
            {{ type.id }} - {{ type.name }}
          </option>
        </select>
        
        <button @click="saveBreed">{{ isEditMode ? "Сохранить" : "Добавить" }}</button>
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
      breeds: [],
      types: [],
      showModal: false,
      isEditMode: false,
      currentBreed: { id: null, name: "", animaltype_id: null },
    };
  },
  mounted() {
    this.fetchBreeds();
    this.fetchAnimalTypes();
  },
  methods: {
    // Получение данных о породах животных
    async fetchBreeds() {
      try {
        const response = await axios.get('/api/breeds');
        console.log("Данные о породах:", response.data); // Для отладки
        this.breeds = response.data.breeds || [];
      } catch (error) {
        console.error("Ошибка при получении данных о породах животных:", error);
      }
    },
    
    // Получение данных о типах животных
    async fetchAnimalTypes() {
      try {
        const response = await axios.get('/api/animaltypes');
        this.types = response.data.animal_types || []; // Убедитесь, что данные приходят в нужном формате
      } catch (error) {
        console.error("Ошибка при получении данных о типах животных:", error);
      }
    },

    // Открытие модального окна для добавления породы
    openAddModal() {
      this.currentBreed = { id: null, name: "", animaltype_id: null };
      this.isEditMode = false;
      this.showModal = true;
    },

    // Открытие модального окна для редактирования породы
    openEditModal(breed) {
      this.currentBreed = { ...breed };
      this.isEditMode = true;
      this.showModal = true;
    },

    // Добавление или редактирование породы животного
    async saveBreed() {
      if (!this.currentBreed.name) {
        console.error("Ошибка: Название породы не может быть пустым.");
        return;
      }

      try {
        if (this.isEditMode) {
          await axios.put(`/api/breeds/${this.currentBreed.id}`, {
            name: this.currentBreed.name,
            animaltype_id: this.currentBreed.animaltype_id,
          });
          console.log("Порода успешно отредактирована.");
        } else {
          await axios.post('/api/breeds', {
            name: this.currentBreed.name,
            animaltype_id: this.currentBreed.animaltype_id,
          });
          console.log("Порода успешно добавлена.");
        }
        await this.fetchBreeds();
        this.closeModal();
      } catch (error) {
        console.error("Ошибка при сохранении породы:", error);
      }
    },

    // Удаление породы
    async deleteBreed(id) {
      try {
        await axios.delete(`/api/breeds/${id}`);
        console.log("Порода успешно удалена.");
        await this.fetchBreeds();
      } catch (error) {
        console.error("Ошибка при удалении породы:", error);
      }
    },

    // Закрытие модального окна
    closeModal() {
      this.showModal = false;
      this.currentBreed = { id: null, name: "", animaltype_id: null };
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
