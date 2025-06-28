const textarea = document.querySelector('form textarea');
const btn = document.querySelector('form .btn');

if (textarea && btn) {
    textarea.addEventListener('input', () => {
        btn.disabled = textarea.value.trim() === '';
    });
}