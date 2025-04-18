from fastapi import HTTPException

def calculate_order_cost(drink, cups):
    if cups > 5:
        raise HTTPException(status_code=400, detail="Максимум 5 чашек")
    return drink[2] * cups

def format_order_message(drink, cups, cost):
    return f"Ваш заказ: {cups} x {drink[1]}, стоимость {cost} рублей"