<template>
  <div>
    <h1>Типы животных</h1>
    <button @click="openAddModal">+</button>

    <!-- Таблица типов животных -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Название</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="animal_type in animal_types" :key="animal_type.id">
          <td>{{ animal_type.id }}</td>
          <td>{{ animal_type.name }}</td>
          <td>
            <button @click="openEditModal(animal_type)">Редактировать</button>
            <button @click="deleteAnimalType(animal_type.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно для добавления/редактирования -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ isEditMode ? "Редактировать тип животного" : "Добавить тип животного" }}</h2>
        <input type="text" v-model="currentAnimalType.name" placeholder="Название" />
        <button @click="saveAnimalType">{{ isEditMode ? "Сохранить" : "Добавить" }}</button>
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
      animal_types: [],
      showModal: false,
      isEditMode: false,
      currentAnimalType: { id: null, name: "" },
    };
  },
  mounted() {
    this.fetchAnimalTypes();
  },
  methods: {
    
    async fetchAnimalTypes() {
      try {
        const response = await axios.get('/api/animaltypes');
        this.animal_types = response.data.animal_types || []; 
      } catch (error) {
        console.error("Ошибка при получении данных о типах животных:", error);
      }
    },

    
    openAddModal() {
      this.currentAnimalType = { id: null, name: "" };
      this.isEditMode = false;
      this.showModal = true;
    },

    
    openEditModal(animal_type) {
      this.currentAnimalType = { ...animal_type };
      this.isEditMode = true;
      this.showModal = true;
    },

    
    async saveAnimalType() {
      if (!this.currentAnimalType.name) {
        console.error("Ошибка: Название типа животного не может быть пустым.");
        return;
      }
      
      try {
        if (this.isEditMode) {
          await axios.put(`/api/animaltypes/${this.currentAnimalType.id}`, {
            name: this.currentAnimalType.name,
          });
          console.log("Тип животного успешно отредактирован.");
        } else {
          await axios.post('/api/animaltypes', {
            name: this.currentAnimalType.name,
          });
          console.log("Тип животного успешно добавлен.");
        }
        await this.fetchAnimalTypes();
        this.closeModal();
      } catch (error) {
        console.error("Ошибка при сохранении типа животного:", error);
      }
    },

   
    async deleteAnimalType(id) {
      try {
        await axios.delete(`/api/animaltypes/${id}`);
        console.log("Тип животного успешно удален.");
        await this.fetchAnimalTypes();
      } catch (error) {
        console.error("Ошибка при удалении типа животного:", error);
      }
    },

   
    closeModal() {
      this.showModal = false;
      this.currentAnimalType = { id: null, name: "" };
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
