import requests
from bs4 import BeautifulSoup
import streamlit as st
import re
import pandas as pd

def scrape_yahoo_shopping(search_term):
    url = f"https://shopping.yahoo.co.jp/search?p={search_term}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 商品名と価格を抽出
    items = soup.find_all("li", class_="LoopList__item")
    products = []
    for item in items:
        name = item.find("span", class_=re.compile("^SearchResultItemTitle_SearchResultItemTitle__name__"))
        price = item.find("span", class_=re.compile("^SearchResultItemPrice_SearchResultItemPrice__value__"))
        if name and price:
            products.append({
                "商品名": name.text.strip(),
                "価格": price.text.strip()
            })
    return products

def main():
    st.title("ヤフーショッピング検索結果")

    search_term = st.text_input("検索ワードを入力してください")
    search_button = st.button("検索")
    
    if search_button:
        if search_term:
            products = scrape_yahoo_shopping(search_term)
            if products:
                # データフレームの作成
                df = pd.DataFrame(products)
                
                # 価格を数値に変換
                df['価格'] = df['価格'].str.replace('円', '').str.replace(',', '').astype(int)
                
                # 価格で昇順にソート
                df = df.sort_values('価格')
                
                # 価格を元の表示形式に戻す
                df['価格'] = df['価格'].apply(lambda x: f"{x:,}円")
                
                # Streamlitで表を表示（インデックスを非表示に）
                st.dataframe(df.reset_index(drop=True), width=1200, height=800, hide_index=True)
            else:
                st.warning("商品が見つかりませんでした。")
        else:
            st.warning("検索欄が空です")

if __name__ == "__main__":
    main()