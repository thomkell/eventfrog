from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64
from eventfrog_data import get_category_sales, plot_category_sales

app = Flask(__name__)

filepath = '/Users/thomaskeller/Dropbox/RK/Eventfrog/2025.xlsx'  # Define the file path for 2025 data

@app.route("/")
def index():
    # Category Sales
    sold_category_sales = get_category_sales(filepath)
    plt_category_sales = plot_category_sales(sold_category_sales)
    img_category_sales = io.BytesIO()
    plt_category_sales.savefig(img_category_sales, format='png')
    img_category_sales.seek(0)
    plot_url_category_sales = base64.b64encode(img_category_sales.read()).decode('utf-8')
    plt.close()

    return render_template('index.html', plot_url_category_sales=plot_url_category_sales)

if __name__ == "__main__":
    app.run(debug=True)
