<template>
    <el-table>
        <el-table-column prop="date" label="日期" width="180"></el-table-column>
        <el-table-column prop="name" label="姓名" width="180"></el-table-column>
        <el-table-column prop="address" label="地址"></el-table-column>
    </el-table>
    <div class="">
        <el-pagination
        :page-size="14"
        :pager-count="10"
        layout="prev, pager, next"
        :hide-on-single-page="true"
        :total="1000"
    />
    </div>

</template>

<script>
    export default{
        data(){
            return{
                total: 0,
            }
        },
        method:{

        }
    }
</script>