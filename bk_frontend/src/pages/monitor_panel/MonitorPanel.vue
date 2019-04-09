<template>
<div class="monitor_panel">
  <el-row :gutter="20" type="flex" class="row-bg" justify="space-between">
    <el-col :span="12">
      <div class="grid-content bg-purple">任务统计</div>
    </el-col>
    <el-col :span="12">
      <div class="grid-content bg-purple-light">CPU状态</div>
    </el-col>
  </el-row>
  <el-row :gutter="20" type="flex" class="row_middle" justify="space-between">
    <el-col :span="12">
      <div class="task_pic">任务统计</div>
    </el-col>
    <el-col :span="12">
      <div class="cpu_pic">CPU状态</div>
    </el-col>
  </el-row>
  <el-row type="flex" class="row_end">
    <el-col :span="12"></el-col>
  </el-row>
</div>
</template>

<script>
export default {
}
</script>

<style lang="scss">
  .monitor_panel {
    height: 100%;
    padding: 0 20px 0 20px;
    .row-bg {
      height: 40px;
      font-size: 1.2em;
      color: rgb(134, 134, 125);
      font-weight: 550;
      text-align: center;
      .grid-content.bg-purple {
        background: #fff;
        line-height: 40px;
      }
      .grid-content.bg-purple-light {
        background: #fff;
        line-height: 40px;
      }
    }
    .row_middle {
      height: calc((100% - 56px)/2);
      margin-top: 8px;
      .task_pic {
        height: 100%;
        background: #fff;
      }
      .cpu_pic {
        height: 100%;
        background: #fff;
      }
    }
    .row_end {
      margin-top: 8px;
      height: calc((100% - 56px)/2);
      background: #fff;
    }
  }
</style>
