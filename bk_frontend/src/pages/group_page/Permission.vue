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
        <el-tab-pane label="操作权限" name="second">
          <div class="one-layer" v-for="(item, index) in allOperations" :key="index">
            <span class="one-layer-name">{{item.display_name}}</span>
            <el-checkbox
            v-for="(itemOperation, indexOperations) in item.children"
            :key="indexOperations"
            v-model="itemOperation.has_perms">
              {{itemOperation.display_name}}
            </el-checkbox>
          </div>
        </el-tab-pane>
        <div class="check-confirm">
          <el-button type="primary" size="mini" @click="checkConfirm">保存</el-button>
        </div>
      </el-tabs>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      checked: [],
      activeName: 'first',
      dataMenuTree: [],
      haveMenuAuthority: [],
      checkeditem: [], // 勾选的操作
      allOperations: [], // 所有操作
      defaultMenuProps: {
        children: 'children',
        label: 'display_name'
      },
    }
  },
  created() {
    this.menuAuthority()
    this.getPerm()
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
      return this.$store.dispatch('group/getAuthority', params).then(res => {
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
    // 操作权限数据
    getPerm() {
      this.allOperations = []
      let param = {id: this.$route.params.group_id}
      this.$store.dispatch('group/getPermsTree', param).then(res => {
        if (res.result) {
          this.allOperations = res.data
        }
      })
    },
    // 确认操作权限
    checkConfirm() {
      // 菜单权限id数组
      let menuList = this.$refs.tree.getCheckedNodes()
      menuList = menuList.map(item => item.id)
      // 操作功能权限id数组
      let permIdList = []
      for (let i of this.allOperations) {
        if (i.children.length !== 0) {
          for (let j of i.children) {
            if (j.has_perms == true) {
              permIdList.push(j.id)
            }
          }
        }
      }
      let params = {
        id: this.$route.params.group_id,
        permissions: permIdList,
        menus: menuList,
      }
      this.$store.dispatch('group/editGroups', params).then(res => {
        if (res.result) {
          this.$message({type: 'success', message: '权限设置成功'})
        } else {
          this.getPerm()
          this.$message({type: 'error', message: '权限设置失败'})
        }
      })
    }
  }
}
</script>

<style lang="scss">
  .permission {
    height: 100%;
    width: 100%;
    .contain {
      height: 100%;
      padding: 15px 20px 0 20px;
      background: #fff;
      .check-confirm {
        padding: 20px;
        position: absolute;
        bottom: 0;
      }
      .el-tabs.el-tabs--top {
        height: 100%;
        .el-tabs__content {
          height: calc(100% - 55px);
          .el-tab-pane {
            height: 100%;
            .one-layer {
              padding: 20px;
              border-bottom: 1px solid #f1eded;
              .one-layer-name {
                display: block;
                font-size: 1.5em;
                margin-bottom: 20px;
              }
            }
          }
        }
      }
    }
  }
</style>
