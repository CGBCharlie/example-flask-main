from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the expanded data into a pandas DataFrame
data = pd.read_csv('calculator.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    product_id = request.form['product_id']
    current_inventory = float(request.form['current_inventory'])
    month = request.form['month']

    product_data = data[data['id'] == int(product_id)].to_dict('records')

    if not product_data:
        return jsonify({'error': 'Product not found'}), 404

    product_data = product_data[0]
    product_name = product_data['product_name']
    month_sales = product_data[f'{month[:3].lower()}']
    month_inventory = product_data[f'{month[:3].lower()}Inv']

    # Calculate how much inventory to buy
    inventory_to_buy = month_sales - current_inventory + month_inventory
    if inventory_to_buy < 0:
        inventory_to_buy = 0

    # Return the calculated data
    return jsonify({
        'product_id': product_id,
        'product_name': product_name,
        'predicted_sales': month_sales,
        'inventory_to_buy': inventory_to_buy
    })

if __name__ == '__main__':
    app.run(debug=True)
