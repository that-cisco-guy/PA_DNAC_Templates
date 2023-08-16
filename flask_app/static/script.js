const copyButton = document.getElementById("btn-copy");

copyButton.addEventListener('click', (event) => {
    const content = document.getElementById("content-copy").textContent;
    navigator.clipboard.writeText(content);
} )