from langchain_core.tools import tool
import re
# ==============================================================================
# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ==============================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"}
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"}
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"}
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "08:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"}
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"}
    ]
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "area": "Mỹ Khê", "stars": 5, "price_per_night": 1_800_000, "rating": 4.5},
        {"name": "Sala Danang Beach", "area": "Mỹ Khê", "stars": 4, "price_per_night": 1_200_000, "rating": 4.3},
        {"name": "Fivitel Danang", "area": "Sơn Trà", "stars": 3, "price_per_night": 650_000, "rating": 4.1},
        {"name": "Memory Hostel", "area": "Hải Châu", "stars": 2, "price_per_night": 250_000, "rating": 4.6},
        {"name": "Christina's Homestay", "area": "Sơn Trà", "stars": 2, "price_per_night": 350_000, "rating": 4.7}
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "area": "Bãi Dài", "stars": 5, "price_per_night": 3_500_000, "rating": 4.4},
        {"name": "Sol by Meliá", "area": "Bãi Trường", "stars": 4, "price_per_night": 1_500_000, "rating": 4.2},
        {"name": "Lahana Resort", "area": "Dương Đông", "stars": 3, "price_per_night": 800_000, "rating": 4.0},
        {"name": "9Station Hostel", "area": "Dương Đông", "stars": 2, "price_per_night": 200_000, "rating": 4.5}
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "area": "Quận 1", "stars": 5, "price_per_night": 2_800_000, "rating": 4.3},
        {"name": "Liberty Central", "area": "Quận 1", "stars": 4, "price_per_night": 1_400_000, "rating": 4.1},
        {"name": "Cochin Zen Hotel", "area": "Quận 3", "stars": 3, "price_per_night": 550_000, "rating": 4.4},
        {"name": "The Common Room", "area": "Quận 1", "stars": 2, "price_per_night": 180_000, "rating": 4.6}
    ]
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    flights = FLIGHTS_DB.get((origin, destination))
    direction = f"từ {origin} đến {destination}"
    
    # Nếu không thấy, thử tra cứu chiều ngược (yêu cầu từ ảnh)
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        direction = f"từ {destination} đến {origin} (Tra cứu ngược chiều)"
    
    if not flights:
        return f"Không tìm thấy chuyến bay nào {direction}."
    
    result = [f"--- Chuyến bay {direction} ---"]
    for f in flights:
        price_fmt = f"{f['price']:,}đ".replace(",", ".")
        result.append(
            f"- {f['airline']} ({f['class']}): {f['departure']} -> {f['arrival']} | Giá: {price_fmt}"
        )
    return "\n".join(result)    

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn tại {city}."
    
    # Lọc theo giá tối đa
    filtered_hotels = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
    
    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night:,}đ/đêm."
    
    # Sắp xếp theo rating giảm dần (yêu cầu từ ảnh)
    sorted_hotels = sorted(filtered_hotels, key=lambda x: x['rating'], reverse=True)
    
    result = [f"--- Khách sạn tại {city} (Giá dưới {max_price_per_night:,}đ) ---"]
    for h in sorted_hotels:
        price_fmt = f"{h['price_per_night']:,}đ".replace(",", ".")
        result.append(
            f"- {h['name']} ({h['stars']}*): {h['rating']}/5 sao | Khu vực: {h['area']} | Giá: {price_fmt}/đêm"
        )
    return "\n".join(result)
    pass

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, 
      định dạng 'tên_khoản_số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        # Tách chuỗi bằng dấu phẩy, sau đó tách tên và số tiền bằng dấu hai chấm
        expense_items = [item.strip() for item in expenses.split(",") if ":" in item]
        if not expense_items:
            return "Lỗi: Định dạng expenses không đúng. Vui lòng dùng 'tên:số_tiền'."

        total_spent = 0
        detail_lines = []
        
        for item in expense_items:
            name, amount = item.split(":")
            # Loại bỏ các ký tự không phải số trong amount để tránh lỗi
            clean_amount = int(re.sub(r'[^\d]', '', amount))
            total_spent += clean_amount
            detail_lines.append(f"- {name.replace('_', ' ').capitalize()}: {clean_amount:,}đ".replace(",", "."))
        
        remaining = total_budget - total_spent
        
        report = [
            "Bảng chi phí chi tiết:",
            *detail_lines,
            "---",
            f"Tổng chi: {total_spent:,}đ".replace(",", "."),
            f"Ngân sách ban đầu: {total_budget:,}đ".replace(",", "."),
            f"Còn lại: {remaining:,}đ".replace(",", ".")
        ]
        
        if remaining < 0:
            report.append(f"⚠️ CẢNH BÁO: Vượt ngân sách {-remaining:,}đ! Cần điều chỉnh lại.".replace(",", "."))
            
        return "\n".join(report)
    
    except Exception as e:
        return f"Lỗi xử lý tính toán: {str(e)}. Vui lòng kiểm tra lại định dạng input."
