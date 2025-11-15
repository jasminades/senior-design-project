<template>
  <v-card class="pa-4 mt-4" color="#fffdf9">
    <v-data-table
      :headers="headers"
      :items="history"
      class="elevation-1"
      dense
    >
      <template #item.confidence="{ item }">
        {{ (item.confidence * 100).toFixed(2) }}%
      </template>


    </v-data-table>
  </v-card>
</template>

<script>
export default {
  name: "HistoryTable",
  props: {
    history: Array,
  },
  data() {
    return {
      headers: [
        { text: "Date", value: "date" },
        { text: "Prediction", value: "prediction" },
        { text: "Confidence", value: "confidence" },
      ],
    };
  },
};
</script>
