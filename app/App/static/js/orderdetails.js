document.querySelectorAll('.review-link').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const itemName = this.dataset.itemName;
        const itemId = this.dataset.itemId;

        document.getElementById('product-name').textContent = itemName;
        document.getElementById('item-id').value = itemId;
        document.getElementById('review-form').classList.remove('hidden');
    });
});

document.getElementById('cancel-button').addEventListener('click', function() {
    document.getElementById('review-form').classList.add('hidden');
});

document.querySelector('#review').addEventListener('submit', function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    comment = formData.get('comment');
    const orderId = document.getElementById('orderid').dataset.orderId;
    const productId = document.getElementById('item-id').value;
    fetch('/review', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            order_id: orderId,
            comment: comment
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            window.location.reload();
        } else {
            alert('评论失败: ' + data.message);
        }
    });
});
