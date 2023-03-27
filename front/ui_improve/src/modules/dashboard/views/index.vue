<template>
  <div class="w-full mx-auto">
    <div class="w-full">
      <AnalysisCard  />
    </div>

    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
          <GradientLineChart title="数据统计" subcription="人脸注册人数"/>
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <TotalBarChart title="数据统计" subcription="欺诈种类"/>
        </div>
      </div>
    </div>

    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5">
          <PageVisitTable title="API使用情况"/>
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <SocialTrafficTable title="系统资源使用率总览"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import AnalysisCard from 'modules/cards/views/components/AnalysisCard.vue'
// Chart
import GradientLineChart from './components/GradientLineChart.vue'
import TotalBarChart from './components/TotalBarChart.vue'
// Table
import SocialTrafficTable from './components/SocialTrafficTable.vue'
import PageVisitTable from './components/PageVisitTable.vue'

export default defineComponent({
  name: 'DashBoard',
  components: {
    AnalysisCard,
    GradientLineChart,
    TotalBarChart,
    PageVisitTable,
    SocialTrafficTable,
  },
  setup() {
    return {}
  },
})
</script>
