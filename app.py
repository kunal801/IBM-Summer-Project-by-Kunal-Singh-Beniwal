#!/usr/bin/env python
# coding: utf-8

# In[13]:


get_ipython().system('pip install -q opencv-python matplotlib pillow')
get_ipython().system('pip install -q git+https://github.com/facebookresearch/segment-anything.git')
get_ipython().system('pip install -q git+https://github.com/huggingface/diffusers.git')
get_ipython().system('pip install -q transformers accelerate')
get_ipython().system('pip install -q gradio')
get_ipython().system('pip install -q scikit-image')


# In[14]:


import gradio as gr
import pandas as pd
import numpy as np
import random
import time
import io


# In[15]:


def ai_suggest_price(category, cost_price):
    margin_map = {
        "electronics": 0.25,
        "fashion": 0.5,
        "grocery": 0.15,
        "furniture": 0.4,
        "other": 0.2
    }
    margin = margin_map.get(category.lower(), 0.3)
    return round(float(cost_price) * (1 + margin), 2)

inventory_store = {}


# In[16]:


def get_inventory_df():
    df = pd.DataFrame(list(inventory_store.values()))
    if not df.empty:
        df["Total Cost"] = df["Quantity"] * df["Cost Price"]
        df["Total Revenue"] = df["Quantity"] * df["Discounted Price"]
        df["Profit"] = df["Total Revenue"] - df["Total Cost"]
    return df

def update_inventory(item_id, item, category, quantity, cost_price, selling_price, description, discount=0.0):
    cost_price = float(cost_price)
    selling_price = float(selling_price)
    discount = float(discount)
    quantity = int(quantity)

    discounted_price = selling_price * (1 - discount / 100)

    inventory_store[item_id] = {
        "Item ID": item_id,
        "Item": item,
        "Category": category,
        "Quantity": quantity,
        "Cost Price": cost_price,
        "Selling Price": selling_price,
        "Discount (%)": discount,
        "Discounted Price": discounted_price,
        "Description": description,
    }
    return get_inventory_df()

def delete_item(item_id):
    inventory_store.pop(item_id, None)
    return get_inventory_df()


# In[17]:


def import_data(file):
    ext = file.name.split(".")[-1].lower()
    try:
        if ext in ["xlsx", "xls"]:
            df = pd.read_excel(file.name)
        elif ext == "csv":
            df = pd.read_csv(file.name)
        else:
            return "❌ Unsupported file format. Upload a .csv or .xlsx file."
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

    required_columns = {"Item ID", "Item", "Category", "Quantity", "Cost Price", "Selling Price", "Description"}
    missing = required_columns - set(df.columns)
    if missing:
        return f"⚠️ Missing columns in your file: {', '.join(missing)}. Please correct and re-upload."

    for _, row in df.iterrows():
        update_inventory(
            str(row.get("Item ID", f"auto-{random.randint(1000,9999)}")),
            row.get("Item", ""),
            row.get("Category", "other"),
            row.get("Quantity", 0),
            row.get("Cost Price", 0.0),
            row.get("Selling Price", 0.0),
            row.get("Description", "")
        )
    return get_inventory_df()

def download_inventory():
    df = get_inventory_df()
    if df.empty:
        return None
    out = io.BytesIO()
    df.to_excel(out, index=False)
    out.seek(0)
    return out.read(), "inventory.xlsx"


# In[18]:


def inventory_analytics():
    df = get_inventory_df()
    if df.empty:
        return "⚠️ No inventory data available."

    total_items = len(df)
    total_stock = df["Quantity"].sum()
    total_cost = df["Total Cost"].sum()
    total_revenue = df["Total Revenue"].sum()
    total_profit = df["Profit"].sum()
    top_items = df.sort_values(by="Profit", ascending=False).head(3)

    report = f"""
📊 **Inventory Summary**
────────────────────────────
🧾 **Total Items:** {total_items}
📦 **Total Stock:** {total_stock}
💰 **Total Investment:** ₹{total_cost:,.2f}
📈 **Expected Revenue:** ₹{total_revenue:,.2f}
📊 **Expected Profit:** ₹{total_profit:,.2f}

🔥 **Top Profitable Items:**
{top_items[['Item', 'Profit']].to_string(index=False)}
    """
    return report


# In[19]:


def item_analytics(item_id):
    if item_id not in inventory_store:
        return "❌ Item ID not found."
    item = inventory_store[item_id]
    total_cost = item['Quantity'] * item['Cost Price']
    total_revenue = item['Quantity'] * item['Selling Price']
    profit = total_revenue - total_cost

    report = f"""
📋 **Item Report: {item['Item']}**
────────────────────────────
🔢 Quantity: {item['Quantity']}
💸 Cost Price: ₹{item['Cost Price']:.2f}
💵 Selling Price: ₹{item['Selling Price']:.2f}
💰 Total Cost: ₹{total_cost:.2f}
📈 Revenue: ₹{total_revenue:.2f}
📊 Profit: ₹{profit:.2f}
📝 Description: {item['Description'] or 'N/A'}
    """
    return report


# In[20]:


def ai_recommend_price(category, cost_price):
    if not category or not cost_price:
        return "Provide category and cost price."
    price = ai_suggest_price(category, cost_price)
    return f"🤖 Suggested Optimal Selling Price: ₹{price}"

with gr.Blocks(css="""
body { background-color: #ffffff; color: #333; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
.gr-button { background-color: #ff6600 !important; color: #fff !important; font-weight: 600; border-radius: 14px; padding: 10px 20px; }
input, textarea, .gr-textbox textarea { border: 1px solid #ddd; border-radius: 14px; padding: 10px; }
table { font-size: 14px; }
""") as app:

    gr.Markdown("""# AI Merchant Inventory
### Designed & Developed by Kunal Singh Beniwal (22BCE2174)
A inventory management system powered by AI. Managed for actionable insights and pricing intelligence.
""")

    with gr.Row():
        with gr.Column():
            item_id = gr.Textbox(label="🔖 Item ID (Unique Key)")
            item = gr.Textbox(label="📦 Item Name")
            category = gr.Textbox(label="🗂️ Category")
            quantity = gr.Number(label="🔢 Quantity")
            cost_price = gr.Number(label="💸 Cost Price (₹)")
            selling_price = gr.Number(label="💵 Selling Price (₹)")
            description = gr.Textbox(label="📝 Description (Optional)", lines=2)

            with gr.Row():
                add_btn = gr.Button("➕ Add / Update Item")
                delete_btn = gr.Button("🗑️ Delete Item")

        with gr.Column():
            inventory_table = gr.Dataframe(label="📋 Inventory View", interactive=False)
            search_box = gr.Textbox(label="🔍 Search Item by ID")
            search_output = gr.Textbox(label="🔎 Item Analytics", lines=10)
            ai_btn = gr.Button("🤖 Suggest Selling Price")
            ai_output = gr.Textbox(label="AI Price Suggestion")
            analytics_btn = gr.Button("📊 Inventory Report")
            analytics_output = gr.Textbox(label="📈 Analytics Overview", lines=12)
            file_input = gr.File(label="📁 Upload Inventory File (.csv or .xlsx)")
            import_btn = gr.Button("📥 Import File to Inventory")
            export_btn = gr.Button("📤 Download Inventory Dataset")
            file_download = gr.File(label="📥 Downloaded Inventory File")

    add_btn.click(update_inventory, [item_id, item, category, quantity, cost_price, selling_price, description], inventory_table)
    delete_btn.click(delete_item, [item_id], inventory_table)
    analytics_btn.click(inventory_analytics, [], analytics_output)
    search_box.change(item_analytics, [search_box], search_output)
    ai_btn.click(ai_recommend_price, [category, cost_price], ai_output)
    import_btn.click(import_data, [file_input], inventory_table)
    export_btn.click(download_inventory, [], file_download)

app.launch(share=True)

