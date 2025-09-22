from tkinter import *
import random
import time
import math

root = Tk()
root.geometry("1600x900+0+0")
root.resizable(0, 0)
root.title("Enhanced Restaurant Management System")

# Frames for layout
Tops = Frame(root, bg="white", width=1600, height=50, relief=SUNKEN)
Tops.pack(side=TOP)

f1 = Frame(root, width=900, height=700, relief=SUNKEN)
f1.pack(side=LEFT)

f2 = Frame(root, width=400, height=700, relief=SUNKEN)
f2.pack(side=RIGHT)

f3 = Frame(root, width=900, height=200, relief=SUNKEN, bg="lightgrey")
f3.pack(side=BOTTOM)

# Display local time
localtime = time.asctime(time.localtime(time.time()))
lblinfo = Label(Tops, font=('aria', 30, 'bold'), text="Enhanced Restaurant Ordering System", fg="steel blue", bd=10, anchor='w')
lblinfo.grid(row=0, column=0)
lblinfo = Label(Tops, font=('aria', 20), text=localtime, fg="steel blue", anchor=W)
lblinfo.grid(row=1, column=0)

# Calculator
text_Input = StringVar()
operator = ""

txtdisplay = Entry(f2, font=('ariel', 20, 'bold'), textvariable=text_Input, bd=5, insertwidth=7, bg="white", justify='right')
txtdisplay.grid(columnspan=4)

def btnclick(numbers):
    global operator
    operator = operator + str(numbers)
    text_Input.set(operator)

def clrdisplay():
    global operator
    operator = ""
    text_Input.set("")

def eqals():
    global operator
    try:
        sumup = str(eval(operator))
        text_Input.set(sumup)
    except:
        text_Input.set("Error")
    operator = ""

def add_percentage():
    global operator
    operator = operator + "/100"
    eqals()

def sqrt():
    global operator
    try:
        sumup = str(math.sqrt(float(operator)))
        text_Input.set(sumup)
    except:
        text_Input.set("Error")
    operator = ""

# Buttons for calculator
buttons = [
    ('7', 2, 0, None), ('8', 2, 1, None), ('9', 2, 2, None), ('+', 2, 3, None),
    ('4', 3, 0, None), ('5', 3, 1, None), ('6', 3, 2, None), ('-', 3, 3, None),
    ('1', 4, 0, None), ('2', 4, 1, None), ('3', 4, 2, None), ('*', 4, 3, None),
    ('0', 5, 0, None), ('.', 5, 1, None), ('%', 5, 2, add_percentage),
    ('C', 5, 3, clrdisplay), ('√', 6, 0, sqrt), ('=', 6, 1, eqals)
]

# Generating the buttons
for (text, row, col, cmd) in buttons:
    Button(f2, padx=16, pady=16, bd=4, fg="black", font=('ariel', 20, 'bold'), text=text, bg="powder blue",
           command=lambda t=text: btnclick(t) if cmd is None else cmd).grid(row=row, column=col)

# Food Menu Entries
rand, Fries, Largefries, Burger, Filet, Subtotal, Total, Service_Charge, Drinks, Tax, cost, Cheese_burger = \
    [StringVar() for _ in range(12)]

meal_labels = ["Order No.", "Fries Meal", "Lunch Meal", "Burger Meal", "Pizza Meal", "Cheese Burger", "Drinks"]
meal_vars = [rand, Fries, Largefries, Burger, Filet, Cheese_burger, Drinks]

for i, label in enumerate(meal_labels):
    Label(f1, font=('aria', 16, 'bold'), text=label, fg="steel blue", bd=10, anchor='w').grid(row=i, column=0)
    Entry(f1, font=('ariel', 16, 'bold'), textvariable=meal_vars[i], bd=6, insertwidth=4, bg="powder blue", justify='right').grid(row=i, column=1)

# Cost, tax, and total calculation
def Ref():
    # Random order ID
    rand.set(str(random.randint(12980, 50876)))

    # Meal costs
    meal_prices = [25, 40, 35, 50, 30, 35]
    meal_costs = [float(v.get() or 0) * p for v, p in zip(meal_vars[1:], meal_prices)]

    cost.set("Rs." + str('%.2f' % sum(meal_costs)))
    Tax.set("Rs." + str('%.2f' % (sum(meal_costs) * 0.18)))
    Service_Charge.set("Rs." + str('%.2f' % (sum(meal_costs) * 0.05)))
    Total.set("Rs." + str('%.2f' % (sum(meal_costs) * 1.23))) # Including tax and service charge

    # Display order summary
    order_summary.insert(END, f"Order {rand.get()}:\n")
    for label, cost in zip(meal_labels[1:], meal_costs):
        order_summary.insert(END, f"{label}: Rs. {cost}\n")
    order_summary.insert(END, f"Subtotal: {cost.get()}\nTotal: {Total.get()}\n---\n")

def reset():
    for var in meal_vars + [Subtotal, Total, Service_Charge, Tax, cost]:
        var.set("")
    order_summary.delete(1.0, END)

def qexit():
    root.destroy()

# Summary section
order_summary = Text(f3, font=('aria', 14), height=10, width=70, wrap=WORD)
order_summary.grid(row=0, column=0, padx=10, pady=5)
Label(f3, text="Order Summary", font=('aria', 16, 'bold'), bg="lightgrey").grid(row=0, column=0, sticky=W)

# Price List button
def price():
    price_win = Toplevel(root)
    price_win.title("Price List")
    items = [("Fries Meal", 25), ("Lunch Meal", 40), ("Burger Meal", 35), ("Pizza Meal", 50), ("Cheese Burger", 30), ("Drinks", 35)]
    Label(price_win, font=('aria', 15, 'bold'), text="ITEM", fg="black", bd=5).grid(row=0, column=0)
    Label(price_win, font=('aria', 15, 'bold'), text="PRICE", fg="black").grid(row=0, column=1)
    for i, (item, price) in enumerate(items, 1):
        Label(price_win, font=('aria', 15), text=item, fg="steel blue").grid(row=i, column=0)
        Label(price_win, font=('aria', 15), text="Rs." + str(price), fg="steel blue").grid(row=i, column=1)

Button(f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="TOTAL", bg="powder blue", command=Ref).grid(row=7, column=1)
Button(f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="RESET", bg="powder blue", command=reset).grid(row=7, column=2)
Button(f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="EXIT", bg="powder blue", command=qexit).grid(row=7, column=3)
Button(f1, padx=16, pady=8, bd=10, fg="black", font=('ariel', 16, 'bold'), width=10, text="PRICE", bg="powder blue", command=price).grid(row=7, column=0)

status = Label(f2, font=('aria', 15, 'bold'), width=16, text="-By Amar Kumar", bd=2, relief=SUNKEN)
status.grid(row=7, columnspan=3)

root.mainloop()
