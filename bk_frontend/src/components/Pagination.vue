<template>
  <div id="pagination">
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 50, 100]"
      :pager-count="pager"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total">
    </el-pagination>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        currentPage: 1, //默认显示第一页
        pageSize: 10, //默认每页显示10条
        pager: 5 //页码按钮的数量，当总页数超过该值时会折叠
      }
    },
    props: {
      total: Number
    },
    methods: {
      /* @param    val           点击几条一页
       * @param    pageSize      每页显示条目个数，将用户选择的条目数赋值给pageSize
       * @param    currentPage   当前页码
       */
      handleSizeChange(val) { // pageSize 改变时会触发
        this.pageSize = val
        this.$emit('page-size-change', {pageSize: this.pageSize, currentPage: this.currentPage})
      },
      /* @param    val           点击的第几页
       * @param    pageSize      每页显示条目个数
       * @param    currentPage   当前页码，将用户点击的页码赋值给currentPage
       */
      handleCurrentChange(val) { // currentPage改变时会触发
        this.currentPage = val
        this.$emit('page-size-change', {pageSize: this.pageSize, currentPage: this.currentPage})
      }
    },
  }
</script>
<style>
  #pagination {
    width: 77%;
    height: 40px;
    position: absolute;
    bottom: 20px;
    text-align: right
  }
</style>
