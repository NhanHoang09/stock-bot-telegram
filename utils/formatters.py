def format_vnd(amount):
    """Format số tiền theo định dạng VNĐ đầy đủ"""
    if amount is None:
        return "N/A"
    
    try:
        amount = float(amount)
        # Hiển thị số tiền đầy đủ với dấu phẩy ngăn cách hàng nghìn
        return f"{amount:,.0f}"
    except:
        return "N/A" 