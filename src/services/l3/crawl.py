import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO 

HEADER = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

def crawl_data(url: str) -> pd.DataFrame:
    """
    Crawl data from the given URL and return as a Pandas DataFrame.
    """
    
    response = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(response.text, "html.parser")
    div = soup.find("div", class_="major-table pc-table none-backgroud")

    if div:
        html_str = str(div)
        tables = pd.read_html(StringIO(html_str))
        if tables:
            return tables[0]
        else:
            print("Không tìm thấy bảng trong div")
            return pd.DataFrame()
    else:
        print("Không tìm thấy div")
        return pd.DataFrame()

if __name__ == "__main__":
    url = "https://diemthi.tuyensinh247.com/de-an-tuyen-sinh/dai-hoc-su-pham-ky-thuat-tphcm-SPK.html#diem-hoc-ba-6035"
    df = crawl_data(url)
    df.to_excel("../../../data/spk_hb.xlsx", index=False)