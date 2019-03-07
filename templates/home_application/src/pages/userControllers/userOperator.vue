<template>
    <el-dialog :title='showDialogData.title' :visible="showDialogData.is_show" width="30%" center>
        <div class="dialog-content">
            <el-form ref="form" :model="showDialogData.data" label-width="80px" size="small">
                <el-form-item label="名称：">
                    <el-input v-model="showDialogData.data.name"></el-input>
                </el-form-item>
                <el-form-item label="账号：">
                    <el-input v-model="showDialogData.data.account"></el-input>
                </el-form-item>
                <el-form-item label="密码：">
                    <el-input v-model="showDialogData.data.password" type="password"></el-input>
                </el-form-item>
                <el-form-item label="邮箱：">
                    <el-input v-model="showDialogData.data.email"></el-input>
                </el-form-item>
                <el-form-item label="性别：">
                    <el-radio-group v-model="showDialogData.data.sex">
                        <el-radio label="女" value="0"></el-radio>
                        <el-radio label="男" vlaue="1"></el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>
        </div>
        <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="confirm()" size="small">保存</el-button>
            <el-button @click="cancel()" size="small">取 消</el-button>
        </span>
    </el-dialog>
</template>

<script>
    export default {
        name: 'userOperator',
        props: {
            showDialogData: {
                is_show: false
            }
        },
        methods: {
            cancel() {
                this.showDialogData.is_show = false;
            },
            confirm() {
                if (this.showDialogData.operator === 'add') {
                    this.add();
                }
                if (this.showDialogData.operator === 'edit') {
                    this.edit();
                }
                this.showDialogData.is_show = false;
            },
            add() {
                this.$http.post('create_user', this.showDialogData.data).then(res => {
                    if (res.result) {
                        this.showDialogData.data.id = res.data.id;
                        this.$emit('save', this.showDialogData);
                        this.$message({
                            showClose: true,
                            message: '添加成功',
                            type: 'success'
                        });
                    } else {
                        this.$message({
                            showClose: true,
                            message: res.message,
                            type: 'error'
                        });
                    }
                });
            },
            edit() {
                this.$http.post('update_user', this.showDialogData.data).then(res => {
                    if (res.result) {
                        this.$emit('save', this.showDialogData);
                        this.$message({
                            showClose: true,
                            message: '保存成功',
                            type: 'success'
                        });
                    } else {
                        this.$message({
                            showClose: true,
                            message: res.message,
                            type: 'error'
                        });
                    }
                });
            }
        }
    }
</script>

<style lang="scss" scoped>
    .dialog-content {
        text-align: left;
        width: 100%;
        margin: auto;
    }
</style>
