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
      <el-button size="mini" type="primary" @click="handleNewUser">新建用户</el-button>
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
            <el-button type="text" @click="handleEdit(scope)">编辑</el-button>
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
          <!-- <el-form-item label="描述">
            <el-input class="form-content" type="textarea" v-model="formGroups.desc"></el-input>
          </el-form-item> -->
        </el-form>
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
      dataUser: [],
      allUserName: [],
      allUser: [],
      formUser: {
        username: '',
        phone: '',
        email: '',
      },
      rulesUser: {},
      userDetail: [],
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
      this.formUser = {}
      this.dialogAction = 'new'
      this.title = '新建'
      this.$refs['newEdit'].open()
    },
    handleEdit(scope) {
      this.dialogAction = 'edit'
      this.title = '编辑'
      this.$refs['newEdit'].open()
      this.formUser = JSON.parse(JSON.stringify(scope.row))
    },
    handleSuccess(dialogAction) {
      if (this.dialogAction == 'new') {} else if (this.dialogAction == 'edit') {}
    },
    checkboxChange(scope) {},
    handleDelete(scope) {},
    // 关键字提醒后点击某一关键字后操作
    handleSelect(item) {
      this.getUser({chname: item.value})
    },
    handleSelectDialog(item) {
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
            })
          }
          this.allUser = res.data
        }
      })
    },
    // 匹配输入字符
    querySearchDetail(queryString, cb) {
      let userDetail = this.userDetail;
      let results = queryString ? userDetail.filter(this.createStateFilterDetail(queryString)) : userDetail;
      cb(results)
    },
    // 匹配位置
    createStateFilterDetail(queryString) {
      return (usernameDetail) => {
        return (usernameDetail.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    // 匹配输入字符
    querySearchAsync(queryString, cb) {
      let allUserName = this.allUserName;
      let results = queryString ? allUserName.filter(this.createStateFilter(queryString)) : allUserName;
      cb(results)
    },
    // 匹配位置
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
  }
</style>
