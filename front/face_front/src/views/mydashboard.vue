<template>
  <div class="left-box">
    <div class="left-single">
    <el-card class="box-card">
        这里做每日人脸识别的数据折线图，包括正常的和欺诈的asdddddddddssdasdasdddddddddddasdddddddddddddddddddddddddddddddddddddddddddddddddddddasddddddddddddasddddddddddddddddddddddddddddddddddddddddddddd
      </el-card>
    </div>
      <div class="left-single">
        <div class="left-left-box"> 
        <el-card class="box-card">
        <v-chart class="chart" :option="option" autoresize />
        这里放欺诈类型assssssssssssssssssssssssssssssssssssaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaassssssssssssssssssssssssssss
        </el-card>    
      </div>      
      <div class="left-right-card">
        <el-card class="box-card">
          <v-chart class="chart" :option="option" autoresize />
        这里放人脸识别的饼图sdaaaaaaaaaaasddddkiiiiiiiiiiiiiiiikiiiiiiiiiiiiiiikiiiiiiiiiiiiiiiiiiiiiiiiii
        </el-card>
      </div>
    </div>
  </div >
  <div class="right-box">
    <el-card class="box-card">
    这里做人脸数量和欺诈分析的饼图asddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddasd
      </el-card>
  </div>

</template>
  
  <script>

  export default{
    name: 'dashboard',
    data(){
      return{
        option: {
        title: {
          text: ''
        },
        tooltip: {},
        legend: {
          data:['销量']
        },
        xAxis: {
          data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
        },
        yAxis: {},
        series: [{
          name: '销量',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }]},
      }
    },
  }
  
  </script>
  
  <style >
  .chart{
    width: 100%;
    height: 350px;
  }
  .left-box{
    margin-left: 1%;
    width: 60%;
    height: 100%;
    float: left;
  }
  .left-single{
    width: 100%;
    height: 34vh;
    margin-top: 1%;
    display: flex;
  }
  .left-single .left-left-box{
    width: 46%;
    height: 20vh;
    margin-right: 2%;
    float: left;
  }
  .left-single .left-right-box{
    width: 46%;
    height: 100%;
    margin: 0;
    float: right;
  }
  .right-box{
    margin-left: 1%;
    width: 37%;
    margin-right: 1%;
    height: 100%;
    margin-top: 0.62%;
    float: right;
  }
  .box-card{
    border: 1px white solid;
    border-radius: 5px;
    min-height: 20px;
  }
  </style>
  