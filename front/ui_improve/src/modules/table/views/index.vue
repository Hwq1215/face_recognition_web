<template>
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="py-5 px-6 border-b border-primary-white">
        <h3 class="cursor-auto">人脸信息</h3>
      </div>
      <div class="block overflow-x-auto w-full">
        <ProjectTable :facesData="facesData" :pageSize="page-size" />
      </div>
      <!-- <div class="p-4">
        <el-pagination 
        :page-size="pageSize"
        :pager-count="5"
        v-model:current-page="currentPage"
        background
        layout="prev, pager, next"
        :total="total"
        class="mt-4"
        />
      </div> -->
    </div>
    <!-- <div class="flex flex-wrap flex-col shadow mb-7 mx-auto rounded-md bg-dark">
      <div class="py-5 px-6 border-b border-dark-light">
        <h3 class="cursor-auto text-slate-50">Dark table</h3>
      </div>
      <div class="block overflow-x-auto w-full">
        <ProjectTable :tableData="tableData" :theme="'dark'" />
      </div>
    </div> -->
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import {getFacesData} from '@/api/getData'
import John_Snow_Url from '@/assets/images/John_Snow.png'
import Team_2_Url from '@/assets/images/team-2.jpg'
import Team_3_Url from '@/assets/images/team-3.jpg'
import Team_4_Url from '@/assets/images/team-4.jpg'
import Logo_Url from '@/assets/images/ltv_logo.png'
import ProjectTable from './components/ProjectTable.vue'

export default {
  name: 'Tables',
  data(){
    return {
      facesData: [],
      pageSize: 13,
      currentPage: 1,
      total: 0,
    }
  },
  
  methods: {
    init(){
      this.ProjectTable.init()
    }
  },
  components: {
    ProjectTable,
  },
}
</script>
