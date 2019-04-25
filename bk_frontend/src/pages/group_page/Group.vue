<template>
  <div class="group">
    <div class="search">
      <el-row>
        <el-col :span="6">
          <span class="aglin">角色名：</span>
          <el-input class="aglin-input" size="mini" v-model="inputGroup" clearable placeholder="请输入内容"></el-input>
        </el-col>
        <el-col :span="6">
          <span class="aglin">是否内置：</span>
          <el-select size="mini" v-model="valueIsBuiltIn" clearable placeholder="请选择">
            <el-option
              v-for="(item, index) in optionsIsBuiltIn"
              :key="index"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <span class="aglin">是否启用：</span>
          <el-select size="mini" v-model="valueIsEnable" clearable placeholder="请选择">
            <el-option
              v-for="(item, index) in optionsIsEnable"
              :key="index"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button size="mini" type="primary" @click.native="search">查询</el-button>
          <el-button size="mini" @click.native="reset">重置</el-button>
        </el-col>
      </el-row>
    </div>
    <div class="new">
      <el-button size="mini" type="primary" @click="handleNew">新建角色</el-button>
    </div>
    <div class="table">
      <el-table
        stripe
        ref=""
        :data="data"
        v-loading="loadingGroup"
        style="width: 100%"
        height="100%">
        <el-table-column
        prop="name"
        label="组名"
        show-overflow-tooltip>
        </el-table-column>
        <el-table-column
        prop="display_name"
        label="显示名"
        show-overflow-tooltip>
        </el-table-column>
        <el-table-column
        label="是否内置">
          <template slot-scope="scope">
            <span>{{scope.is_built_in == false ? '否' : '是'}}</span>
          </template>
        </el-table-column>
        <el-table-column
        label="是否启用">
          <template slot-scope="scope">
            <el-checkbox
            v-model="scope.row.is_enable"
            @change="checkboxChange(scope.row)">
            </el-checkbox>
          </template>
        </el-table-column>
        <el-table-column
        prop="description"
        label="描述"
        show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="handle"
          label="操作"
          fixed="right"
          width="150">
          <template slot-scope="scope">
            <el-button type="text" @click="handleEdit(scope)">编辑</el-button>
            <el-button type="text" @click="handleAuthority({name: 'permission', params: {group_id: scope.row.id}})">权限</el-button>
            <el-button type="text" @click="handleDelete(scope)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <pagination
      :total="totalNumber"
      @page-size-change="pageSizeChange">
    </pagination>
    <new-edit ref="newEdit" :title="title" @handle-success="handleSuccess" dialog-action="dialogAction" :width="width">
      <div slot="dialog-content">
        <el-tabs v-model="activeName" :before-leave="leaveTab">
          <el-tab-pane label="角色信息" name="first">
            <el-form ref="refformGroups" :label-position="labelPosition" label-width="120px" :model="formGroups" :rules="rulesGroups">
              <el-form-item label="组名" prop="name">
                <el-input class="form-content" size="mini" v-model="formGroups.name"></el-input>
              </el-form-item>
              <el-form-item label="显示名" prop="display_name">
                <el-input class="form-content" size="mini" v-model="formGroups.display_name"></el-input>
              </el-form-item>
              <el-form-item label="描述">
                <el-input class="form-content" type="textarea" v-model="formGroups.desc"></el-input>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="分配用户" name="second">
            <div>
              <el-row>
                <el-col :span="10">
                  <el-table
                    :data="leftData"
                    border
                    v-loading="loadingLeft"
                    height="280"
                    style="width: 100%;margin-bottom: 0px"
                    @selection-change="handleLeftChange"
                    :row-class-name="leftRow">
                    <el-table-column type="selection" prop="value"></el-table-column>
                    <el-table-column prop="username" label="用户名"></el-table-column>
                    <el-table-column prop="chname" label="中文名" show-overflow-tooltip></el-table-column>
                  </el-table>
                </el-col>
                <el-col :span="4">
                  <div style="margin-top: 100%;margin-left:25%;margin-right:25%">
                    <el-button v-if="leftButtonColor" size="mini" type="primary" @click="turnRightItems" icon="icon el-icon-d-arrow-right"></el-button>
                    <el-button v-if="!leftButtonColor" type="info" disabled size="mini" icon="icon el-icon-d-arrow-right"></el-button>
                    <el-button v-if="rightButtonColor" style="margin: 5px 0 0 0" size="mini" type="primary" @click="turnLeftItems" icon="icon el-icon-d-arrow-left"></el-button>
                    <el-button v-if="!rightButtonColor" type="info" disabled class="not-have" style="margin: 5px 0 0 0" size="mini" icon="icon el-icon-d-arrow-left"></el-button>
                  </div>
                </el-col>
                <el-col :span="10">
                  <el-table
                    :data="rightData"
                    height="280"
                    v-loading="loadingRight"
                    style="width: 100%;margin-bottom: 0px"
                    border
                    @selection-change="handleRightChange"
                    :row-class-name="rightRow">
                    <el-table-column type="selection" prop="value"></el-table-column>
                    <el-table-column label="用户名" prop="username"></el-table-column>
                    <el-table-column prop="chname" label="中文名" show-overflow-tooltip></el-table-column>
                  </el-table>
                </el-col>
              </el-row>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </new-edit>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import NewEdit from '@/components/NewEdit'
import * as commonValidate from '@/common/js/validate'
import * as commonMethods from '@/common/js/common'

export default {
  components: {
    'pagination': Pagination,
    'new-edit': NewEdit,
  },
  data() {
    return {
      inputGroup: '',
      title: '',
      dialogAction: '',
      activeName: 'first',
      width: '40%',
      valueIsBuiltIn: undefined,
      valueIsEnable: undefined,
      labelPosition: 'right',
      totalNumber: 0,
      currentPage: 1,
      pageSize: 10,
      loadingGroup: false,
      loadingLeft: false,
      loadingRight: false,
      cacheLeftData: [], // 左侧缓存数据
      cacheRightData: [], // 右侧缓存数据
      data: [],
      leftData: [],
      rightData: [],
      formGroups: {
        name: '',
        display_name: '',
        users: [],
        desc: '',
      },
      rulesGroups: {
        name: [
          { required: true, message: '请输入组名' },
          { max: 20, message: '长度在20个字符之内' },
          { validator: commonValidate.validateNameUnderline }
        ],
        display_name: [
          { required: true, message: '请输入显示名' },
          { max: 14, message: '长度在14个字符之内' },
          { validator: commonValidate.validateChName }
        ],
      },
      optionsIsBuiltIn: [
        {value: true, label: '是'},
        {value: false, label: '否'},
      ],
      optionsIsEnable: [
        {value: true, label: '是'},
        {value: false, label: '否'},
      ],
    }
  },
  created() {
    this.search()
  },
  methods: {
    search() {
      let params = {
        page: this.currentPage,
        page_size: this.pageSize,
        is_built_in: this.valueIsBuiltIn,
        is_enable: this.valueIsEnable,
        display_name: this.inputGroup,
        omit: 'menus,permissions'
      }
      this.loadingGroup = true
      this.$store.dispatch('group/getGroups', params).then(res => {
        if (res.result) {
          this.loadingGroup = false
          this.data = res.data.items
          this.totalNumber = res.data.count
        }
      })
    },
    pageSizeChange(val) {
      this.currentPage = val.currentPage
      this.pageSize = val.pageSize
      this.search({page: this.currentPage, page_size: this.pageSize})
    },
    reset() {
      this.inputGroup = ''
      this.valueIsBuiltIn = undefined
      this.valueIsEnable = undefined
      this.search()
    },
    handleEdit(scope) {
      this.activeName = 'first'
      this.dialogAction = 'edit'
      this.title = '编辑'
      this.$refs['newEdit'].open()
      this.formGroups = JSON.parse(JSON.stringify(scope.row))
      this.formGroups.users = this.formGroups.users.map(item => item.id)
      this.rightData = scope.row.users
      this.leftData = []
      this.getLeftUser()
    },
    leaveTab(val) {
      let res = true
      this.$refs.refformGroups.validate((valid) => {
        if (!valid) {
          res = false
        } else {
          res = true
        }
      })
      return res
    },
    handleNew() {
      this.activeName = 'first'
      this.dialogAction = 'new'
      this.title = '新建'
      this.$refs['newEdit'].open()
      this.$nextTick(() => {
        this.$refs['refformGroups'].clearValidate()
      })
      this.leftData = []
      this.rightData = []
      this.getLeftUser()
      this.formGroups = {}
    },
    checkboxChange(row) {
      let tipEnable = row.is_enable ? '是否启用' : '是否禁用'
      this.$confirm(tipEnable, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (row.is_enable == true) {
          let params = {
            groups: [row.id],
            enable: true
          }
          this.$store.dispatch('group/groupsStatus', params).then(res => {
            if (res.result) {
              this.$message({type: 'success', message: '禁用成功'})
            } else {
              row.is_enable = !row.is_enable
              this.$message({type: 'error', message: '禁用失败'})
            }
          });
        } else if (row.is_enable == false) {
          let params = {
            groups: [row.id],
            enable: false
          }
          this.$store.dispatch('group/groupsStatus', params).then(res => {
            if (res.result) {
              this.$message({type: 'success', message: '启用成功'})
            } else {
              row.is_enable = !row.is_enable
              this.$message({type: 'error', message: '启用失败'})
            }
          });
        }
      }).catch(() => {
        row.is_enable = !row.is_enable
        this.$message({type: 'info', message: '调取接口失败'})
      })
    },
    handleAuthority(data) {
      this.$router.push(data)
    },
    handleSuccess(dialogAction) {
      if (this.dialogAction == 'new') {
        let params = {
          name: this.formGroups.name,
          description: this.formGroups.desc,
          users: this.formGroups.users
        }
        this.$store.dispatch('group/addGroups', params).then(res => {
          if (res.result) {
            this.search()
            this.$message({type: 'success', message: '新建成功'})
          } else {
            this.$message({type: 'error', message: '新建失败'})
          }
        }).catch(() => {
          this.$message({type: 'info', message: '接口调用失败'})
        })
      } else if (this.dialogAction == 'edit') {
        this.rightDataId = this.rightData.map(item => item.id)
        this.formGroups.users = this.rightDataId
        let params = this.formGroups
        this.$store.dispatch('group/editGroups', params).then(res => {
          if (res.result) {
            this.search()
            this.$message({type: 'success', message: '编辑成功'})
          } else {
            this.$message({type: 'error', message: '编辑失败'})
          }
        }).catch(() => {
          this.$message({type: 'info', message: '接口调用失败'})
        })
      }
      this.$refs['newEdit'].cancel()
    },
    handleDelete(scope) {
      this.$confirm('此操作将永久删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let params = {
          id: scope.row.id
        }
        this.$store.dispatch('group/deleteGroups', params).then(res => {
          if (res.result) {
            this.search()
            this.$message({type: 'success', message: '删除成功'})
          } else {
            this.$message({type: 'error', message: '删除失败'})
          }
        })
      }).catch(() => {
        this.$message({type: 'info', message: '已取消'})
      })
    },
    // 左侧所有用户数据
    getLeftUser() {
      this.$store.dispatch('group/getAllUser').then(res => {
        if (res.result) {
          if (this.dialogAction == 'new') {
            this.leftData = res.data
          } else if (this.dialogAction == 'edit') {
            this.leftData = res.data.filter((item) => {
              for (let i of this.rightData) {
                if (item.id == i.id) {
                  return false
                }
              }
              return true
            })
          }
        }
      })
    },
    // 向右侧添加数据
    turnRightItems() {
      // 合并左侧选中数据和右侧数据
      this.rightData.push.apply(this.rightData, this.cacheLeftData)
      // 删除左侧勾选数据\
      let indexLeft = 0
      for (let i of this.cacheLeftData) {
        this.leftData.splice(i.rowIndex - indexLeft, 1)
        indexLeft++
      }
      this.cacheLeftData = []
    },
    // 向左侧添加数据
    turnLeftItems() {
      // 合并左侧选中数据和右侧数据
      this.leftData.push.apply(this.leftData, this.cacheRightData)
      // 删除右侧勾选数据
      let indexRight = 0
      for (let i of this.cacheRightData) {
        this.rightData.splice(i.indexRight - indexRight, 1)
        indexRight++
      }
      this.cacheRightData = []
    },
    // 左侧选择项发生变化
    handleLeftChange(val) {
      this.cacheLeftData = val
    },
    // 右侧选择项发生变化
    handleRightChange(val) {
      this.cacheRightData = val
    },
    // 左侧表格的每行数据对象中加入索引字段
    leftRow({row, rowIndex}) {
      row.rowIndex = rowIndex
    },
    // 右侧表格的每行数据对象中加入索引字段
    rightRow({row, rowIndex}) {
      row.rowIndex = rowIndex
    },
  },
  computed: {
    leftButtonColor() {
      if (this.leftData.length == 0) {
        return false
      } else {
        return true
      }
    },
    rightButtonColor() {
      if (this.rightData.length == 0) {
        return false
      } else {
        return true
      }
    },
  },
}
</script>

<style lang="scss">
  .group {
    height: 100%;
    padding: 15px 20px 0 20px;
    background: #fff;
      .search {
        height: 50px;
        line-height: 50px;
        .aglin-input {
          width: 60%;
        }
      }
      // /*
      .new {
        height: 40px;
      }
      // */
      .table {
        height: calc(100% - 130px);
        .el-table {
          border-top: 1px solid rgb(235, 238, 245);
        }
      }
  }
</style>
