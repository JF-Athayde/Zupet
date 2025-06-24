document.querySelectorAll('.curtir-btn').forEach(button => {
    button.addEventListener('click', async () => {
        const postId = button.getAttribute('data-post-id');
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const likeCountSpan = document.getElementById(`likes-${postId}`);
        const img = button.querySelector('img');

        try {
            const response = await fetch(`/curtir/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            });

            const data = await response.json();

            if (data.success) {
                // Atualiza o número de likes
                likeCountSpan.textContent = data.likes;

                // Troca o ícone do coração para o curtido
                img.src = '/static/assets/icones/coracao-cheio.png';
                img.alt = 'Descurtir';

                // Opcional: desabilita o botão para não permitir mais likes
                button.disabled = true;
            } else {
                console.log('Já Curtiu')
            }
        } catch (error) {
            console.error('Erro ao curtir:', error);
            alert('Erro ao curtir o post. Tente novamente.');
        }
    });
});
