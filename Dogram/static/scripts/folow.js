document.addEventListener("DOMContentLoaded", function () {
    const seguirBtn = document.querySelector(".seguir-btn");

    if (!seguirBtn) return;

    seguirBtn.addEventListener("click", () => {
        const userId = seguirBtn.getAttribute("data-profile-id");
        const csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content");

        fetch(`/seguir/${userId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                seguirBtn.textContent = data.seguindo ? "Deixar de seguir" : "Seguir";
                seguirBtn.classList.toggle("seguindo", data.seguindo);
                document.getElementById("contador-seguidores").textContent = data.total_seguidores;
            }
        })
        .catch(error => {
            console.error("Erro ao seguir:", error);
        });
    });
});
