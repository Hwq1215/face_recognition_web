<template>


    <el-button class="btn-add" @click="handleAdd()">
        <el-icon><Plus /></el-icon>
    </el-button>
    <el-table 
    :data="facesData" 
    >
    
        <el-table-column type="expand">
            <template #default="scope">
            <img class="face-img" :src="scope.src"/>
            </template>
        </el-table-column>
        <el-table-column prop="index" label="" width="300" type="index">
        </el-table-column>
        <el-table-column prop="name" label="姓名" width="400"></el-table-column>
        <el-table-column prop="fake" label="欺诈识别" width="400"></el-table-column>
        <el-table-column  label="操作">
            <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
            >编辑</el-button
            >
            <el-button
                size="small"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)"
                >删除</el-button
            >
            </template>
        </el-table-column>
    </el-table>
    <div class="page-item">
        
        <el-pagination
        :page-size="14"
        :pager-count="5"
        background
        layout="prev, pager, next"
        :total="total"
        class="mt-4"
    />
    </div>
    <!-- 更新面板 -->
    <el-dialog v-model="EditDialogIsVisiable" title="修改">
        <el-form>
            <el-form-item label="姓名">
                <el-input v-model="chooseItem.name"></el-input>
            </el-form-item>
            <el-form-item label="图片">
                <div @click="HandleImgSelect()" class="input-img">
                    <img v-if="chooseItem.imgSrc" :src="chooseItem.imgSrc" >
                    <el-icon size="20" v-else><Picture/></el-icon>
                </div>
                <div style="margin-top: 0px; margin-left: 20px;" >
                    <input @change="showImg($event)" ref="inputImg" class="input-hiden" hidden type="file"/><br>
                    <el-button type="success" @click="handleUpdate()">录制<el-icon size="17"><VideoCameraFilled /></el-icon></el-button>
                </div>
                
                </el-form-item>
            <el-form-item>
                    <el-button type="primary" @click="handleUpdate()">确认</el-button>
                    <el-button type="danger" @click="EditDialogIsVisiable = false">取消</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
</template>

<script>
import {getFacesData,getFacesTotal,deleteFaceData} from "@/api/getData";
import { extend } from "@vue/shared";
import { Plus,Picture as IconPicture, Picture, Upload} from '@element-plus/icons-vue'
import {httpurl} from "@/config"
import axios from "axios";
    export default{
    data() {
        return {
            total: 100,
            currentPage: 1,
            EditDialogIsVisiable: false,
            ADDDialogIsVisiable: false,
            imageUrl: "",
            chooseItem: {
                faceId: 0,
                name: "",
                fake: "",
                imgSrc: "",
                files: undefined
            },
            facesData: [
                {
                    name: "张三",
                    fake: "是"
                },
                {
                    name: "李四",
                    fake: "否"
                }
            ]
        };
    },
    components:{
        Plus,
        IconPicture
    },
    init() {
        this.getFacesTotal();
        this.HandlePageSelect(1);
    },
    watch: {
        currentPage(val) {
            this.HandlePageSelect(val);
        }
    },
    methods: {
        handlePageSelect(currentPage) {
            this.getFacesInPage(currentPage);
        },
        handleEdit(index,row){
            this.factoryChooseItem(row);
            this.EditDialogIsVisiable = true;
        },
        handleUpdate(){
            this.UploadFaceData();
        },
        handleDelete(index,row){
            this.deleteFaceData(row.faceId);
        },
        handleAdd(){
            this.initChooseItem();
            this.EditDialogIsVisiable = true;
        },
        handleInsert(){
            this.addFaceData();
        },
        async getFacesTotal() {
            this.total = await getFacesTotal();
        },
        async getFacesInPage(currentpage) {
            this.facesData = await getFacesData(currentpage);
        },
        async deleteFaceData(faceId){
            await deleteFaceData(faceId);
            this.getFacesTotal();
            this.HandlePageSelect(this.currentPage);
        },
        initChooseItem(){
            this.chooseItem = {
                faceId: 0,
                name: "",
                fake: "",
                imgSrc: "",
                files: undefined
            };
        },
        factoryChooseItem(row){
            this.chooseItem = {
                faceId: row.faceId,
                name: row.name,
                fake: row.fake,
                imgSrc: row.imgSrc,
                files: undefined
            };
        },
        showImg(e) {
            let that = this;//改变this指向
            let files = e.target.files[0];//图片文件名
            if (!e || !window.FileReader) return; // 看是否支持FileReader
            let reader = new FileReader();
            reader.readAsDataURL(files); // 关键一步，在这里转换的
            reader.onloadend = function () {
                that.chooseItem.imgSrc = this.result;//赋值
                that.chooseItem.files = files;
            }
        //     let param = new FormData(); //转换为表单进行发送给后端
        //     param.append("imgFile", files); //第一个参数就是后端要接受的字段，要一样，不一样会发送失败
        //     Axios.post(this.$api.ip,param).then((data)=>{
        //         console.log(data);
        // })
        },
        UploadFaceData(){
            try{
                let fd = new FormData(); //转换为表单进行发送给后端
                fd.append('faceId',this.chooseItem.faceId)
                fd.append('name',this.chooseItem.name)
                fd.append("imgFile", this.chooseItem.files); //第一个参数就是后端要接受的字段，要一样，不一样会发送失败
                axios({
                    method:'post',
                    url:this.httpurl+'/manage/upload',
                    headers:{'Content-Type':'multipart/form-data',
                            "Access-Control-Allow-Origin": "*"},
                    data:fd,
                }).then((res)=>{
                    if(res.status == 200){
                        this.$message({
                            message: '上传成功',
                            type: 'success'
                        });
                        this.facesData.find((item)=>{
                        if(item.faceId == this.chooseItem.faceId){
                            item.name = this.chooseItem.name;
                            item.imgSrc = this.chooseItem.imgSrc;
                        }
                    })
                    }
                })
            }
            finally{
                this.EditDialogIsVisiable = false;
                this.initChooseItem();
            }
        },
        HandleImgSelect(){
            this.$refs.inputImg.click();
        },
        }
    }
</script>

<style>
    .page-item{
        text-align: center;
        height: 33px;
        background-color: white;
        display: flex;
    }
    .page-item .el-pagination{
        max-width: 500px;
    }
    .btn-add{
        text-align: center;
        width: 100%;
        height: 100px;
        background-color: #409EFF;
        color: white;
        border: none;
        font-size: small;
        border-radius: 5px;
        
    }
    .avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
    .input-img{
        width: 200px;
        height: 200px;
        border: 1px solid #dcdfe6;
        border-radius: 6px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .input-img img{
        max-width: 200px;
        max-height: 200px;
    }
    .input-img .el-icon{
        font-size: 50px;
    }
    .input-hiden{
       margin-left: 30px;
    }

</style>
