const storysContainer = document.getElementById("storys");
const scrollAmount = 120;

document.querySelector(".arrow.left").onclick = () => {storysContainer.scrollBy({ left: -scrollAmount, behavior: 'smooth' });};
document.querySelector(".arrow.right").onclick = () => {storysContainer.scrollBy({ left: scrollAmount, behavior: 'smooth' });};
