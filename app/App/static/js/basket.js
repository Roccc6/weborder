document.addEventListener('DOMContentLoaded', function() {
    // 获取移除按钮和结算按钮
    const removeButton = document.querySelector('.btn-remove');
    const checkoutButton = document.querySelector('.btn-checkout');
    if (!removeButton || !checkoutButton) {
        return;
    }
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
    // 监听结算按钮点击事件
    checkoutButton.addEventListener('click', function() {
        const selectedItems = document.querySelectorAll('.checkbox-input:checked');
        if (selectedItems.length > 0) {
            // 这里你可以加入结算逻辑
            alert('选中的商品已经准备结算。');
            // 在这里调用结算逻辑，比如向服务器发送请求结算选中的商品
        } else {
            alert('请先选择要结算的商品。');
        }
    });
});
