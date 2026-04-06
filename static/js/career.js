document.addEventListener("DOMContentLoaded", function () {
  fetch('/api/result')
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById("career-title").textContent = "No result found";
        document.getElementById("score-value").textContent = "0%";
        document.getElementById("gap-list").innerHTML =
          "<li>Please complete the assessment first.</li>";
        return;
      }

      document.getElementById("career-title").textContent = data.career;
      document.getElementById("score-value").textContent = data.score + "%";
      document.getElementById("score-bar").style.width = data.score + "%";

      let techHTML = "";
      let softHTML = "";
      let metricsHTML = "";

      for (let skill in data.skills) {
        if (skill === "Readiness") continue;

        let value = data.skills[skill];
        let block = `
          <div class="skill-row">
            <p>${skill} <span>${value}%</span></p>
            <div class="progress-bar">
              <div class="progress" style="width:${value}%"></div>
            </div>
          </div>
        `;

        const techCategories = ["Frontend", "Backend", "AI/Data Science", "DSA"];
        const metricsCategories = ["Domain Fit", "Tag Similarity"];

        if (techCategories.includes(skill)) {
          techHTML += block;
        } else if (skill === "Soft Skills") {
          softHTML += block;
        } else if (metricsCategories.includes(skill)) {
          metricsHTML += block;
        }
      }

      document.getElementById("technical-skills").innerHTML = techHTML;
      document.getElementById("soft-skills").innerHTML = softHTML;

      const metricsContainer = document.getElementById("advanced-metrics");
      if (metricsContainer) {
        metricsContainer.innerHTML = metricsHTML;
      }

      let gapHTML = "";
      if (data.gaps?.missing?.length) {
        gapHTML += `<li style="font-weight: bold; color: #c62828;">Critical Missing Skills:</li>`;
        data.gaps.missing.forEach(g => {
          gapHTML += `<li>❌ ${g}</li>`;
        });
      }

      if (data.gaps?.weak?.length) {
        gapHTML += `<li style="font-weight: bold; color: #f9a825; margin-top: 10px;">Skills to Improve:</li>`;
        data.gaps.weak.forEach(g => {
          gapHTML += `<li>⚠️ ${g}</li>`;
        });
      }

      document.getElementById("gap-list").innerHTML =
        gapHTML || "<li>No major skill gaps identified! You are well-prepared.</li>";
    })
    .catch(err => {
      console.error(err);
      document.getElementById("career-title").textContent = "Error loading result";
      document.getElementById("score-value").textContent = "0%";
    });
});