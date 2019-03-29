<template>
  <div class="group">
    <div class="contain">
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
          <!-- <el-table-column
          type="selection"
          width="30">
          </el-table-column> -->
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
          <el-form ref="formGroups" :label-position="labelPosition" label-width="120px" :model="formGroups" :rules="rulesGroups">
            <el-form-item label="组名" prop="name">
              <el-input class="form-content" size="mini" v-model="formGroups.name"></el-input>
            </el-form-item>
            <el-form-item label="显示名" prop="display_name">
              <el-input class="form-content" size="mini" v-model="formGroups.display_name"></el-input>
            </el-form-item>
            <el-form-item label="用户成员" prop="users">
              <el-select class="form-content" v-model="formGroups.users" multiple placeholder="请选择">
                <el-option
                  v-for="(item, index) in optionsUsers"
                  :key="index"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="描述">
              <el-input class="form-content" type="textarea" v-model="formGroups.desc"></el-input>
            </el-form-item>
          </el-form>
        </div>
      </new-edit>
    </div>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import NewEdit from '@/components/NewEdit'
import * as commonValidate from '@/common/js/validate'
import * as commonMethods from '@/common/js/common'

export default {
  components: {
    Pagination,
    NewEdit,
  },
  data() {
    return {
      inputGroup: '',
      title: '',
      dialogAction: '',
      activeName: 'first',
      width: '30%',
      valueIsBuiltIn: undefined,
      valueIsEnable: undefined,
      labelPosition: 'right',
      totalNumber: 0,
      currentPage: 1,
      pageSize: 10,
      loadingGroup: false,
      data: [],
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
      optionsUsers: [],
      dataMenuTree: [], // 菜单全部树形数据
      haveMenuAuthority: [], // 当前用户已有的菜单权限
      defaultMenuProps: {
        children: 'children',
        label: 'display_name'
      }
    }
  },
  created() {
    this.search()
    this.getGroup()
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
    getGroup() {
      this.$store.dispatch('group/getUserSelect').then(res => {
        if (res.result) {
          this.optionsUsers = res.data
        }
      })
    },
    handleEdit(scope) {
      this.dialogAction = 'edit'
      this.title = '编辑'
      this.$refs['newEdit'].open()
        // this.$refs['formGroups'].clearValidate()
      this.formGroups = JSON.parse(JSON.stringify(scope.row))
      this.formGroups.users = this.formGroups.users.map(item => item.id)
      // this.formGroups.users = []
      // for (let i of scope.row.users) {
      //   this.formGroups.users.push(i.id)
      // }
    },
    handleNew() {
      this.dialogAction = 'new'
      this.title = '新建'
      this.formGroups = {users: []}
      this.$refs['newEdit'].open()
      this.$nextTick(() => {
        this.$refs['formGroups'].clearValidate()
      })
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
              this.$message({type: 'success', message: res.message})
            } else {
              row.is_enable = !row.is_enable
              this.$message({type: 'error', message: res.message})
            }
          });
        } else if (row.is_enable == false) {
          let params = {
            groups: [row.id],
            enable: false
          }
          this.$store.dispatch('group/groupsStatus', params).then(res => {
            if (res.result) {
              this.$message({type: 'success', message: res.message})
            } else {
              row.is_enable = !row.is_enable
              this.$message({type: 'error', message: res.message})
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
            this.$message({type: 'success', message: res.message})
          } else {
            this.$message({type: 'error', message: res.message})
          }
        }).catch(() => {
          this.$message({type: 'info', message: '接口调用失败'})
        })
      } else if (this.dialogAction == 'edit') {
        let params = this.formGroups
        this.$store.dispatch('group/editGroups', params).then(res => {
          if (res.result) {
            this.$message({type: 'success', message: res.message})
          } else {
            this.$message({type: 'error', message: res.message})
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
            this.$message({type: 'success', message: res.message})
          } else {
            this.$message({type: 'error', message: res.message})
          }
        })
      }).catch(() => {
        this.$message({type: 'info', message: '已取消'})
      })
    },
  },
}
</script>

<style lang="scss">
  .group {
    height: calc(100% - 55px);
    width: 100%;
    .contain {
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
      .new {
        height: 40px;
      }
      .table {
        height: calc(100% - 130px);
        .el-table {
          border-top: 1px solid rgb(235, 238, 245);
        }
      }
    }
  }
</style>
