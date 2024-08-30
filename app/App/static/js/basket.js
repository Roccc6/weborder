document.addEventListener('DOMContentLoaded', function() {
    // 获取移除按钮和结算按钮
    const removeButton = document.querySelector('.btn-remove');
    const submitButton = document.querySelector('.btn-submit');
    const emptyButton = document.querySelector('.btn-empty');
    // 监听清空购物车按钮点击事件
    emptyButton.addEventListener('click', function() {
        if (confirm('你确定要清空购物车吗？')) {
            fetch('/empty_basket', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);
                    // 延迟移除
                    setTimeout(function() {
                        window.location.reload();
                    }, 500);
                } else {
                    alert('清空购物车失败: ' + data.message);
                }
            })
            .catch(error => {
                console.error('清空购物车时出错:', error);
            });
        }
    });
    // 监听移除按钮点击事件
    removeButton.addEventListener('click', function() {
        // 获取所有选中的复选框
        const selectedItems = document.querySelectorAll('.checkbox-input:checked');
        let removeItems = [];
        selectedItems.forEach(function(checkbox) {
            productinfo = checkbox.nextElementSibling;
            productId = productinfo.id;
            removeItems.push(productId);
        });
        if (selectedItems.length > 0) {
            // 询问用户确认移除
            if (confirm('你确定要移除选中的商品吗？')) {
                selectedItems.forEach(function(checkbox) {
                    const cartItem = checkbox.closest('.cart-item');
                    if (cartItem) {
                        // 删除选中的商品
                        cartItem.style.transition = 'opacity 0.5s ease-out';
                        cartItem.style.opacity = 0;
                        fetch('/remove_from_basket', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                product_id: removeItems
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                alert(data.message);                                // 延迟移除
                                setTimeout(function() {
                                    cartItem.remove();
                                    window.location.reload();
                                }, 500);
                            } else {
                                alert('移除商品失败: ' + data.message);
                            }
                        })
                    }
                else {
                    alert('请先选择要移除的商品。');
                }
            }); 
        }}     
    });
    // 监听提交订单按钮点击事件
    submitButton.addEventListener('click', function() {
        //获取运输方式
        const shippingSelect = document.getElementById('shipping');
        const currentShippingMethod = shippingSelect.value;
        console.log('当前选中的运输方式是:', currentShippingMethod);
        fetch('/submit_order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                shipping_method: currentShippingMethod
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
                // 延迟移除
                setTimeout(function() {
                    window.location.reload();
                }, 500);
            } else {
                alert('提交订单失败: ' + data.message);
            }
        })
    });
});
