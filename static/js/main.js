document.addEventListener("DOMContentLoaded", function () {
   
    // PRODUCTOS
  const productGrid = document.querySelector(".row.g-3");
  if (productGrid && document.body.contains(productGrid)) {
    const productCards = productGrid.querySelectorAll(".card");
    const existingBadge = document.getElementById("productResultsInfo");


    let infoEl = existingBadge;
    if (!infoEl) {
      infoEl = document.createElement("small");
      infoEl.id = "productResultsInfo";
      infoEl.className = "text-muted d-block mb-2";
      const mainContainer = document.querySelector("main.container");
      if (mainContainer && mainContainer.firstElementChild) {
        mainContainer.insertBefore(infoEl, mainContainer.firstElementChild.nextSibling);
      }
    }

    const count = productCards.length;
    if (count > 0) {
      infoEl.textContent = `${count} producto${count !== 1 ? "s" : ""} encontrados`;
    } else {
      infoEl.textContent = "Sin productos en esta vista";
    }
  }


    //  LOOKS
  const tagInput = document.getElementById("tagFilterInput");
  const lookCardsGrid = document.getElementById("lookCardsGrid");
  const lookInfo = document.getElementById("lookResultsInfo");

  if (tagInput && lookCardsGrid) {
    const lookCards = Array.from(
      lookCardsGrid.querySelectorAll(".look-card")
    );

    function actualizarFiltroLooks() {
      const term = tagInput.value.trim().toLowerCase();
      let visibles = 0;

      lookCards.forEach((card) => {
        const tags = (card.dataset.tags || "").toLowerCase();
        const coincide = term === "" || tags.includes(term);
        card.classList.toggle("d-none", !coincide);
        if (coincide) visibles++;
      });

      if (lookInfo) {
        if (visibles === lookCards.length && term === "") {
          lookInfo.classList.add("d-none");
        } else {
          lookInfo.classList.remove("d-none");
          lookInfo.textContent =
            visibles > 0
              ? `${visibles} look${visibles !== 1 ? "s" : ""} encontrados`
              : "Sin resultados para ese tag";
        }
      }
    }

    // Filtro mientras escribe
    tagInput.addEventListener("input", actualizarFiltroLooks);

    tagInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        actualizarFiltroLooks();
      }
    });

    actualizarFiltroLooks();
  }
});