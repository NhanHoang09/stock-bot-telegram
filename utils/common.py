"""
Common utility functions used across the bot
"""

def get_development_message(command_name: str, description: str = "") -> str:
    """
    Tạo thông báo "tính năng đang phát triển" có thể tái sử dụng
    
    Args:
        command_name: Tên command (ví dụ: "/etf", "/analysis")
        description: Mô tả ngắn về chức năng (ví dụ: "hiển thị danh sách ETF")
    
    Returns:
        str: Thông báo HTML format
    """
    reply = "🚧 <b>Tính năng đang phát triển</b>\n\n"
    
    if description:
        reply += f"📊 Command {command_name} ({description}) đang được kiểm tra và cập nhật."
    else:
        reply += f"📊 Command {command_name} đang được kiểm tra và cập nhật."
    
    return reply


def get_error_message(error: str, context: str = "") -> str:
    """
    Tạo thông báo lỗi có thể tái sử dụng
    
    Args:
        error: Thông báo lỗi
        context: Ngữ cảnh lỗi (tùy chọn)
    
    Returns:
        str: Thông báo lỗi HTML format
    """
    reply = "❌ <b>Có lỗi xảy ra</b>"
    
    if context:
        reply += f" khi {context}"
    
    reply += f": {error}"
    
    return reply


def get_success_message(message: str) -> str:
    """
    Tạo thông báo thành công có thể tái sử dụng
    
    Args:
        message: Thông báo thành công
    
    Returns:
        str: Thông báo thành công HTML format
    """
    return f"✅ {message}"


def get_info_message(message: str) -> str:
    """
    Tạo thông báo thông tin có thể tái sử dụng
    
    Args:
        message: Thông báo thông tin
    
    Returns:
        str: Thông báo thông tin HTML format
    """
    return f"ℹ️ {message}" 