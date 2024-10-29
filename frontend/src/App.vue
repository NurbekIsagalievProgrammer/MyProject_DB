<template>
  <div id="app">
    <h1>Система для работы с таблицами</h1>
    <nav>
      <ul>
        <li><router-link to="/animaltypes">Типы Животных</router-link></li>
        <li><router-link to="/breeds">Породы</router-link></li>
        <li><router-link to="/animals">Животные</router-link></li>
        <li><router-link to="/weightings">Весовые данные</router-link></li>
        <li><router-link to="/users">Пользователи</router-link></li>
      </ul>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
nav {
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline;
  margin-right: 15px;
}
</style>
