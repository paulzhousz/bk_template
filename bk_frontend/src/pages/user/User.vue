<template>
  <div class="user">
    <div class="search">
      <el-autocomplete
        v-model="stateUser"
        :fetch-suggestions="querySearchAsync"
        placeholder="请输入用户名"
        @select="handleSelect"
        clearable>
      </el-autocomplete>
    </div>
    <div class="new">
      <el-button size="mini" type="primary" @click="handleNewUser">添加用户</el-button>
    </div>
    <div class="table">
      <el-table
        stripe
        ref=""
        :data="dataUser"
        v-loading="loadingUser"
        style="width: 100%"
        height="100%">
        <!-- <el-table-column
        type="selection"
        width="30">
        </el-table-column> -->
        <el-table-column
        prop="username"
        label="用户名"
        show-overflow-tooltip>
        </el-table-column>
        <el-table-column
        prop="chname"
        label="中文名"
        show-overflow-tooltip>
        </el-table-column>
        <el-table-column
        prop="phone"
        label="电话"
        show-overflow-tooltip>
        </el-table-column>
        <el-table-column
        prop="email"
        label="邮箱"
        show-overflow-tooltip>
        </el-table-column>
        <el-table-column
        prop="groups"
        label="所属角色"
        show-overflow-tooltip>
          <template slot-scope="scope">
            <span>{{scope.row.groups | arrayFormat}}</span>
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
          prop="handle"
          label="操作"
          fixed="right"
          width="100">
          <template slot-scope="scope">
            <el-button type="text" @click="handleAuthority(scope)">权限</el-button>
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
      <div slot="dialog-content" v-if="showForm">
        <el-form ref="formUser" :label-position="labelPosition" label-width="120px" :model="formUser" :rules="rulesUser">
          <el-form-item label="用户名" prop="name">
            <el-autocomplete
              clearable
              size="small"
              class="inline-input"
              v-model="formUser.username"
              :fetch-suggestions="querySearchDetail"
              placeholder="请输入用户名"
              @select="handleSelectDialog">
            </el-autocomplete>
          </el-form-item>
          <el-form-item label="电话" prop="phone">
            <span class="form-content">{{formUser.phone}}</span>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <span class="form-content">{{formUser.email}}</span>
          </el-form-item>
        </el-form>
      </div>
      <div slot="dialog-content" v-if="!showForm">
        <div class="label-position" v-for="(item, index) in userAuthorityList" :key="index">
          <span class="label-position-content">{{item.display_name}}</span>
          <div></div>
        </div>
      </div>
    </new-edit>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import NewEdit from '@/components/NewEdit'

export default {
  components: {
    'pagination': Pagination,
    'new-edit': NewEdit,
  },
  data() {
    return {
      loadingUser: false,
      showForm: true,
      dataUser: [],
      allUserName: [],
      allUser: [],
      formUser: {
        username: '',
        phone: '',
        email: '',
      },
      userID: '',
      rulesUser: {},
      userDetail: [],
      userAuthorityList: [],
      stateUser: '',
      title: '',
      width: '35%',
      labelPosition: '120px',
      totalNumber: 0,
      currentPage: 1,
      pageSize: 10,
    }
  },
  created() {
    this.getUser()
    this.search()
  },
  methods: {
    // 获取用户页面表格数据
    getUser(apiParam) {
      let params = {
        page: this.currentPage,
        page_size: this.pageSize,
      }
      params = Object.assign(params, apiParam)
      this.$store.dispatch('user/getTableUser', params).then(res => {
        if (res.result) {
          this.totalNumber = res.data.count
          this.dataUser = res.data.items
        }
      })
    },
    // 表格分页
    pageSizeChange(val) {
      this.currentPage = val.currentPage
      this.pageSize = val.pageSize
      this.getUser({page: this.currentPage, page_size: this.pageSize})
    },
    handleNewUser() {
      this.showForm = true
      this.formUser = {}
      this.dialogAction = 'new'
      this.title = '新建'
      this.$refs['newEdit'].open()
    },
    handleAuthority(scope) {
      this.showForm = false
      this.title = '权限管理'
      this.$refs['newEdit'].open()
      let params = {
        id: scope.row.id
      }
      this.$store.dispatch('user/getUserAuthority', params).then(res => {
        if (res.result) {
          this.userAuthorityList = res.data
        }
      })
    },
    handleSuccess() {
      let params = {
        id: this.userID
      }
      this.$store.dispatch('user/addUser', params).then(res => {
        if (res.result) {
          this.getUser()
          this.$message({type: 'success', message: '添加用户成功'})
        } else {
          this.$message({type: 'error', message: '添加用户失败'})
        }
      })
      this.$refs['newEdit'].cancel()
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
            users: [row.id],
            enable: true
          }
          this.$store.dispatch('user/usersStatus', params).then(res => {
            if (res.result) {
              this.$message({type: 'success', message: res.message})
            } else {
              row.is_enable = !row.is_enable
              this.$message({type: 'error', message: res.message})
            }
          });
        } else if (row.is_enable == false) {
          let params = {
            users: [row.id],
            enable: false
          }
          this.$store.dispatch('user/usersStatus', params).then(res => {
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
    handleDelete(scope) {
      this.$confirm('此操作将永久删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let params = {
          id: scope.row.id
        }
        this.$store.dispatch('user/deleteUser', params).then(res => {
          if (res.result) {
            this.getUser()
            this.$message({type: 'success', message: '删除用户成功'})
          } else {
            this.$message({type: 'error', message: '删除用户失败'})
          }
        })
      }).catch(() => {
        this.$message({type: 'info', message: '已取消'})
      })
    },
    // 关键字提醒后点击某一关键字后操作
    handleSelect(item) {
      this.getUser({chname: item.value})
    },
    handleSelectDialog(item) {
      this.userID = item.id
      this.formUser.phone = item.phone
      this.formUser.email = item.email
    },
    // 获取所有用户（用于关键字提醒）
    search() {
      this.allUserName = []
      this.$store.dispatch('group/getAllUser').then(res => {
        if (res.result) {
          for (let i of res.data) {
            this.allUserName.push({
              value: i.chname
            })
            this.userDetail.push({
              value: i.chname,
              phone: i.phone,
              email: i.email,
              id: i.id,
            })
          }
          this.allUser = res.data
        }
      })
    },
    // 添加用户时用户输入匹配输入字符
    querySearchDetail(queryString, cb) {
      let userDetail = this.userDetail;
      let results = queryString ? userDetail.filter(this.createStateFilterDetail(queryString)) : userDetail;
      cb(results)
    },
    // 添加用户时用户输入匹配位置
    createStateFilterDetail(queryString) {
      return (usernameDetail) => {
        return (usernameDetail.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    // 表格页匹配输入字符
    querySearchAsync(queryString, cb) {
      let allUserName = this.allUserName;
      let results = queryString ? allUserName.filter(this.createStateFilter(queryString)) : allUserName;
      cb(results)
    },
    // 表格页匹配位置
    createStateFilter(queryString) {
      return (username) => {
        return (username.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
  },
}
</script>

<style lang="scss">
  .user {
    height: 100%;
    padding: 15px 20px 0 20px;
    background: #fff;
    .search {
      line-height: 100px;
      text-align: center;
      .el-autocomplete {
        width: 65%;
      }
    }
    .new {
      height: 40px;
    }
    .table {
      height: calc(100% - 180px);
      .el-table {
        border-top: 1px solid rgb(235, 238, 245);
      }
    }
    .label-position {
      margin: 0 0 15px 0;
      .label-position-content {
        // float: left;
        width: 80px;
      }
    }
  }
</style>
