<template>
    <div class="w-full">
        <div class="compare-box">
        <div class="left-img-container">
            
            <h3>第一张图片</h3>
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
                <img  v-if="img1Url" class="imgshow" :src="img1Url">
            </div>
                <el-icon v-else class="avatar-uploader-icon "><IconPicture /></el-icon>
            </el-upload>
            <div class="record-button">
                <el-button type="success" @click="openVideo(1)" round><el-icon><CameraIcon /></el-icon></el-button>
            </div>
        </div>
        
        <div class="mid-img-container">
            <div>

            </div>
            <div>
                <el-button type="primary" size="large" @click="compare">比对</el-button>
            </div>
            <div>
                <el-button type="danger" size="large" @click="clear">清空</el-button>
            </div>
        </div>
         <div class="right-img-container">
            <h3>第二张图片</h3>
            <el-upload class="img-button"
            ref="upload"
            list-type="picture-card"
            :action="actionUrl"
            drag
            v-model:file-list="fileList2"
            :show-file-list="false"
            :limit="1"
            :auto-upload="false"
            >
            <div  v-if="img2Url" class="imgshow">
                <img  v-if="img1Url" :src="img2Url">
            </div>
                <el-icon v-else class="avatar-uploader-icon "><IconPicture /></el-icon>
            </el-upload>
            <div class="record-button">
                <el-button type="success" @click="openVideo(2)" round><el-icon><CameraIcon /></el-icon></el-button>
            </div>
        </div>

    </div>
 
    </div>
    <el-dialog v-model="DialogIsVisiable" v-loading="loadingVisible" width="200px" title="比对结果" center>
            <div>
                <div >
                    <div >
                    <h3>是否为一个人
                        <el-icon v-if="loadingVisible"> <Loading /></el-icon>
                        <el-icon v-else-if="result.is_same"  color="#5bc194"><SuccessFilled/></el-icon>
                        <el-icon v-else color="#fc5531"><CircleCloseFilled/></el-icon>
                    </h3>
                    </div>
                    <div>
                    <h3>成绩:
                        <el-icon v-if="loadingVisible"> <Loading /></el-icon>
                        <el v-else>{{result.score}}</el>
                    </h3>
                    </div>
                </div>
                
            </div>
    </el-dialog>

    <el-dialog v-model="VideoDialogIsVisiable" class="dialog-center" :lock-scroll="false">
        <video-reader @choose-img="saveImg()" ref="video-reader"></video-reader>
    </el-dialog>

</template>

<script >
import { Picture as IconPicture ,SuccessFilled,CircleCloseFilled,Loading} from '@element-plus/icons-vue'
import { httpurl } from '../config';
import axios from 'axios';
import VideoReader from '../mycomponents/VideoReader.vue';
import {CameraIcon} from '@heroicons/vue/solid'
export default{
    name: 'compareFace',
    data(){
        return{
            fileList1:[],
            fileList2:[],
            result: {
                is_same: false,
                score: 0,
            },
            actionUrl: httpurl+"/compare",
            img1Url: '',
            img2Url: '',
            DialogIsVisiable: false,
            loadingVisible: true,
            VideoDialogIsVisiable: false,
            videoIndex: 1,
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
        VideoReader,
        CameraIcon,
    },
    methods:{
        compare(){
            this,this.loadingVisible = true;
            this.DialogIsVisiable = true;
            let fd = new FormData();
            console.log(this.fileList1);
            console.log(this.fileList2);
            if (this.fileList1.length == 0 || this.fileList2.length == 0){
                this.$message.error('请上传图片');
                return;
            }
            fd.append('img1', this.fileList1[0].raw);
            fd.append('img2', this.fileList2[0].raw);
            axios({
                method:'post',
                url:this.actionUrl,
                headers:{'Content-Type':'multipart/form-data',
                        "Access-Control-Allow-Origin": "*"},
                data:fd,
            }).then((res)=>{
                console.log(res);
                this.result = res.data;
                if(res.status!=200){
                    this.$message.error('比对失败');
                    this.DialogIsVisiable = false
                    return;
                }
                console.log(this.result);
                if(this.result.score == -1){
                    this.$message.error('比对失败,没有找到人脸');
                    this.DialogIsVisiable = false
                    return;
                }
                
                this.loadingVisible = false;                
            })
        },
        clear(){
            this.fileList1 = [];
            this.fileList2 = [];
            this.img1Url = '';
            this.img2Url = '';
        },
        openVideo(index){
            console.log(index);
            this.videoIndex = index;
            this.VideoDialogIsVisiable = true;
        },
        saveImg(){
            var img = this.$refs['video-reader'].imgFile;
            if(img == '' || img == null || img == undefined){
                this.$message.error('请先拍照');
                return;
            }
            if(this.videoIndex == 1){
                this.fileList1 = [];
                this.fileList1.push({raw:img});
            }else{
                this.fileList2 = [];
                this.fileList2.push({raw:img});
            }
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

.right-img-container .el-upload-dragger{
    width: 400px;
    height: 400px;
    background-color: #f8f9fe;
    border: #614555 2px;
    border-radius: 5px;
    border-style:dotted;
    text-align: center;
}

 .mid-img-container{
    margin-top: 50px;
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

.right-img-container .el-upload-dragger{
    width: 400px;
    height: 400px;
    background-color: #f5f5f5;
    border: #614555 2px;
    border-radius: 5px;
    border-style:dotted;
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
    max-height: 320px;
    margin: 0 auto;
}
.imgshow img{
    max-width: 390px;
    max-height: 320px;
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

</style>


