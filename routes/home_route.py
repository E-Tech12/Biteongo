from flask import Blueprint,render_template,redirect
from flask_login import login_required
home_auth = Blueprint("home_auth",__name__)

@home_auth.route("/home")
@login_required
def home():
    foods = [
        {
            "name": "Pizza",
            "price": "₦5,000.00",
            "image": "pizz.jpg",
            "desc": "Delicious cheese pizza with fresh toppings."
        },
        {
            "name": "Burger",
            "price": "₦5,000.00",
            "image": "burger.jpg",
            "desc": "Juicy beef burger with lettuce and cheese."
        },
        {
            "name": "Shawarma",
            "price": "₦2,000.00",
            "image": "shawarma.jpg",
            "desc": "Loaded shawarma with tasty fillings."
        },
        
        {
            "name": "Doughnuts",
            "price": "500.00",
            "image": "Doughnuts.jpg",
            "desc": "Freshly Based Gazed Doughnuts."
        },
        
        {
            "name": "Eggroll",
            "price": "500.00",
            "image": "eggroll.jpg",
            "desc": "Delicios eggroll with savory filling."
        },
        
        {
            "name": "Meat Pie",
            "price": "700.00",
            "image": "pie.jpg",
            "desc": "Flaky pastry filled with seasoned meat."
        },
        
        {
            "name": "Croissants",
            "price": "500.00",
            "image": "croissants.jpg",
            "desc": "Buttery and flaky croissants."
        },
        
        {
            "name": "Coldstone",
            "price": "2,000.00",
            "image": "coldstone.jpg",
            "desc": "Creamy coldstone ice cream."
        },
                    
        {
            "name": "Chicken Chips",
            "price": "1,500.00",
            "image": "chicken.jpg",
            "desc": "Crispy chicken chips with seasoning."
        },
        
        {
            "name": "parfait",
            "price": "1,500.00",
            "image": "parfait.jpg",
            "desc": "Layered yogurt parfait with fruits and granola."
        },
        
        {
            "name": "Amala",
            "price": "₦300.00",
            "image": "amala.jpg",
            "desc": "Traditional Nigerian amala dish."
        },
                  
        {
            "name": "Eba",
            "price": "₦300.00",
            "image": "eba.jpg",
            "desc": "Traditional Nigerian eba dish."
        },
        
        {
            "name": "fufu",
            "price": "₦300.00",
            "image": "fufuu.jpg",
            "desc": "Traditional Nigerian fufu dish."
        },
        
        
        
        {
            "name": "Pounded yam",
            "price": "₦500.00",
            "image": "pounded.jpg",
            "desc": "Traditional Nigerian pounded yam dish."
        },
                
        {
            "name": "Wheat meal",
            "price": "₦300.00",
            "image": "wheat.jpg",
            "desc": "Traditional Nigerian wheat meal dish."
        },
        
        {
            "name": "Semo",
            "price": "₦300.00",
            "image": "semo.jpg",
            "desc": "Traditional Nigerian Semo dish."
        },
        
        {
            "name": "Ewedu soup",
            "price": "₦100.00",
            "image": "ewedu.jpg",
            "desc": "Traditional Nigerian ewedu soup."
        },
        
        
        {
            "name": "Egusi soup",
            "price": "₦150.00",
            "image": "egusi.jpg",
            "desc": "Traditional Nigerian egusi soup."
        },
        
        {
            "name": "Efo riro",
            "price": "₦200.00",
            "image": "efo.jpg",
            "desc": "Traditional Nigerian efo riro dish."
        },
        
        {
            "name": "Okro soup",
            "price": "₦100.00",
            "image": "okro.jpg",
            "desc": "Traditional Nigerian okro soup."
        },
        
        {
            "name": "Jollof Rice",
            "price": "₦300.00",
            "image": "jollof.jpg",
            "desc": "Spicy and flavorful jollof rice."
        },
        
        {
            "name": "Fried Rice",
            "price": "₦400.00",
            "image": "friedrice.jpg",
            "desc": "Spicy and flavorful fried rice."
        },
        
        
        {
            "name": "White Rice",
            "price": "₦300.00",
            "image": "whiterice.jpg",
            "desc": "Steamed white rice."
        },
        
        {
            "name": "Ofada Rice",
            "price": "₦300.00",
            "image": "ofada.jpg",
            "desc": "Traditional Nigerian ofada rice."
        },
        
        {
            "name": "Pomo",
            "price": "₦200.00",
            "image": "pomo.jpg",
            "desc": "Delicious pomo."
        },
        
        {
            "name": "Meat",
            "price": "₦200.00",
            "image": "meat.jpg",
            "desc": "Delicious assorted meat."
        },
          
          
        {
            "name": "Chicken",
            "price": "₦1,500.00",
            "image": "chiccken.jpg",
            "desc": "Grilled chicken with spices."
        },
        
        {
            "name": "Full Chicken",
            "price": "₦12,000.00",
            "image": "fullchicken.jpg",
            "desc": "Whole roasted chicken."
        },
        
        {
            "name": "Yogurt",
            "price": "₦1,200.00",
            "image": "milk.jpg",
            "desc": "Creamy and delicious yogurt drink."
        },
        
        {
            "name": "malt",
            "price": "₦1,000.00",
            "image": "malt.jpg",
            "desc": "Fresh strawberries packed with flavor."
        },
        
        {
            "name": "Coke",
            "price": "₦500.00",
            "image": "coke.jpg",
            "desc": "Chilled Coca-Cola beverage."
        },
        
        {
            "name": "Bottle water",
            "price": "₦300.00",
            "image": "water.jpg",
            "desc": "Pure bottled water."
        },
        
        {
            "name": "Sobo",
            "price": "₦500.00",
            "image": "sobo.jpg",
            "desc": "refreshing sobo drink."
        },
        {
            "name": "Fearless",
            "price": "₦700.00",
            "image": "fearless.jpg",
            "desc": "Energy drink to boost your day."
        },
        {
            "name": "Fanta",
            "price": "₦500.00",
            "image": "fanta.jpg",
            "desc": "Chilled fanta beverage."
        },
        
        {
            "name": "Strawberry",
            "price": "₦1,00.00",
            "image": "strawberry.jpg",
            "desc": "Fresh strawberr packed with flavor."
        },
        
        {
            "name": "Vitamilk",
            "price": "₦800.00",
            "image": "vitamilk.jpg",
            "desc": "Nutrituos vitamin drink."
        },
        
        {
            "name": "Chivita",
            "price": "₦1,000.00",
            "image": "vital.jpg",
            "desc": "Refreshing fruit juice drink."
        },
        
        {
            "name": "Monster",
            "price": "₦1,000.00",
            "image": "monster.jpg",
            "desc": "Energy drink to keep you going."
        },
        {
            "name": "Bullet",
            "price": "₦1,500.00",
            "image": "bullet.jpg",
            "desc": "Powerful energy drink."
        }
    ]

    return render_template("base.html", foods=foods)