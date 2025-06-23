🧠 AI-Powered Merchant Inventory Dashboard
A smart and intuitive inventory management dashboard designed to help merchants make informed pricing and discounting decisions using AI. Built using Python, Pandas, and Gradio.
🚀 Features
	•	AI Price Suggestion: Automatically recommends selling prices based on product category and cost price.
	•	Inventory Upload: Upload CSV inventory files to analyze product data in real time.
	•	Profit Calculation: View cost price, selling price, profit margin, and profit in absolute terms.
	•	Discount Simulation: Simulate discounts and see their impact on profit and inventory value.
	•	Dashboard Interface: Easy-to-use UI powered by Gradio for seamless interaction.
🧩 Tech Stack
	•	Python 3.10+
	•	Gradio – for building the UI
	•	Pandas / NumPy – for data manipulation
	•	Random / Time – for simulating product recommendations and AI logic
📂 How to Use
	1	Clone the Repository: git clone https://github.com/your-username/ai-merchant-inventory.git
	2	cd ai-merchant-inventory
	3	
	4	Install Dependencies: pip install -r requirements.txt
	5	
	6	Run the App: python AI_Merchant_Inventory.ipynb
	7	
	8	Upload Inventory File: Upload a .csv file with the following columns:
	◦	Product Name
	◦	Category
	◦	Cost Price
	◦	(Optionally) Selling Price
	9	Interact with Dashboard: Use sliders and selectors to analyze profitability, try AI pricing, and simulate discounts.
📸 Screenshot
(Insert screenshot of the dashboard here)
📁 Sample CSV Format
Product Name,Category,Cost Price
LED TV,electronics,15000
T-Shirt,fashion,300
Rice Pack,grocery,700
Wooden Chair,furniture,2500

🧠 Sample AI Logic (Simplified)
margin_map = {
    "electronics": 0.25,
    "fashion": 0.5,
    "grocery": 0.15,
    "furniture": 0.35
}

selling_price = cost_price * (1 + margin_map.get(category.lower(), 0.2))

📌 Notes
	•	The AI logic here is a mock/simulated margin estimator. You can extend it with ML models or real-time market data integration.
	•	Ensure the uploaded CSV follows the format with no missing values.
📜 License
MIT License
