<template>
  <div class="user">
    <div class="search">
      <el-autocomplete
        v-model="stateUser"
        :fetch-suggestions="querySearchAsync"
        placeholder="请输入用户名"
        @select="handleSelect">
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
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'

export default {
  components: {
    Pagination
  },
  data() {
    return {
      loadingUser: false,
      dataUser: [],
      allUserName: [],
      allUser: [],
      stateUser: '',
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
    getUser() {
      let params = {
        page: this.currentPage,
        page_size: this.pageSize
      }
      this.$store.dispatch('user/getTableUser').then(res => {
        if (res.result) {
          this.totalNumber = res.data.count
          this.dataUser = res.data.items
        }
      })
    },
    pageSizeChange(val) {
      this.currentPage = val.currentPage
      this.pageSize = val.pageSize
      this.getUser({page: this.currentPage, page_size: this.pageSize})
    },
    handleNewUser() {},
    handleEdit(scope) {},
    checkboxChange(scope) {},
    handleDelete(scope) {},
    handleSelect(item) {
      for (let i in this.allUserName) {
        if (this.allUserName[i].display_name == item.value) {
          // return
        }
      }
      console.log(item)
    },
    search() {
      this.allUserName = []
      this.$store.dispatch('group/getAllUser').then(res => {
        if (res.result) {
          for (let i of res.data) {
            this.allUserName.push({
              value: i.display_name
            })
          }
          this.allUser = res.data
        }
      })
    },
    querySearchAsync(queryString, cb) {
      let allUserName = this.allUserName;
      let results = queryString ? allUserName.filter(this.createStateFilter(queryString)) : allUserName;
      cb(results)
    },
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
