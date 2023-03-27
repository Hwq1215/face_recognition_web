<template>
    <div class="w-full">
        <div class="compare-box">
        <div class="left-img-container">
            
            <h3>源图片</h3>
            
            <el-upload class="img-button"
            ref="upload"
            :action="actionUrl"
            drag
            v-model:file-list="fileList1"
            list-type="picture-card"
            :show-file-list="false"
            :limit="1"
            :auto-upload="false"
            >      
            <div v-if="img1Url" >          
                <img  class="imgshow" :src="img1Url">
            </div>
                <el-icon v-else class="avatar-uploader-icon "><IconPicture /></el-icon>
            </el-upload>
            <div class="record-button">
                <el-button type="success" @click="openVideo()" circle><el-icon size=""><VideoCameraIcon /></el-icon></el-button>
            </div>
        </div>
        
        <div class="mid-img-container">
            <div>
                <h4>开启关键点检测<el-switch v-model="keyPoint"></el-switch></h4>
                
            </div>
            <div>
                <el-button type="success" size="large" @click="slice">生成</el-button>
            </div>
            <div>
                <el-button type="danger" size="large" @click="clear">清空</el-button>
            </div>
        </div>
         <div class="right-img-container">
            <h3>目标图片</h3>
            <div class="img-button-product">
                <img v-if="img2Url" class="imgshow" :src="img2Url">
                <el-icon v-else class="avatar-uploader-icon "><IconPicture /></el-icon>
            </div>
            
        </div>

    </div>
    </div>

    <el-dialog v-model="VideoDialogIsVisiable">
        <video-reader @choose-img="saveImg()" ref="video-reader"></video-reader>
    </el-dialog>
</template>

<script lang="js">
import { Picture as IconPicture ,SuccessFilled,CircleCloseFilled,Loading, Switch} from '@element-plus/icons-vue'
import { httpurl } from '../config';
import axios from 'axios';
import VideoReader from '../mycomponents/VideoReader.vue';
import {VideoCameraIcon} from "@heroicons/vue/outline"
export default{
    data(){
        return{
            fileList1:[],
            fileList2:[],
            result: {
                is_same: false,
                score: 0,
            },
            actionUrl: httpurl+"/slice",
            img1Url: '',
            img2Url: '',
            DialogIsVisiable: false,
            loadingVisible: true,
            keyPoint: true,
            VideoDialogIsVisiable: false,
        }
    },
    watch:{
        fileList1(newVal){
            if(newVal.length>0){
                this.img1Url = URL.createObjectURL(newVal[0].raw);
            }
        },
        fileList2(newVal){
            if(newVal.length>0){
                this.img2Url = URL.createObjectURL(newVal[0].raw);
            }
        }
    },
    components: {
    IconPicture,
    SuccessFilled,
    CircleCloseFilled,
    Loading,
    Switch,
    VideoReader,
    VideoCameraIcon,
},
    methods:{
        slice(){
            this,this.loadingVisible = true;
            this.DialogIsVisiable = true;
            let fd = new FormData();
            console.log(this.fileList1);
            if (this.fileList1.length == 0){
                this.$message.error('请上传图片');
                return;
            }
            fd.append('img', this.fileList1[0].raw);
            fd.append('keypoint', this.keyPoint);
            axios({
                method:'post',
                url:this.actionUrl,
                headers:{'Content-Type':'multipart/form-data',
                        "Access-Control-Allow-Origin": "*"},
                data:fd,
            }).then((res)=>{
                this.img2Url = res.data;               
            })
        },
        clear(){
            this.fileList1 = [];
            this.fileList2 = [];
            this.img1Url = '';
            this.img2Url = '';
        },
        openVideo(){
            this.VideoDialogIsVisiable = true;
        },
        saveImg(){
            var img = this.$refs['video-reader'].imgFile;
            if(img == '' || img == null || img == undefined){
                this.$message.error('请先拍照');
                return;
            }
            this.fileList1 = [];
            this.fileList1.push({raw:img});
            this.VideoDialogIsVisiable = false;
        }
    }
}
</script>
<style>
@media screen and (max-width: 1400px) {
    .compare-box{
    width: 100%;
    height: 1300px;
    background-color: #f8f9fe;
    text-align: center;
    align-items: center;
    justify-content: center;
}

.left-img-container{
    margin: 0 auto;
    margin-top: 20%;
    width: 400px;
    height: 400px;
    background-color: #f8f9fe;
    text-align: center;
}

.left-img-container .el-upload-dragger{
    width: 400px;
    height: 400px;
    background-color: #f8f9fe;
    border: #614555 2px;
    border-radius: 5px;
    border-style:dotted;
    text-align: center;
}

.right-img-container{
    margin: 0 auto;
    margin-top: 5%;
    width: 400px;
    height: 400px;
    background-color: #f8f9fe;
    text-align: center;
    
}
.right-img-container .img-button-product{
    width: 400px;
    height: 400px;
    background-color: #f8f9fe;
    border: #614555 2px;
    border-radius: 5px;
    border-style:dotted;
    text-align: center;
}

.img-button-product .el-icon.avatar-uploader-icon {
  
  font-size: 28px;
  color: #8c939d;
  width: 390px;
  height: 390px;
  text-align: center;
}
.right-img-container .img{
    width: 400px;
    height: 400px;
    background-color: #f8f9fe;
    border: #614555 2px;
    border-radius: 5px;
    border-style:dotted;
    text-align: center;
}

 .mid-img-container{
    margin-top: 120px;
    background-color: #f8f9fe;
    border: #f5f5f5 1px;
    border-radius: 5px;
    text-align: center;
    align-items: center;
    justify-content: center;
}

.mid-img-container > div{
    width: 100%;
    height: 100px;
    background-color: #f8f9fe;
    text-align: center;
}

.img-button{
    width: 100%;
    height: 100%;
    background-color: #f8f9fe;
    border: #f5f5f5 1px;
    border-radius: 5px;
    display: flex;
    text-align: center;
}
.img-button .imgshow{
    max-width: 400px;
    max-height: 400px;
    margin: 0 auto;
    justify-content: center;
    align-items: center;
}
.imgshow img{
    max-width: 400px;
    max-height: 400px;
    display: inline;
    object-fit: fill;
    margin: 0 auto;
}
.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 300px;
  height: 300px;
  text-align: center;
}
.dialog-center{
    text-align: center;
}
.record-button{
    margin-top: 5%;
    width: 100%;
    height: 100%;
}
}
@media screen and (min-width: 1400px) {
    .compare-box{
    display: flex;
    width: 100%;
    height: 100%;
    background-color: #ffffff;
    text-align: center;
    align-items: center;
    justify-content: center;
}

.left-img-container{
    margin-left: 120px;
    margin-top: 100px;
    width: 400px;
    height: 600px;
    background-color: #ffffff;
    float: left;
    text-align: center;
}

.left-img-container .el-upload-dragger{
    width: 400px;
    height: 400px;
    background-color: #f5f5f5;
    border: #614555 2px;
    border-radius: 5px;
    border-style:dotted;
    text-align: center;
}

.right-img-container{
    margin-right: 120px;
    margin-top: 100px;
    width: 400px;
    height: 600px;
    background-color: #ffffff;
    float: right;
    text-align: center;

}

.right-img-container .img-button-product{
    width: 400px;
    height: 400px;
    background-color: #f5f5f5;
    border: #614555 2px;
    border-radius: 5px;
    border-style:dotted;
    text-align: center;
}

.img-button-product .el-icon.avatar-uploader-icon {
  
  font-size: 28px;
  color: #8c939d;
  width: 390px;
  height: 390px;
  text-align: center;
}
.mid-img-container{
    margin-left: 132px;
    margin-right: 132px;
    width: 200px;
    height: 200px;
    background-color: #ffffff;
    float: left;
    border: #f5f5f5 1px;
    border-radius: 5px;
    text-align: center;
}

.mid-img-container > div{
    width: 100%;
    height: 100px;
    background-color: #ffffff;
    float: left;
    text-align: center;
}

.img-button{
    width: 400px;
    height: 400px;
    background-color: #f5f5f5;
    border: #f5f5f5 1px;
    border-radius: 5px;
    display: flex;
}
.img-button .imgshow{
    max-width: 390px;
    max-height: 330px;
    margin: 0 auto;
}
.img-button-product .imgshow{
    margin: auto;
    margin-top: 35px;
    max-width: 390px;
    max-height: 360px;
    display: inline;
    justify-content: center;
    align-items: center;
}
.imgshow img{       
    max-width: 360px;
    max-height: 330px;
    margin: 0 auto;
    justify-content: center;
    align-items: center;
}
.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 300px;
  height: 300px;
  text-align: center;
}
.dialog-center{
    text-align: center;
}
.record-button{
    margin-top: 5%;
    width: 100%;
    height: 100%;
}
}
</style>



