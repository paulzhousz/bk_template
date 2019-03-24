<template>
<div class="authority">
  <breadcrumb :to="to"></breadcrumb>
  <div class="contain"></div>
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
      to: [
        {displayName: '系统管理', path: {path: ''}},
        {displayName: '用户管理', path: {path: '/authority'}},
      ]
    }
  }
}
</script>

<style lang="scss">
  .authority {
    .contain {
      width: 100%;
      height: 100%;
      // height: calc(100% - 80px);
      background: #fff;
    }
  }
</style>
