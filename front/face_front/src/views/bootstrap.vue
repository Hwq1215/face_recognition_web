<template>
    <div>
        <el-carousel height="600px" type="card">
            <el-carousel-item v-for="item in 3" :key="item"  >
                <img  src="../assets/Biden.png">
            </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script>
export default{
    name: 'bootstrap',
}
</script>

<style>
 .el-carousel__item{
    text-align: center;
 }
 .el-carousel__item img {
  color: #475669;
  opacity: 1;
  margin: 0;
  text-align: center;
  
}
</style>