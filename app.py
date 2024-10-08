from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data for bike and customers
# Sample data for bike and customers
bike = [
    {"id": 1, "brand": "Toyota", "model": "Camry", "available": True},
    {"id": 2, "brand": "Honda", "model": "Accord", "available": True},
    {"id": 3, "brand": "Ford", "model": "Mustang", "available": False},
    {"id": 4, "brand": "Chevrolet", "model": "Cruze", "available": True},
    {"id": 5, "brand": "Nissan", "model": "Altima", "available": True},
    {"id": 6, "brand": "BMW", "model": "3 Series", "available": True},
    # Add more bike as needed
]


customers = []

@app.route("/")
def index():
    return render_template("index.html", bike=bike)

@app.route("/customer")
def customer():
    return render_template("customer.html")

@app.route("/add_customer", methods=["POST"])
def add_customer():
    customer_name = request.form.get("customer_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    selected_bike_id = int(request.form.get("bike_id"))

    # Check if the selected bike is available
    selected_bike = next((bike for bike in bike if bike["id"] == selected_bike_id), None)
    if selected_bike and selected_bike["available"]:
        # Mark the selected bike as unavailable
        selected_bike["available"] = False

        # Add customer to the list with more details
        customers.append({
            "name": customer_name,
            "email": email,
            "phone": phone,
            "bike": selected_bike
        })

        return redirect(url_for("index"))
    else:
        return "Selected bike is not available."

# ...
if __name__ == "__main__":
    app.run(debug=True)
