document.addEventListener('DOMContentLoaded', function() {
    // 获取所有商品的数量控件
    const quantityControls = document.querySelectorAll('.quantity-controls');

    quantityControls.forEach(function(control) {
        const decreaseButton = control.querySelector('.btn-decrease');
        const increaseButton = control.querySelector('.btn-increase');
        const quantityInput = control.querySelector('input[type="text"]');

        // 减少数量按钮事件监听
        decreaseButton.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {  // 确保数量不小于1
                quantityInput.value = currentValue - 1;
            }
        });

        // 增加数量按钮事件监听
        increaseButton.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            quantityInput.value = currentValue + 1;
        });
    });
});



document.addEventListener('DOMContentLoaded', function() {
    // 获取所有“添加到购物车”按钮
    const addToCartButtons = document.querySelectorAll('.btn-add-to-cart');

    addToCartButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const productItem = button.closest('.product-item');
            const productID = productItem.id;
            const quantity = parseInt(productItem.querySelector('input[type="text"]').value);
            
            // 发送 AJAX 请求到后端
            fetch('/add_to_basket', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_id: productID,
                    quantity: quantity
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);
                } else {
                    alert('添加购物车失败: ' + data.message);
                }
            })
            .catch(error => {
                console.error('添加购物车时出错:', error);
            });
        });
    });
});

