<template>
  <div class="dialog">
    <el-dialog
      :title="title"
      :visible.sync="isShow"
      :width="width">
      <slot name="dialog-content"></slot>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="confirm" size="mini">确 定</el-button>
        <el-button @click="cancel" size="mini">取 消</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: ''
    },
    width: {
      type: String,
      default: ''
    },
    dialogAction: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      isShow: false,
    }
  },
  methods: {
    open() {
      this.isShow = true
    },
    confirm() {
      this.$emit('handle-success', this.dialogAction)
    },
    cancel() {
      this.isShow = false
    },
  }
}
</script>

<style lang="scss">
</style>
