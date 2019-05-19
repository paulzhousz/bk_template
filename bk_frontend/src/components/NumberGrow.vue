<template>
  <span ref="numberGrow" :data-time="time" class="number-grow" :data-value="value">{{value}}</span>
</template>
<script>
export default {
  props: {
    time: {
      type: Number,
      default: 2
    },
    value: {
      type: Number,
      default: 10
    }
  },
  methods: {
    numberGrow () {
      let _this = this
      let step = (_this.value * 10) / (_this.time * 1000)
      let start = 0
      let t = setInterval(function () {
        start += step
        if (start > _this.value) {
          clearInterval(t)
          start = _this.value
          t = null
        }
        _this.$el.innerHTML = parseInt(start)
      }, 10)
    }
  },
  watch: {
    value (newValue, oldValue) {
      this.numberGrow()
    }
  }
}
</script>
