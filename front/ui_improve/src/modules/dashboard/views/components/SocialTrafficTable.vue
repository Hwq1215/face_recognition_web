<template>
  <div class="w-full">
    <div class="flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="flex flex-wrap items-center py-2 px-6 mb-0 border-b-dark-4">
        <div class="max-w-full basis-0 grow">
          <h3 class="mb-0 cursor-auto text-primary-dark">{{ title }}</h3>
        </div>
        <div class="max-w-full basis-0 grow">
          <div class="flex flex-wrap mb-0 pl-0 justify-end gap-x-3">
            <div>
              <el-button type="primary" size="small"> 查看全部 </el-button>
            </div>
          </div>
        </div>
      </div>

      <div class="block overflow-x-auto w-full">
        <el-table :data="tableData" style="width: 100%" class="is-light">
          <el-table-column label="设备名称" min-width="100">
            <template #default="scope">
              <div class="flex items-center">
                <span class="mb-0 text-0.8125 font-semibold cursor-auto text-dark-lighter">{{
                  scope.row.referral
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="设备内容" width="130">
            <template #default="scope">
              <div class="flex items-center">
                <span class="px-4 text-0.8125 font-normal text-dark-lighter">{{
                  scope.row.visitorNumber
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column min-width="200">
            <template #default="scope">
              <div class="px-4 flex flex-row items-center">
                <div class="w-2/5 text-right">
                  <span class="text-0.8125">{{ scope.row.completion }}%</span>
                </div>
                <div class="w-full ml-2">
                  <el-progress
                    :percentage="scope.row.completion"
                    :show-text="false"
                    :color="customColorMethod(scope.row.completion)"
                  />
                </div>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'SocialTrafficTable',
  props: {
    title: {
      type: String,
      default: 'Social traffic',
    },
  },
  setup() {
    const tableData: any[] = [
      {
        referral: 'GPU1',
        visitorNumber: 'RTX 3090',
        completion: 60,
      },
      {
        referral: 'GPU2',
        visitorNumber: 'RTX 2080',
        completion: 70,
      },
      {
        referral: 'CPU',
        visitorNumber: 'Xeon 8358P',
        completion: 80,
      },
      {
        referral: '内存',
        visitorNumber: '63.45GB',
        completion: 75,
      },
      {
        referral: '网络带宽',
        visitorNumber: '1000Mbps',
        completion: 30,
      },
    ]
    const theme = ref([
      { completion: 60, color: '#F5365C' },
      { completion: 70, color: '#2DCE89' },
      { completion: 75, color: '#11CDEF' },
      { completion: 80, color: '#6c6be4' },
    ])

    const customColorMethod = (completion: number) => {
      return theme.value.find((el: any) => el.completion == completion)?.color ?? '#FB6340'
    }

    return {
      tableData,
      customColorMethod,
    }
  },
})
</script>
