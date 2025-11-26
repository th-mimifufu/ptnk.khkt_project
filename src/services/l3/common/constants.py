BASE_SUBJECT_MAP = {
    "Toán": "toan", 
    "Lý": "ly", 
    "Hóa": "hoa", 
    "Văn": "van", 
    "Anh": "anh",
    "Sinh": "sinh", 
    "Sử": "su", 
    "Địa": "dia", 
    "Tin": "tin",
    "GDKT&PL": "gdkt_pl",
}

NANG_KHIEU_MAP = {
    "Vẽ TT": "ve_tt",
    "Vẽ DT": "ve_dt"
}

FULL_SUBJECT_MAP = {
    **BASE_SUBJECT_MAP,
    **NANG_KHIEU_MAP
}

TO_HOP_SUBJECTS = {
    # Khối A (Toán - Lý - Hóa - Sinh - Anh)
    "A00": ["Toán", "Lý", "Hóa"],
    "A01": ["Toán", "Lý", "Anh"],
    "A02": ["Toán", "Lý", "Sinh"],
    "A03": ["Toán", "Lý", "Sử"],
    "A04": ["Toán", "Lý", "Địa"],
    "A05": ["Toán", "Hóa", "Sử"],
    "A06": ["Toán", "Hóa", "Địa"],
    "A07": ["Toán", "Sử", "Địa"],
    "A08": ["Toán", "Sử", "GDKTPL"],
    "A09": ["Toán", "Địa", "GDKTPL"],
    "A10": ["Toán", "Lý", "GDKTPL"],
    "A11": ["Toán", "Hóa", "GDKTPL"],

    # Khối B (Toán - Hóa - Sinh)
    "B00": ["Toán", "Hóa", "Sinh"],
    "B02": ["Toán", "Sinh", "Địa"],
    "B03": ["Toán", "Sinh", "Ngữ"],
    "B04": ["Toán", "Sinh", "GDKTPL"],
    "B08": ["Toán", "Sinh", "Anh"],

    # Khối C (Văn - Sử - Địa)
    "C00": "Văn, Sử, Địa lí",
    "C01": "Văn, Toán, Vật lí",
    "C02": "Văn, Toán, Hóa học",
    "C03": "Văn, Toán, Sử",
    "C04": "Văn, Toán, Địa lí",
    "C05": "Văn, Vật lí, Hóa học",
    "C08": "Văn, Hóa học, Sinh học",
    "C12": "Văn, Sử, Sinh học",
    "C13": "Văn, Sinh học, Địa lí",
    "C14": "Văn, Toán, GDKTPL",
    "C17": "Văn, Hóa học, GDKTPL",
    "C19": "Văn, Sử, GDKTPL",
    "C20": "Văn, Địa lí, GDKTPL",

    # Khối D (Toán - Văn - Anh)
    "D01": ["Văn", "Toán", "Anh"],
    "D02": ["Văn", "Toán", "Tiếng Nga"],
    "D03": ["Văn", "Toán", "Tiếng Pháp"],
    "D04": ["Văn", "Toán", "Tiếng Trung"],
    "D05": ["Văn", "Toán", "Tiếng Đức"],
    "D06": ["Văn", "Toán", "Tiếng Nhật"],
    "D07": ["Toán", "Hóa", "Anh"],
    "D08": ["Toán", "Sinh", "Anh"],
    "D09": ["Toán", "Sử", "Anh"],
    "D10": ["Toán", "Địa", "Anh"],
    "D11": ["Văn", "Lý", "Anh"],
    "D12": ["Văn", "Hóa", "Anh"],
    "D12": ["Văn", "Hóa", "Anh"],
    "D13": ["Văn", "Sinh", "Anh"],
    "D14": ["Văn", "Sử", "Anh"],
    "D15": ["Văn", "Địa", "Anh"],
    "D20": ["Toán", "Địa", "Tiếng Trung"],
    "D21": ["Toán", "Hóa", "Tiếng Đức"],
    "D22": ["Toán", "Hóa", "Tiếng Nga"],
    "D23": ["Toán", "Hóa", "Tiếng Nhật"],
    "D24": ["Toán", "Hóa", "Tiếng Pháp"],
    "D25": ["Toán", "Hóa", "Tiếng Trung"],
    "D26": ["Toán", "Lý", "Tiếng Đức"],
    "D27": ["Toán", "Lý", "Tiếng Nga"],
    "D28": ["Toán", "Lý", "Tiếng Nhật"],
    "D29": ["Toán", "Lý", "Tiếng Pháp"],
    "D30": ["Toán", "Lý", "Tiếng Trung"],
    "D31": ["Toán", "Sinh", "Tiếng Đức"],
    "D32": ["Toán", "Sinh", "Tiếng Nga"],
    "D33": ["Toán", "Sinh", "Tiếng Nhật"],
    "D34": ["Toán", "Sinh", "Tiếng Pháp"],
    "D35": ["Toán", "Sinh", "Tiếng Trung"],
    "D42": ["Văn", "Địa", "Tiếng Nga"],
    "D43": ["Văn", "Địa", "Tiếng Nhật"],
    "D44": ["Văn", "Địa", "Tiếng Pháp"],
    "D45": ["Văn", "Địa", "Tiếng Trung"],
    "D55": ["Văn", "Lý", "Tiếng Trung"],
    "D63": ["Văn", "Sử", "Tiếng Nhật"],
    "D64": ["Văn", "Sử", "Tiếng Pháp"],
    "D65": ["Văn", "Sử", "Tiếng Trung"],
    "D66": ["Văn", "GDKTPL", "Anh"],
    "D68": ["Văn", "GDKTPL", "Tiếng Nga"],
    "D69": ["Văn", "GDKTPL", "Tiếng Nhật"],
    "D70": ["Văn", "GDKTPL", "Tiếng Pháp"],
    "D71": ["Văn", "GDKTPL", "Tiếng Trung"],
    "D84": ["Toán", "Anh", "GDKTPL"],

    # Khối X
    "X01": ["Văn", "Toán", "GDKTPL"],
    "X02": ["Toán", "Văn", "Tin"],
    "X03": ["Toán", "Văn", "Công nghệ"],
    "X04": ["Toán", "Văn", "Công nghệ"],
    "X06": ["Toán", "Lý", "Tin"],

    "X08": ["Toán", "Lý", "Công nghệ"],
    "X10": ["Toán", "Hóa", "Tin"],
    "X11": ["Toán", "Hóa", "Công nghệ"],
    "X12": ["Toán", "Hóa", "Công nghệ"],
    "X26": ["Toán", "Anh", "Tin"],
    "X27": ["Toán", "Anh", "Công nghệ"],
    "X28": ["Toán", "Anh", "Công nghệ"],
    "X60": ["Toán", "Lý", "Tin"],
    "X61": ["Toán", "Sinh", "Công nghệ"],

    # Khối H (Khối nghệ thuật)
    "H01": ["Toán", "Văn", "Vẽ mỹ thuật"],
    "H02": ["Toán", "Vẽ mỹ thuật", "Vẽ trang trí"],
    "H04": ["Toán", "Anh", "Vẽ năng khiếu"],
    "H06": ["Văn", "Anh", "Vẽ mỹ thuật"],
    "H07": ["Toán", "Vẽ mỹ thuật", "Vẽ trang trí"],
    "H08": ["Văn", "Sử", "Vẽ mỹ thuật"],


    # Khối M (Khối năng khiếu)
    "M00": ["Văn", "Toán", "Đọc diễn cảm", "Hát"],
    "M01": ["Văn", "Sử", "Năng khiếu"],
    "M02": ["Toán", "Năng khiếu 1", "Năng khiếu 2"],
    "M03": ["Văn", "Năng khiếu 1", "Năng khiếu 2"],
    "M04": ["Toán", "Đọc diễn cảm", "Hát - Múa"],
    "M09": ["Toán", "Đọc diễn cảm", "Hát"],
    "M10": ["Toán", "Anh", "Năng khiếu 1"],
    "M11": ["Văn", "Năng khiếu báo chí", "Anh"],
    "M12": ["Toán", "Sinh", "Năng khiếu"],
    "M13": ["Văn", "Năng khiếu báo chí", "Toán"],
    "M14": ["Văn", "Năng khiếu báo chí", "Toán"],

    # Khối V (Khối Vẽ)
    "V02": ["Toán", "Anh", "Vẽ mỹ thuật"],
    "V03": ["Toán", "Hóa", "Vẽ mỹ thuật"],
    "V04": ["Toán", "Văn", "Vẽ mỹ thuật"],
    "V05": ["Văn", "Lý", "Vẽ mỹ thuật"],
    "V06": ["Toán", "Địa", "Vẽ mỹ thuật"],
    "V10": ["Toán", "Tiếng Pháp", "Vẽ mỹ thuật"],
    "V11": ["Toán", "Tiếng Trung", "Vẽ mỹ thuật"],

    # Khối T (Khối Thể thao)
    "T00": ["Toán", "Sinh", "Năng khiếu TDTT"],
    "T01": ["Toán", "Văn", "Năng khiếu TDTT"],
    "T02": ["Văn", "Sinh", "Năng khiếu TDTT"],
    "T03": ["Văn", "Địa", "Năng khiếu TDTT"],
    "T04": ["Toán", "Lý", "Năng khiếu TDTT"],
    "T05": ["Văn", "GDKTPL", "Năng khiếu TDTT"],

    # Khối N
    "N00": ["Văn", "Năng khiếu Âm nhạc 1", "Năng khiếu Âm nhạc 2"],
    "N01": ["Văn", "xướng âm", "biểu diễn nghệ thuật"],
    "N02": ["Văn", "Ký xướng âm", "Hát hoặc biểu diễn nhạc cụ"],
    "N05": ["Văn", "Xây dựng kịch bản sự kiện", "Năng khiếu"]
}