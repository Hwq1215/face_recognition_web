<template>
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
        </div>
        
        <div class="mid-img-container">
            <div>

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
    <!-- <el-dialog v-model="DialogIsVisiable" v-loading="loadingVisible" width="300px" title="比对结果" center>
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
    </el-dialog> -->
</template>

<script>
import { Picture as IconPicture ,SuccessFilled,CircleCloseFilled,Loading} from '@element-plus/icons-vue'
import { httpurl } from '../../public/config';
import axios from 'axios';

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
        Loading
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
        }
    }
</script>
<style>
.compare-box{
    display: flex;
    width: 100%;
    height: 100%;
    background-color: #ffffff;
}

.left-img-container{
    margin-left: 120px;
    margin-top: 100px;
    width: 400px;
    height: 400px;
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
    height: 400px;
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
    margin-top: 200px;
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
    max-width: 350px;
    max-height: 320px;
}
.img-button-product{
    width: 400px;
    height: 400px;
    background-color: #f5f5f5;
    border: #000000 2px dotted;
    border-radius: 5px;
    display: flex;
    
}
.img-button-product .imgshow{
    margin: auto;
    max-width: 360px;
    max-height: 320px
}
.img-button .el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 300px;
  height: 300px;
  text-align: center;
}
.img-button-product .el-icon.avatar-uploader-icon {
  
  font-size: 28px;
  color: #8c939d;
  width: 390px;
  height: 390px;
  text-align: center;
}
.dialog-center{
    text-align: center;
}
</style>


