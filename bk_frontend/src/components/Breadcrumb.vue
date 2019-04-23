<template>
  <div id="bread-crumb">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item
        v-for="(item, index) in to"
        :key="index"
        :to="{ path: item.path }">
        {{item.displayName}}
      </el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>
<script>
/**
 * breadcrumb
 * @desc 面包屑组件
 * @param to {Array} 面包屑数据对象
 * @example <breadcrumb :to="to"></breadcrumb>
 */
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
    cursor: pointer;
  }
  .el-breadcrumb {
    font-size: 14px;
    line-height: 1.8;
    cursor: pointer;
}
</style>
