<template>
<div class="group">
  <breadcrumb :to="to"></breadcrumb>
  <div class="contain">
    <div class="search">
      <el-row>
        <el-col :span="8">
          <!-- <div class="grid-content"></div> -->
          <span class="aglin">角色名：</span>
          <el-input class="aglin-input" size="mini" v-model="inputGroup" placeholder="请输入内容"></el-input>
        </el-col>
        <el-col :span="8">
          <!-- <div class="grid-content"></div> -->
          <span class="aglin">是否内置：</span>
          <el-checkbox v-model="checkedIsBuilt" :true-label="1" :false-label="0"></el-checkbox>
        </el-col>
        <el-col :span="8">
          <span class="aglin">是否启用：</span>
          <el-checkbox v-model="checkedIsEnable" :true-label="1" :false-label="0"></el-checkbox>
          <!-- <div class="grid-content"></div> -->
        </el-col>
      </el-row>
    </div>
  </div>
</div>
</template>

<script>
import Breadcrumb from '@/components/Breadcrumb'
export default {
  components: {
    Breadcrumb
  },
  data() {
    return {
      inputGroup: '',
      checkedIsBuilt: 0,
      checkedIsEnable: 0,
      to: [
        {displayName: '系统管理', path: {path: ''}},
        {displayName: '角色管理', path: {path: '/group'}},
      ]
    }
  }
}
</script>

<style lang="scss">
  .group {
    padding: 20px;
    height: 100%;
    width: 100%;
    .contain {
      height: calc(100% - 40px);
      background: #fff;
      .search {
        .aglin {
          .el-input__inner {
            display: inline-block;
            width: 80% !important;
          }
        }
      }
    }
  }
</style>
