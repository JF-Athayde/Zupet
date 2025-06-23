document.addEventListener("DOMContentLoaded", function () {
    const botoesCurtir = document.querySelectorAll(".curtir-btn");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    botoesCurtir.forEach(botao => {
        botao.addEventListener("click", function (e) {
            e.preventDefault(); // impede comportamento padrão

            const postId = this.getAttribute("data-post-id");

            fetch(`/curtir/${postId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({}),
                credentials: "include" // mantém o cookie de login
            })
            .then(response => {
                if (!response.ok) throw new Error("Erro na requisição");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const contador = document.getElementById(`likes-${postId}`);
                    contador.textContent = data.likes;
                }
            })
            .catch(error => {
                console.error("Erro ao curtir:", error);
            });
        });
    });
});
