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
          <div class="one-layer" v-for="(item, index) in allOperations" :key="index" :label="item">
            {{item}}
            <!-- <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox> -->
            <el-checkbox-group v-model="checkedOperations" @change="handleCheckedOperationsChange">
              <el-checkbox v-for="(itemOperation, indexOperations) in item.operations" :label="itemOperation" :key="indexOperations">
                {{itemOperation}}
              </el-checkbox>
            </el-checkbox-group>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeName: 'second',
      dataMenuTree: [],
      haveMenuAuthority: [],
      checkeditem: [], // 勾选的操作
      allOperations: [], // 所有操作
      operations: [], // 第二层级下的所有操作
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
    // 权限树状数据
    getPerm() {
      this.allOperations = []
      this.operations = []
      this.$store.dispatch('perm/getPermsTree').then(res => {
        if (res.result) {
          for (let i of res.data) {
            this.allOperations.push(i.display_name)
            if (i.children.length !== 0) {
              // for (let j of i.children) {
              //   this.operations.push(j.display_name)
              // }
              this.operations = i.children.map(item => item.display_name)
            }
          }
        }
      })
    },
    handleCheckedOperationsChange() {},
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
      .one-layer {
        padding: 20px;
      }
    }
  }
</style>
