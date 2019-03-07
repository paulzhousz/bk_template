<template>
    <div id="user-manage">
        <div class="op-nav">
            <div class="search">
                <el-input placeholder="请输入内容" v-model="condition.value" size="small" class="input-with-select">
                    <el-select v-model="condition.select" slot="prepend" placeholder="请选择">
                        <el-option label="名称" value="name"></el-option>
                    </el-select>
                    <el-button @click="search()" slot="append" icon="el-icon-search"></el-button>
                </el-input>
            </div>
            <div class="operator">
                <el-button type="primary" size="small" @click="create_operator()">添加</el-button>
            </div>
        </div>
        <div class="content" v-loading="loading">
            <el-table :data="userList" border size="small">
                <el-table-column type="index" label="序号" width="80"></el-table-column>
                <el-table-column prop="name" label="姓名" width="180"></el-table-column>
                <el-table-column prop="account" label="账号"></el-table-column>
                <el-table-column prop="email" label="邮箱"></el-table-column>
                <el-table-column prop="age" label="年龄"></el-table-column>
                <el-table-column prop="sex" label="性别"></el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button
                            size="mini"
                            type="primary" plain
                            @click="edit_operator(scope.$index, scope.row)">编辑
                        </el-button>
                        <el-button
                            size="mini"
                            type="danger" plain
                            @click="del(scope.$index, scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <UserOperator :showDialogData="showUserDialog" @save="save"></UserOperator>
    </div>
</template>

<script>
    import UserOperator from '@/pages/userControllers/userOperator'

    export default {
        name: 'userManage',
        components: {
            UserOperator
        },
        data() {
            return {
                condition: {
                    select: '',
                    value: ''
                },
                loading: false,
                userList: [],
                showUserDialog: {
                    is_show: false,
                    operator: '',
                    title: '',
                    data: {}
                }
            }
        },
        mounted() {
            this.search();
        },
        methods: {
            search() {
                this.loading = true;
                this.$http.post('search_user', this.condition).then(res => {
                    this.loading = false;
                    if (res.result) {
                        this.userList = res.data;
                    }
                })
            },
            create_operator() {
                this.showUserDialog.is_show = true;
                this.showUserDialog.operator = 'add';
                this.showUserDialog.title = '添加用户';
                this.showUserDialog.data = {}
            },
            edit_operator(index, row) {
                this.showUserDialog.is_show = true;
                this.showUserDialog.operator = 'edit';
                this.showUserDialog.title = '修改用户';
                this.showUserDialog.index = index;
                this.showUserDialog.data = JSON.parse(JSON.stringify(row))
            },
            save(item) {
                if (item.operator === 'add') {
                    this.userList.push(item.data)
                }
                if (item.operator === 'edit') {
                    this.userList.splice(item.index, 1, item.data)
                }
            },
            del(index, row) {
                this.$confirm('此操作将永久删除, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$http.post('delete_user?id=' + row.id, {}).then(res => {
                        if (res.result) {
                            this.userList.splice(index, 1);
                            this.$message({
                                showClose: true,
                                message: '删除成功',
                                type: 'success'
                            });
                        } else {
                            this.$message({
                                showClose: true,
                                message: res.message,
                                type: 'error'
                            });
                        }
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            }
        }
    }
</script>

<style lang="scss" scoped>
    #user-manage {
        height: 100%;
        box-sizing: border-box;
        padding: 10px;
        .op-nav {
            height: 60px;
            line-height: 60px;
            .search {
                width: 300px;
                float: left;
                .el-select {
                    width: 90px;
                }
            }
            .operator {
                width: 300px;
                float: right;
                text-align: right;
            }
        }
        .content {
            background: #fff;
            height: 100%;
            margin: auto;
        }
    }
</style>
