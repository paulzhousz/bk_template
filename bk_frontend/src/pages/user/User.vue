<template>
<div class="user">
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
  .user {
    padding: 20px;
    height: 100%;
    width: 100%;
    .contain {
      height: 100%;
      background: #fff;
    }
  }
</style>
