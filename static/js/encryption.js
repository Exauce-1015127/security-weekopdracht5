function copyToClipboard() {
    var copyText = document.getElementById("keyField");
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices
    document.execCommand("copy");
    alert("Key gekopieerd naar klembord");
}
function downloadData() {
    const key = "{{ key_hex }}";
    const nonce = "{{ encrypted_data.nonce }}";
    const ciphertext = "{{ encrypted_data.ciphertext }}";
    const tag = "{{ encrypted_data.tag }}";

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'key': key,
            'nonce': nonce,
            'ciphertext': ciphertext,
            'tag': tag
        })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'encrypted_data.json';
        document.body.appendChild(a);
        a.click();
        a.remove();
    });
}