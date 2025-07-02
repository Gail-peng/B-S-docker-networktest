<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button @click="fetchHello">点击获取后端消息</button>
    <p v-if="backendMsg" class="result">后端返回：{{ backendMsg }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: 'Vue2 前端',
      backendMsg: ''  // 存储后端返回的消息
    }
  },
  methods: {
    fetchHello() {
      axios.get('back/hello')
        .then(response => {
          this.backendMsg = response.data.message
        })
        .catch(error => {
          console.error('请求失败：', error)
          this.backendMsg = '请求失败，请查看控制台'
        })
    }
  }
}
</script>

<style scoped>
.result {
  color: green;
  margin-top: 20px;
  font-size: 18px;
}

button {
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
}
</style>