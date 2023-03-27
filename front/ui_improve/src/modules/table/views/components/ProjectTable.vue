<template>
  <div class="w-full">
    <el-table :data="facesData" style="width: 100%" :class="`is-${theme}`" v-cloak>
      <el-table-column label="编号" width="200">
        <template #default="scope">
          {{scope.$index + 1}}
        </template>
      </el-table-column>
      <el-table-column label="用户名" min-width="280">
          <template #default="scope">
          <div @click="handleEdit(scope.$index, scope.row)" class="flex items-center">
            <span class="pl-2 mb-0 text font-semibold cursor-auto " style="margin-left:0">
              {{scope.row.name}}
            </span>
          </div>
          </template>
      </el-table-column>

      <el-table-column  label="操作" width="200" fixed="right">
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
        <el-button type="success"  @click="handleAdd()" style="float:right; margin-right: 5%; margin-top: 40px;" circle>
          <el-icon ><Plus/></el-icon>
        </el-button>
        <el-button type="success" @click="handleAddAll()" style="float:right; margin-right: 2%; margin-top: 40px;" rounded>
          <input type="file" ref="input-all" style="display: none;"/>
            批量上传
        </el-button>
        <span style="float:right; margin-right: 2%; margin-top: 45px; color: #b0b0b0;">支持zip,rar格式的压缩包</span>
        <div class="p-4">
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
  </div>
  <el-dialog v-model="DialogIsVisiable" :title="editChoose?'修改':'上传'">
        <el-form>
            <el-form-item label="姓名">
                <el-input v-model="chooseItem.name"></el-input>
            </el-form-item>
            <el-form-item label="图片">
                <div @click="HandleImgSelect()" class="input-img">
                    <img v-if="chooseItem.imgSrc"  :src="chooseItem.imgSrc">
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
import { defineComponent, ref } from 'vue'
import { DotsVerticalIcon } from '@heroicons/vue/outline'
import {getFacesData,getFacesTotal,deleteFaceData} from "@/api/getData";
import { Plus,Picture as IconPicture, Picture, Upload, Refresh} from '@element-plus/icons-vue'
import VideoReader from "@/mycomponents/VideoReader.vue"
import {httpurl} from "../../../../config";
import axios from "axios";
import { randomUUID } from 'crypto';

export default{
    name: 'ProjectTable',
    props: {
    facesData: {
      type: Array,
      required: false,
    },
    pageSize: {
      type: Number,
      required: false,
    },
    },
    data() {
        return {
            total: 20,
            currentPage: 1,
            DialogIsVisiable: false,
            VideoDialogIsVisiable: false,
            editChoose: true,
            imageUrl: "",
            pageSize: 20,
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
        }
    },
    created(){
        this.init();
    },
    components: {
    DotsVerticalIcon,
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
        },
        handleDelete(index,row){
            this.deleteFaceData(row);
        },
        handleAdd(){
            this.initChooseItem();
            this.editChoose = false
            this.DialogIsVisiable = true;
        },
        handleAddAll(){
          this.$refs['input-all'].click();
        },
        handleVideo(){
            this.VideoDialogIsVisiable = true;
        },
        addFaceData(){
            this.UploadFaceData();
        },
        handleInsert(){
            this.addFaceData();
        },
        async getFacesTotal() {
            this.total = await getFacesTotal();
        },
        async getFacesInPage(currentpage) {
            this.facesData = []
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
                    console.log(res)
                    if(res.data == 'success'){
                        this.$message({
                            message: '添加成功',
                            type: 'success'
                        });
                    }else{
                        this.$message({
                            message: '添加失败',
                            type: 'error'
                        });
                    }
                    this.init();
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
                    console.log(res)
                    if(res.data == "success"){
                        this.$message({
                            message: '修改成功',
                            type: 'success'
                        });
                    this.facesData.map((item)=>{
                    if(item.faceId == this.chooseItem.faceId){
                        item.name = this.chooseItem.name;
                        item.imgSrc = this.chooseItem.imgSrc + "?t=" + new Date().getTime();
                        }
                    })
                    }else{
                        this.$message({
                            message: '修改失败，人脸数不唯一或者人脸重复',
                            type: 'error'
                        });
                    }
                    this.init();
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
    [v-cloak]:{display:none}
</style>