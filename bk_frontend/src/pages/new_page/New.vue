<template>
  <div>
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
    <!-- <el-table
      :data="tableData"
      border
      style="width: 100%">
      <el-table-column
        fixed
        prop="date"
        label="日期"
        width="150">
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
        width="120">
      </el-table-column>
      <el-table-column
        prop="province"
        label="省份"
        width="120">
      </el-table-column>
      <el-table-column
        prop="city"
        label="市区"
        width="120">
      </el-table-column>
      <el-table-column
        prop="address"
        label="地址"
        width="300">
      </el-table-column>
      <el-table-column
        prop="zip"
        label="邮编"
        width="120">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="100">
        <template slot-scope="scope">
          <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
          <el-button type="text" size="small">编辑</el-button>
        </template>
      </el-table-column>
    </el-table> -->
  </div>
</template>
<script>
// import * as commonApi from '@/api/api.js'

export default {
  methods: {
    popover() {
      // alert('jinx真棒')
      // commonApi.getTest().then(res => {
      this.$axios.get('test/').then(res => {
        if (res.result) {
          console.log(res.data)
        }
      })
    }
  },
}
</script>
<style lang="scss">
</style>
