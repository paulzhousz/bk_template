<template>
<div class="monitor_panel">
  <el-row :gutter="20" type="flex" class="row-bg" justify="space-between">
    <el-col :span="12">
      <div class="grid-content bg-purple">任务统计</div>
    </el-col>
    <el-col :span="12">
      <div class="grid-content bg-purple-light">性能状态</div>
    </el-col>
  </el-row>
  <el-row :gutter="20" type="flex" class="row_middle" justify="space-between">
    <el-col :span="12">
      <div id="task_pic"></div>
    </el-col>
    <el-col :span="12">
      <div class="right_pic">
        <div class="choose_server">
          <span>服务器：</span>
          <el-select size="mini" v-model="server" @change="serverChange" :placeholder="defaultServer">
            <el-option
              v-for="(item, index) in optionsServer"
              :key="index"
              :label="item.ip"
              :value="item.id">
            </el-option>
          </el-select>
        </div>
        <div id="cpu_pic"></div>
      </div>
    </el-col>
  </el-row>
  <el-row type="flex" class="row_end">
    <el-col :span="12"></el-col>
  </el-row>
</div>
</template>

<script>
export default {
  data() {
    return {
      server: '',
      serverId: 1,
      defaultServer: '',
      optionsServer: [],
    }
  },
  mounted() {
    this.initTaskChart()
    this.getServerData()
    this.initCpuChart()
    this.setTime()
  },
  methods: {
    // 初始化任务饼图
    async initTaskChart() {
      // 基于准备好的dom，开始初始化任务饼图
      let taskChart = this.$echarts.init(document.getElementById('task_pic'));
      let option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          type: 'scroll',
          orient: 'vertical',
          right: 10,
          top: 20,
          bottom: 20,
        },
      }
      taskChart.setOption(option);
      let dataName = {
        waitting: '等待中',
        running: '运行中',
        success: '已成功',
        fail: '已失败'
      }
      taskChart.showLoading()
      await this.$store.dispatch('pie/getTaskState').then(res => {
        if (res.result) {
          let data = [];
          Object.keys(res.data).forEach((i) => {
            Object.keys(dataName).forEach(j => {
              if (i == j) {
                data.push({
                  name: dataName[j],
                  value: res.data[i]
                })
              }
            })
          })
          taskChart.setOption(
            {
              series: [
                {
                  name: '任务状态',
                  type: 'pie',
                  color: ['#fa541c', '#fadb14', '#a0d911', '#1890ff'],
                  radius: ['30%', '70%'],
                  data: data,
                  itemStyle: {
                    emphasis: {
                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                  }
                }
              ]
            }
          );
        }
      })
      taskChart.hideLoading()
      // 浏览器放大或缩小时无需刷新图表自动随页面的大小而变化
      window.onresize = function() {
        taskChart.resize()
      }
    },
    // 获取服务器数据
    getServerData() {
      this.$store.dispatch('pie/getServerSelect').then(res => {
        if (res.result) {
          this.optionsServer = res.data
          this.defaultServer = this.optionsServer[1].ip
        }
      })
    },
    // 下拉框数据发生改变时触发
    serverChange(val) {
      this.serverId = val
      this.initCpuChart(val)
    },
    // 初始化cpu折线图
    async initCpuChart() {
      let cpuChart = this.$echarts.init(document.getElementById('cpu_pic'))
      let params = {
        id: this.serverId
      }
      let data = []
      let cpuData = []
      let memoryData = []
      cpuChart.showLoading({ text: '正在努力加载数据...' })
      await this.$store.dispatch('pie/getServerPerformance', params).then(res => {
        if (res.result) {
          data = res.data.map(item => item.product)
          cpuData = res.data.map(item => item.cpu)
          memoryData = res.data.map(item => item.mem)
          let option = {
            title: {
              // text: 'Cpu、内存使用率'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: ['CPU', '内存']
            },
            xAxis: {
              type: 'category',
              data: data
            },
            yAxis: {
              type: 'value',
              min: 0
            },
            series: [
              {
                name: 'CPU',
                color: '#fa541c',
                data: cpuData,
                type: 'line',
                smooth: true
              },
              {
                name: '内存',
                data: memoryData,
                color: '#a0d911',
                type: 'line',
                smooth: true
              },
            ]
          }
          cpuChart.setOption(option)
        }
      })
      cpuChart.hideLoading()
      // 浏览器放大或缩小时无需刷新图表自动随页面的大小而变化
      window.onresize = function() {
        cpuChart.resize()
      }
    },
    // 定时器
    setTime() {
      var app = {};
      app.timeTicket = setInterval(() => { //定时刷新图表
        this.initCpuChart();
      }, 3000);
    }
  }
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
      #task_pic {
        height: 100%;
        background: #fff;
      }
      .right_pic {
        height: 100%;
        background: #fff;
        .choose_server {
          line-height: 50px;
          padding-right: 20px;
          text-align: right;
        }
        #cpu_pic {
          width: 100%;
          height: calc(100% - 50px);
        }
      }
    }
    .row_end {
      margin-top: 8px;
      height: calc((100% - 56px)/2);
      background: #fff;
    }
  }
</style>
