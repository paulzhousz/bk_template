<template>
  <div class="permission">
    <div class="contain">
      <el-tabs v-model="activeName" >
        <el-tab-pane label="菜单权限" name="first">
          <el-tree
            :data="dataMenuTree"
            show-checkbox
            default-expand-all
            node-key="id"
            ref="tree"
            highlight-current
            :default-checked-keys="haveMenuAuthority"
            :props="defaultMenuProps">
          </el-tree>
        </el-tab-pane>
        <el-tab-pane label="操作权限" name="second"></el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeName: 'first',
      dataMenuTree: [],
      haveMenuAuthority: [],
      defaultMenuProps: {
        children: 'children',
        label: 'display_name'
      },
    }
  },
  created() {
    this.menuAuthority()
  },
  methods: {
    // 所有菜单数据
    allMenu() {
      this.dataMenuTree = []
      return this.$store.dispatch('leftmenu/getMenuTree').then(res => {
        if (res.result) {
          this.dataMenuTree = res.data
        }
      })
    },
    // 已有菜单权限
    haveMenu() {
      this.haveMenuAuthority = []
      let params = {
        id: this.$route.params.group_id
      }
      return this.$store.dispatch('group/getMenuAuthority', params).then(res => {
        if (res.result) {
          this.haveMenuAuthority = res.data.menus.map(item => item.id)
        }
      })
    },
    // 树状菜单数据
    async menuAuthority(id) {
      await Promise.all([
        this.allMenu(),
        this.haveMenu(id)
      ])
    },
  }
}
</script>

<style lang="scss">
  .permission {
    height: calc(100% - 55px);
    width: 100%;
    .contain {
      height: 100%;
      padding: 15px 20px 0 20px;
      background: #fff;
    }
  }
</style>
