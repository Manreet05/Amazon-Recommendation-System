import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import tkinter as tk
from tkinter import messagebox, ttk

# ---------- CONFIG ----------
CSV_FILENAME = "recommendation_products.csv"
CHROMEDRIVER_PATH = r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Base URLs
amazon_sections = {
    "Electronics": "https://www.amazon.in/s?i=electronics&page={}",
    "Smartphones": "https://www.amazon.in/s?i=electronics&rh=n%3A1389401031&page={}",
    "Laptops": "https://www.amazon.in/s?i=computers&rh=n%3A1375424031&page={}"
}

# ---------- SCRAPER ----------
def scrape_amazon_and_write_to_csv(base_url):
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price", "Rating", "Availability", "Link", "Image"])

        for page in range(1, 3):  # scrape 2 pages for demo
            driver.get(base_url.format(page))
            time.sleep(3)

            products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
            for p in products:
                try:
                    title = p.find_element(By.TAG_NAME, "h2").text.strip()
                    link = p.find_element(By.TAG_NAME, "a").get_attribute("href")

                    try:
                        price = p.find_element(By.CLASS_NAME, "a-price-whole").text
                    except:
                        price = "N/A"

                    try:
                        rating = p.find_element(By.CLASS_NAME, "a-icon-alt").text
                    except:
                        rating = "N/A"

                    try:
                        image = p.find_element(By.TAG_NAME, "img").get_attribute("src")
                    except:
                        image = "N/A"

                    availability = "In Stock"

                    writer.writerow([title, price, rating, availability, link, image])

                except Exception:
                    pass

    driver.quit()
    messagebox.showinfo("Scraping Done", f"Products saved to {CSV_FILENAME}")

# ---------- RECOMMENDER ----------
def get_recommendations(product_name, min_price, max_price):
    df = pd.read_csv(CSV_FILENAME)

    if df.empty or df["Title"].dropna().empty:
        return []

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["Title"].astype(str))
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    idx = df[df["Title"].str.contains(product_name, case=False, na=False)].index
    if not idx.empty:
        idx = idx[0]
        sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
        product_indices = [i[0] for i in sim_scores]

        def parse_price(x):
            try:
                return float(str(x).replace(",", ""))
            except:
                return 0

        df["PriceVal"] = df["Price"].apply(parse_price)

        filtered = df[(df.index.isin(product_indices)) &
                      (df["PriceVal"] >= min_price) &
                      (df["PriceVal"] <= max_price)]

        return filtered[["Title", "Price", "Rating", "Link"]].values.tolist()
    else:
        return []

# ---------- GUI ----------
def scrape_data():
    choice = section_choice.get()
    base_url = amazon_sections[choice]
    scrape_amazon_and_write_to_csv(base_url)

def show_recommendations():
    try:
        search_term = search_entry.get().strip()
        min_price = float(min_price_entry.get() or 0)
        max_price = float(max_price_entry.get() or 1e9)
        recommendations = get_recommendations(search_term, min_price, max_price)

        results_text.delete("1.0", tk.END)
        if recommendations:
            for product in recommendations:
                results_text.insert(tk.END, f"Title: {product[0]}\n")
                results_text.insert(tk.END, f"Price: {product[1]}\n")
                results_text.insert(tk.END, f"Rating: {product[2]}\n")
                results_text.insert(tk.END, f"Link: {product[3]}\n")
                results_text.insert(tk.END, "-" * 80 + "\n")
        else:
            results_text.insert(tk.END, "No recommendations found.\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Amazon Product Recommendation System (Selenium)")
root.geometry("900x700")
root.configure(bg="#f4f4f4")

# Section choice
tk.Label(root, text="Choose Amazon Section:", bg="#f4f4f4", font=("Arial", 12, "bold")).pack(pady=5)
section_choice = tk.StringVar(value="Electronics")
ttk.Combobox(root, textvariable=section_choice, values=list(amazon_sections.keys()), width=30).pack()

# Scrape Button
scrape_button = tk.Button(root, text="Scrape Data", command=scrape_data, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
scrape_button.pack(pady=10)

# Search Section
tk.Label(root, text="Product Search Term:", bg="#f4f4f4", font=("Arial", 11)).pack()
search_entry = tk.Entry(root, width=40)
search_entry.pack()

tk.Label(root, text="Minimum Price:", bg="#f4f4f4", font=("Arial", 11)).pack()
min_price_entry = tk.Entry(root, width=20)
min_price_entry.pack()

tk.Label(root, text="Maximum Price:", bg="#f4f4f4", font=("Arial", 11)).pack()
max_price_entry = tk.Entry(root, width=20)
max_price_entry.pack()

recommend_button = tk.Button(root, text="Get Recommendations", command=show_recommendations, bg="#2196F3", fg="white", font=("Arial", 11, "bold"))
recommend_button.pack(pady=10)

# Results
results_text = tk.Text(root, height=25, width=100, wrap="word")
results_text.pack(pady=10)

root.mainloop()
