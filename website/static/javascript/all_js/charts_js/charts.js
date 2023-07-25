$(document).ready(function() {
  // ----------------------------- set variables start -----------------------------
  // var chartContentColor = "rgb(0, 0, 0, 0.50)";
  var chartContentColor = "rgba(0, 130, 22, 0.5)";
  var chartBorderWidth = 3;
  var idsArray = ["id-chart_distribution_answer_choice","id-chart_distribution_generation","id-chart_distribution_age_group","id-chart_distribution_gender","id-chart_distribution_annual_income","id-chart_distribution_relationship_status","id-chart_distribution_education","id-chart_distribution_employment","id-chart_distribution_collar","id-chart_distribution_ethnicity","id-chart_distribution_politics","id-chart_distribution_own_vs_rent","id-chart_distribution_industry"];
  var titlesArray = [chart_distribution_title_answer_choice,chart_distribution_title_generation,chart_distribution_title_age_group,chart_distribution_title_gender,chart_distribution_title_annual_income,chart_distribution_title_relationship_status,chart_distribution_title_education,chart_distribution_title_employment,chart_distribution_title_collar,chart_distribution_title_ethnicity,chart_distribution_title_politics,chart_distribution_title_own_vs_rent,chart_distribution_title_industry];
  var labelsArray = [chart_distribution_labels_answer_choice,chart_distribution_labels_generation,chart_distribution_labels_age_group,chart_distribution_labels_gender,chart_distribution_labels_annual_income,chart_distribution_labels_relationship_status,chart_distribution_labels_education,chart_distribution_labels_employment,chart_distribution_labels_collar,chart_distribution_labels_ethnicity,chart_distribution_labels_politics,chart_distribution_labels_own_vs_rent,chart_distribution_labels_industry];
  var valuesArray = [chart_distribution_values_answer_choice,chart_distribution_values_generation,chart_distribution_values_age_group,chart_distribution_values_gender,chart_distribution_values_annual_income,chart_distribution_values_relationship_status,chart_distribution_values_education,chart_distribution_values_employment,chart_distribution_values_collar,chart_distribution_values_ethnicity,chart_distribution_values_politics,chart_distribution_values_own_vs_rent,chart_distribution_values_industry];
  // ----------------------------- set variables end -----------------------------
  // ----------------------------- for loop charts start -----------------------------
  for (var i = 0; i < idsArray.length; i++) {
    try {
      new Chart(idsArray[i], {
        type: "horizontalBar",
        data: {
          labels: labelsArray[i],
          datasets: [{
            backgroundColor: chartContentColor,
            data: valuesArray[i],
            borderWidth: chartBorderWidth
          }]
        },
        options: {
          legend: {display: false},
          title: {
            display: true,
            text: titlesArray[i]
          }
        }
      }); 
    } catch (error) {
      // catch_nothing
    }
  }
  // ----------------------------- for loop charts end -----------------------------
});