<template>
  <v-card class="history-card pa-4 mt-4 mx-auto">
    <h2 class="card-title mb-4">Your Previous Analyses</h2>

    <v-data-table
      :headers="headers"
      :items="history"
      class="elevation-1 history-table"
      dense
      :items-per-page="itemsPerPage"
      :footer-props="{
        'items-per-page-options': [10, 15, 20, 50],
        'show-current-page': true,
        'show-first-last-page': true
      }"
    >
      <template #item.confidence="{ item }">
        {{ (item.confidence).toFixed(2) }}%
      </template>

      <template #item.date="{ item }">
        {{ item.date }}
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  name: "HistoryTable",
  props: {
    history: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      headers: [
        { text: "Date", value: "date" },
        { text: "Prediction", value: "prediction" },
        { text: "Confidence", value: "confidence" },
      ],
      itemsPerPage: 10,
    };
  },
};
</script>

<style scoped>
.history-card {
  width: 90%;
  max-width: 1000px;
  border-radius: 2rem;
  background: linear-gradient(145deg, #f9f9ff, #eef1ff);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.history-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.12);
}

.card-title {
  font-weight: 700;
  font-size: 1.5rem;
  color: #4a4a7b;
}

.history-table .v-data-table-header {
  background: #f0eaff;
  font-weight: 600;
  color: #4a4a7b;
}

.history-table .v-data-table__divider {
  border-color: #e6e1ff;
}

.history-table tbody tr {
  transition: background 0.3s ease;
  cursor: pointer;
}

.history-table tbody tr:hover {
  background: rgba(127, 115, 239, 0.1);
}

.history-table td {
  padding: 12px 15px;
  color: #555;
}

@media (max-width: 960px) {
  .history-card {
    width: 95%;
    padding: 2rem 1.5rem;
  }
}
</style>
