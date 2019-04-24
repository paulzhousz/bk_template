<template>
  <div class='new'>
    <el-button type="primary">主要按钮</el-button>
  </div>
</template>
<script>

export default {
  data() {
    return {
    }
  },
  created() {
    this.inntCharts()
  },
  methods: {
    inntCharts() {
      // 基于准备好的dom，初始化echarts实例
      let myCharts = this.$echarts.init(document.getElementById('self_chart'));
      // 指定图表的配置项和数据
      let option = {
        title: {
          text: 'ECharts 入门示例'
        },
        tooltip: {},
        legend: {
          data: ['销量']
        },
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        },
        yAxis: {},
        series: [{
          name: '销量',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }]
      };
      // 使用刚指定的配置项和数据显示图表。
      myCharts.setOption(option);
    }
  },
}
</script>
<style lang='scss'>
.new {
  height: 100%;
  padding: 15px 20px 0 20px;
  background: #fff;
  #self_chart {
    width: 500px;
    height: 500px;
  }
}
</style>
