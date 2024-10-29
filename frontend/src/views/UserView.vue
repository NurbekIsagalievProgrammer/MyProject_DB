<template>
  <div>
    <h1>Пользователи</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Логин</th>
          <th>Статус</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.is_active ? 'Активен' : 'Не активен' }}</td>
          <td>
            <button @click="toggleUserStatus(user)">
              {{ user.is_active ? 'Деактивировать' : 'Активировать' }}
            </button>
          </td>
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
      users: []
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
   
    async fetchUsers() {
      try {
        const response = await axios.get('/api/users');
        this.users = response.data.users;
      } catch (error) {
        console.error("Ошибка при получении данных о пользователях:", error);
      }
    },
   
    async toggleUserStatus(user) {
      try {
        await axios.patch(`/api/users/${user.id}/toggle-status`);
        user.is_active = !user.is_active;
      } catch (error) {
        console.error("Ошибка при изменении статуса пользователя:", error);
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
  border: 1px solid #dddddd;
  padding: 8px;
}
th {
  background-color: blue;
}
</style>
