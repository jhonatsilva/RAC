window.addEventListener("load", () => {
    const analysisSelect = document.getElementById("analysis_key");
    const crimeGroup = document.querySelector(".param[data-param='crime']");
    const bairroGroup = document.querySelector(".param[data-param='bairro']");
    const semestreGroup = document.querySelector(".param[data-param='semestre']");
    const periodoGroup = document.querySelector(".param[data-param='periodo']");
    const crimeSelect = document.getElementById("crime");
    const bairroSelect = document.getElementById("bairro");

    const logic = {
        total_por_crime: ["crime"],
        total_por_bairro: ["bairro"],
        crime_por_bairro: ["crime", "bairro"],
        bairro_por_crime: ["bairro", "crime"],
        comparativo_semestre: ["semestre"],
        periodo_dia: ["periodo"],
        geral: []
    };

    const allGroups = [crimeGroup, bairroGroup, semestreGroup, periodoGroup];

    function hideAll() {
        allGroups.forEach(el => el && el.classList.add("hidden"));
    }

    function showForType() {
        const type = analysisSelect.value;
        const visible = logic[type] || [];
        hideAll();

        visible.forEach(p => {
            const group = document.querySelector(`.param[data-param='${p}']`);
            if (group) group.classList.remove("hidden");
        });

        if (type === "crime_por_bairro" && !crimeSelect.value) {
            bairroGroup.classList.add("hidden");
        }
        if (type === "bairro_por_crime" && !bairroSelect.value) {
            crimeGroup.classList.add("hidden");
        }
    }

    hideAll();

    if (analysisSelect) analysisSelect.addEventListener("change", showForType);
    if (crimeSelect) crimeSelect.addEventListener("change", showForType);
    if (bairroSelect) bairroSelect.addEventListener("change", showForType);
});
