<template>
  <div>
    <h1>Пользователи</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Имя пользователя</th>
          <th>Email</th>
          <th>Статус</th>
          <th>Тип пользователя</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.is_active ? 'Активен' : 'Не активен' }}</td>
          <td>{{ user.user_type }}</td>
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
