<template>
    <el-row gutter="2">
        <el-col :span="22" :offset="1" > 
    <el-card class="box-card">
        <h3><center>人脸信息</center></h3>  
    <el-table 
    :data="facesData" 
    style="margin: 0;"
    >
    
        <el-table-column type="expand">
            <template #default="scope">
            <img class="face-img" :src="scope.src"/>
            </template>
        </el-table-column>
        <el-table-column prop="index" label="" width="350" type="index">
        </el-table-column>
        <el-table-column prop="name" label="姓名" width="350"></el-table-column>
        <!-- <el-table-column prop="fake" label="欺诈识别" width="400"></el-table-column> -->
        <el-table-column  label="操作" width="700">
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
    <el-button class="btn-add" @click="handleAdd()">
        <el-icon><Plus /></el-icon>
    </el-button>
    <div class="page-item">
        
        <el-pagination
        :page-size="pageSize"
        :pager-count="5"
        v-model:current-page="currentPage"
        background
        layout="prev, pager, next"
        :total="total"
        class="mt-4"
    />
    </div>
    </el-card>
        </el-col>
    </el-row >
    <el-row gutter="2" style="margin-top: 50px;">
        <el-col :span="22" :offset="1">
            <el-card>
                <h3><center>欺诈记录</center></h3>  
                <el-table
                :data="fakeData"
                >
                <el-table-column prop="index" label="" width="250" type="index">
                </el-table-column>
                <el-table-column prop="name" label="识别姓名" width="250"></el-table-column>
                <el-table-column prop="time" label="时间" width="250"></el-table-column>
                <el-table-column prop="fake" label="欺诈类型" width="250"></el-table-column>
                <el-table-column prop="imgSrc" label="欺诈图片" width="250">
                    <template #default="scope">
                        <el-button type="text" @click="handleImg(scope.$index, scope.row)">查看</el-button>
                    </template>
                </el-table-column>
                </el-table>
        <div class="page-item">
            <el-pagination
            :page-size="pageSize"
            :pager-count="5"
            background
            layout="prev, pager, next"
            :total="2"
            class="mt-4"
        />
        </div>  
            </el-card>

        </el-col>

    </el-row>
    
    <!-- 更新面板 -->
    <el-dialog v-model="DialogIsVisiable" :title="editChoose?'修改':'上传'">
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
                    <input @change="showImgEvent($event)"  ref="inputImg" class="input-hiden" hidden type="file"/><br>
                    <el-button type="success" @click="handleVideo()">录制<el-icon size="17"><VideoCameraFilled /></el-icon></el-button>
                </div>
                                </el-form-item>
            <el-form-item >
                    <el-button v-if="editChoose" type="primary" @click="updateFaceData()">确认</el-button>
                    <el-button v-else type="primary" @click="addFaceData()">确认</el-button>
                    <el-button type="danger" @click="DialogIsVisiable = false">取消</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>

    <el-dialog v-model="VideoDialogIsVisiable">
    <video-reader @choose-img="getVideoImg()" ref="reader"></video-reader>
    </el-dialog>
</template>

<script>
import {getFacesData,getFacesTotal,deleteFaceData} from "@/api/getData";
import { Plus,Picture as IconPicture, Picture, Upload, Refresh} from '@element-plus/icons-vue'
import VideoReader from "@/components/VideoReader.vue"
import {httpurl} from "@/config"
import axios from "axios";

    export default{
    data() {
        return {
            total: 100,
            currentPage: 1,
            DialogIsVisiable: false,
            VideoDialogIsVisiable: false,
            editChoose: true,
            imageUrl: "",
            pageSize: 7,
            reFresh : true,
            chooseItem: {
                faceId: 0,
                name: "",
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
            ],
            fakeData:[
                {
                    name: "张三",
                    time: "2021-05-01",
                    fake: "是",
                    imgSrc: "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1620000000&di=1b1f1b1f1b1f1b1f1b1f1b1f1b1f1b1f&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F01e4e756e5b9fba801219c77f3b5b6.jpg%401280w_1l_2o_100sh.jpg"
                },
                {
                    name: "李四",
                    time: "2021-05-01",
                    fake: "否",
                    imgSrc: "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1620000000&di=1b1f1b1f1b1f1b1f1b1f1b1f1b1f1b1f&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F01e4e756e5b9fba801219c77f3b5b6.jpg%401280w_1l_2o_100sh.jpg"
                }
            ],
        };
    },
    created() {
        this.init();
    },
    components:{
    Plus,
    IconPicture,
    Refresh,
    VideoReader
},
    watch: {
        currentPage(val) {
            this.handlePageSelect(val);
        }
    },
    methods: {
        init(){
            this.getFacesTotal();
            this.getFacesInPage(this.currentPage);
        },
        handlePageSelect(currentPage) {
            this.getFacesInPage(currentPage);
        },
        handleEdit(index,row){
            this.factoryChooseItem(row);
            this.editChoose = true;
            this.DialogIsVisiable = true;
        },
        updateFaceData(){
            this.UpDateFaceData()
            setTimeout(() => {
                this.init()
            }, 1000);
        },
        handleDelete(index,row){
            this.deleteFaceData(row);
        },
        handleAdd(){
            this.initChooseItem();
            this.editChoose = false
            this.DialogIsVisiable = true;
        },
        handleVideo(){
            this.VideoDialogIsVisiable = true;
        },
        addFaceData(){
            this.UploadFaceData();
            setTimeout(()=>{
                this.init();
            },1000)
        },
        handleInsert(){
            this.addFaceData();
        },

        async getFacesTotal() {
            this.total = await getFacesTotal();
        },
        async getFacesInPage(currentpage) {
            this.facesData = await getFacesData({
                "page":currentpage,
                "pageSize":this.pageSize
            });
        },
        async deleteFaceData(row){
            var results = await deleteFaceData({
                "faceId": row.faceId
                });
            console.log(results);
            if(results.msg=='success'){
                this.$message({
                    message: '删除成功',
                    type: 'success'
                });
            }
            else{
                this.$message({
                    message: '删除失败',
                    type: 'error'
                });
            }   
            this.facesData.forEach((item,index)=>{
                if(item.faceId==row.faceId){
                    this.facesData.splice(index,1);
                }
            })
        },
        initChooseItem(){
            this.chooseItem = {
                faceId: 0,
                name: "",
                fake: "",
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
        getVideoImg(){
            var file = this.$refs['reader'].imgFile;
            this.showImg(file); 
            this.VideoDialogIsVisiable = false;
            console.log(file);
        },
        showImgEvent(e) {
            let file = e.target.files[0];//图片文件名
            this.showImg(file);
        },
        showImg(file){
            let that = this;
            if (!file || !window.FileReader) return; // 看是否支持FileReader
            let reader = new FileReader();
            console.log(file);
            reader.readAsDataURL(file); // 关键一步，在这里转换的
            reader.onloadend = function () {
                that.chooseItem.imgSrc = this.result;//赋值
                that.chooseItem.files = file;
            }
        },
        UploadFaceData(){
            try{
                let fd = new FormData(); //转换为表单进行发送给后端
                fd.append('name',this.chooseItem.name)
                fd.append("imgfile", this.chooseItem.files); //第一个参数就是后端要接受的字段，要一样，不一样会发送失败
                console.log(fd);
                axios({
                    method:'post',
                    url:httpurl+'/manage/add',
                    headers:{'Content-Type':'multipart/form-data',
                            "Access-Control-Allow-Origin": "*"},
                    data:fd,
                }).then((res)=>{
                    if(res.status == 200){
                        this.$message({
                            message: '上传成功',
                            type: 'success'
                        });
                    // this.facesData.find((item)=>{
                    // if(item.faceId == this.chooseItem.faceId){
                    //     item.name = this.chooseItem.name;
                    //     item.imgSrc = this.chooseItem.imgSrc;
                    //     }
                    // })
                    }else{
                        this.$message({
                            message: '上传失败',
                            type: 'error'
                        });
                    }
                })
            }
            catch(e){
                this.$message({
                    message: '错误',
                    type: 'error'
                });
                console.log(e);
            }
            finally{
                this.DialogIsVisiable = false;
                this.initChooseItem();
            }
        },
        UpDateFaceData(){
            try{
                let fd = new FormData(); //转换为表单进行发送给后端
                fd.append('faceId',this.chooseItem.faceId)
                fd.append('name',this.chooseItem.name)
                fd.append("imgfile", this.chooseItem.files); //第一个参数就是后端要接受的字段，要一样，不一样会发送失败
                console.log(fd);
                axios({
                    method:'post',
                    url:httpurl+'/manage/update',
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
                    }else{
                        this.$message({
                            message: '上传失败',
                            type: 'error'
                        });
                    }
                })
            }catch(e){
                this.$message({
                    message: '错误',
                    type: 'error'
                });
                console.log(e);
            }
            finally{
                this.DialogIsVisiable = false;
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
        border-radius:5px;
        
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
    .box-card{
        margin-top: 20px;
    }
</style>
