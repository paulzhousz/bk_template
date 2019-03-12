<template>
  <div id="bread-crumb">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item
      v-for="(item, index) in to"
      :key="index"
      :to="item.path">
      {{item.displayName}}
      </el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>
<script>
  export default {
    props: { // 接收父组件中的每个面包屑对象
      to: {
        type: Array,
        default: () => []
      }
    }
  }
</script>
<style scoped>
  #bread-crumb {
    width: 95%;
    height: 30px;
    padding-left: 20px;
  }
  .el-breadcrumb {
    font-size: 16px;
    line-height: 1.8;
}
</style>
