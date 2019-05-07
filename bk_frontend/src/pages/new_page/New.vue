<template>
  <div class="new">
    <div class="button_layout">
      <el-row>
        <el-button type="primary">主要按钮</el-button>
        <el-button plain type="success">成功按钮</el-button>
        <el-button round type="warning">警告按钮</el-button>
      </el-row>
      <el-row style="margin-top: 20px;">
        <el-button type="primary" @click="popover">主要按钮</el-button>
        <el-button type="success">成功按钮</el-button>
        <el-button type="info">信息按钮</el-button>
      </el-row>
    </div>
    <div class="table_layout">
      <el-table
        :data="tableData"
        height="100%"
        style="width: 100%">
        <el-table-column
          prop="username"
          label="用户名">
        </el-table-column>
        <el-table-column
          prop="chname"
          label="中文名">
        </el-table-column>
        <el-table-column
          prop="phone"
          label="姓名">
        </el-table-column>
        <el-table-column
          prop="id"
          label="用户ID">
        </el-table-column>
        <el-table-column
          prop="email"
          label="邮箱">
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
import * as commonApi from '@/api/api.js'

export default {
  data() {
    return {
      tableData: [],
      webSocket: null
    }
  },
  created() {
    this.getData()
    this.initWebSocket()
  },
  destroyed() {
    this.websocketclose()
  },
  methods: {
    popover() {
      // alert('jinx真棒')
      commonApi.getTest().then(res => {
      // this.$axios.get('test/').then(res => {
        if (res.result) {
          console.log(res.data)
        }
      })
    },
    getData() {
      commonApi.getTableData().then(res => {
        if (res.result) {
          this.tableData = res.data
        }
      })
    },
    // 初始化ws
    initWebSocket() {
      let wsurl = window.siteUrl.replace('http', 'ws') + 'api/monitor/mocks/websocket/demo/'
      // let wsurl = 'ws://127.0.0.1:8001/api/monitor/mocks/websocket/demo/'
      this.webSocket = new WebSocket(wsurl)
      // websocket建立时的回调函数
      this.webSocket.onopen = this.websocketonopen
      // 获取服务器传递的数据的回调函数
      this.webSocket.onmessage = this.websocketonmessage
      // 获取websocket关闭时的回调函数
      this.webSocket.onclose = this.websocketonclose
    },
    websocketonopen() {
      // 客户端发送数据到后端
      this.webSocket.send('{"task_id": 1}')
    },
    websocketonmessage(e) {
      console.log(e.data)
    },
    websocketonclose() {
      console.log('websocket closed')
    },
    // 关闭websocket
    websocketclose() {
      console.log('close websocket')
      this.webSocket.close()
    }
  },
}
</script>
<style lang="scss">
.new {
  height: 100%;
  .button_layout {
    height: 120px;
  }
  .table_layout {
    height: calc(100% - 120px);
    .el-table {
      height: 100%;
    }
  }
}
</style>
