document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector("input[name='file']");
    const yearSelect = document.querySelector("select[name='year']");
    const analysisSelect = document.getElementById("analysis_key");
    const paramGroups = document.querySelectorAll(".param");

    let dataOptions = null;

    async function fetchOptions() {
        if (!fileInput.files[0] || !yearSelect.value) return;

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);
        formData.append("year", yearSelect.value);

        const response = await fetch("/load-options", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        if (data.error) {
            alert("Erro: " + data.error);
            return;
        }

        dataOptions = data;
        fillSelect("crime", data.crimes);
        fillSelect("bairro", data.bairros);
        fillSelect("semestre", data.semestres);
        fillSelect("periodo", data.periodos);
    }

    function fillSelect(paramName, values) {
        const group = document.querySelector(`[data-param="${paramName}"]`);
        if (!group) return;
        const select = group.querySelector("select");
        if (!select) return;

        select.innerHTML = '<option value="">Selecione</option>';
        values.forEach(v => {
            const opt = document.createElement("option");
            opt.value = v;
            opt.textContent = v;
            select.appendChild(opt);
        });
    }

    analysisSelect.addEventListener("change", () => {
        const selected = analysisSelect.options[analysisSelect.selectedIndex];
        const params = selected.dataset.params ? selected.dataset.params.split(",") : [];
        paramGroups.forEach(g => {
            const name = g.getAttribute("data-param");
            g.classList.toggle("hidden", !params.includes(name));
        });
    });

    fileInput.addEventListener("change", fetchOptions);
    yearSelect.addEventListener("change", fetchOptions);
});
