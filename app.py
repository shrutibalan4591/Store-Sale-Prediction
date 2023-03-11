from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import logging

logger = logging.getLogger()
file_handler = logging.FileHandler(filename='LogFiles/logfile.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


X = ['Item_Weight', 'Item_Visibility', 'Item_MRP', 
       'Item_Fat_Content_Low Fat', 'Item_Fat_Content_Non_Edible', 'Item_Fat_Content_Regular', 
       'Item_Type_Baking Goods', 'Item_Type_Breads', 'Item_Type_Breakfast', 'Item_Type_Canned', 'Item_Type_Dairy', 'Item_Type_Frozen Foods',
       'Item_Type_Fruits and Vegetables', 'Item_Type_Hard Drinks', 'Item_Type_Health and Hygiene', 'Item_Type_Household', 'Item_Type_Meat',
       'Item_Type_Others', 'Item_Type_Seafood', 'Item_Type_Snack Foods', 'Item_Type_Soft Drinks', 'Item_Type_Starchy Foods',
       'Item_Category_Drinks', 'Item_Category_Food', 'Item_Category_Non_Consumables', 
       'Outlet_Identifier_OUT010', 'Outlet_Identifier_OUT013', 'Outlet_Identifier_OUT017', 'Outlet_Identifier_OUT018', 
       'Outlet_Identifier_OUT019', 'Outlet_Identifier_OUT027', 'Outlet_Identifier_OUT035', 'Outlet_Identifier_OUT045', 
       'Outlet_Identifier_OUT046', 'Outlet_Identifier_OUT049', 
       'Outlet_Establishment_Year_1985', 'Outlet_Establishment_Year_1987', 'Outlet_Establishment_Year_1997',
       'Outlet_Establishment_Year_1998', 'Outlet_Establishment_Year_1999', 'Outlet_Establishment_Year_2002', 
       'Outlet_Establishment_Year_2004', 'Outlet_Establishment_Year_2007', 'Outlet_Establishment_Year_2009',
       'Outlet_Size_High', 'Outlet_Size_Medium', 'Outlet_Size_Small',
       'Outlet_Location_Type_Tier 1', 'Outlet_Location_Type_Tier 2', 'Outlet_Location_Type_Tier 3', 
       'Outlet_Type_Grocery Store', 'Outlet_Type_Supermarket Type1', 'Outlet_Type_Supermarket Type2', 'Outlet_Type_Supermarket Type3']

def predict_price(model, weight, visibility, mrp, fat_content, item_type, item_category, outlet_id, est_year, outlet_size, location, outlet_type):    
    try:
        fat_index = X.index('Item_Fat_Content_' + fat_content)
        item_type_index = X.index('Item_Type_' + item_type)
        item_category_index = X.index('Item_Category_' + item_category)
        outlet_id_index = X.index('Outlet_Identifier_' + outlet_id)
        est_year_index = X.index('Outlet_Establishment_Year_' + est_year)
        outlet_size_index = X.index('Outlet_Size_' + outlet_size)
        location_index = X.index('Outlet_Location_Type_' + location)
        outlet_type_index = X.index('Outlet_Type_' + outlet_type)

        index_list = [ fat_index, item_type_index, item_category_index, outlet_id_index, est_year_index, outlet_size_index, location_index, outlet_type_index ]

        x = np.zeros(len(X))
        x[0] = weight
        x[1] = visibility
        x[2] = mrp

        for ind in index_list:
            if ind >= 0:
                x[ind] = 1


        return model.predict([x])[0]
    except Exception as Argument:
        logging.exception("Error occurred in predict_price() in app.py")

app = Flask(__name__)

@app.route("/")
def hello_world():
    try:
        return render_template('index.html')
    except Exception as Argument:
        logging.exception("Error occurred in rendering index.html")

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    try:
        if request.method == 'POST':
            weight = float(request.form['weight'])
            visibility = float(request.form['visibility'])
            mrp = float(request.form['mrp'])

            fat_content = request.form['fat_content']
            item_type = request.form['item_type']
            item_category = request.form['item_category']
            outlet_id = request.form['outlet_id']
            est_year = request.form['est_year']
            outlet_size =request.form['outlet_size']
            location = request.form['location']
            outlet_type = request.form['outlet_type']
    
        model = pickle.load(open('model.pkl', 'rb'))

        prediction = predict_price(model, weight, visibility, mrp, fat_content, item_type, item_category, outlet_id, est_year, outlet_size, location, outlet_type)    
    
        return render_template('index.html', prediction='The predicted sales is of ${}'.format(prediction))
    except Exception as Argument:
        logging.exception("Error occurred in predict() in app.py")
"""
def hello_world():
    a = Modeler()
    a.createModel()
    #return "<h1>Hello, World!</h1>"
    return "Created model"

"""

if __name__=="__main__":
    app.run()

