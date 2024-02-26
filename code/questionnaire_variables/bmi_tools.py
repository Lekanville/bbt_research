import numpy as np
import pandas as pd

#editing wrong inputs
def edit_wrong_inputs(df):
    df_to_edit = df.copy()
    for i in range(len(df)):
        if df_to_edit.loc[i, "User ID"] == "YhfYIQ3a5Z":
            df_to_edit.iloc[i, 29] = 164
            
        if df_to_edit.loc[i, "User ID"] == "3JnGCssgii":
            df_to_edit.iloc[i, 29] = 162.56
    
    return df_to_edit

#getting the units of measurements for each user by searching the various units columns
def get_units(df):
    df_funct = df.copy()
    df_funct["Weight_Unit"] = ""
    df_funct["Height_Unit"] = ""
    df_funct["Hip_Unit"] = ""
    df_funct["Waist_Unit"] = ""
    df_funct["Bust_Cir_Unit"] = ""
    
    #This get the units of the weight for each woman by checking the 4 columns (Stones, Kilograms, Pounds 
    #and those not giving their weights) and putting the value in the weight unit column
    for i in range(len(df_funct)):
        if "Stones" in list(df_funct.iloc[i,1:5]):
            df_funct.loc[i,"Weight_Unit"] = "Stones"
        elif "Pounds (US)" in list(df_funct.iloc[i,1:5]):
            df_funct.loc[i,"Weight_Unit"] = "Pounds (US)"
        elif "Kilos" in list(df_funct.iloc[i,1:5]):
            df_funct.loc[i,"Weight_Unit"] = "Kilos"
        else:
            df_funct.loc[i,"Weight_Unit"] = "None"
            
    #This get the units of the height for each woman by checking the 3 columns (Feets and Inches, Centimeters 
    #and those not giving their heights) and putting the value in the height unit column
        if "Feet and inches" in list(df_funct.iloc[i,24:27]):
            df_funct.loc[i,"Height_Unit"] = "Inches"
        elif "Centimeters" in list(df_funct.iloc[i,24:27]):
            df_funct.loc[i,"Height_Unit"] = "Centimeters"
        else:
            df_funct.loc[i,"Height_Unit"] = "None"
            
    #This get the units of the hip size for each woman by checking the 3 columns (Inches, Centimeters 
    #and those not giving their hip sizes) and putting the value in the hip unit column
        if "Inches" in list(df_funct.iloc[i,9:12]):
            df_funct.loc[i,"Hip_Unit"] = "Inches"
        elif "Centimeters" in list(df_funct.iloc[i,9:12]):
            df_funct.loc[i,"Hip_Unit"] = "Centimeters"
        else:
            df_funct.loc[i,"Hip_Unit"] = "None"
            
    #This get the units of the waist size for each woman by checking the 3 columns (Inches, Centimeters 
    #and those not giving their hip sizes) and putting the value in the waist unit column
        if "Inches" in list(df_funct.iloc[i,13:16]):
            df_funct.loc[i,"Waist_Unit"] = "Inches"
        elif "Centimeters" in list(df_funct.iloc[i,13:16]):
            df_funct.loc[i,"Waist_Unit"] = "Centimeters"
        else:
            df_funct.loc[i,"Waist_Unit"] = "None"
            
    #This get the units of the waist size for each woman by checking the 3 columns (Inches, Centimeters 
    #and those not giving their hip sizes) and putting the value in the waist unit column    
        if "Inches" in list(df_funct.iloc[i,20:23]):
            df_funct.loc[i,"Bust_Cir_Unit"] = "Inches"
        elif "Centimeters" in list(df_funct.iloc[i,20:23]):
            df_funct.loc[i,"Bust_Cir_Unit"] = "Centimeters"
        else:
            df_funct.loc[i,"Bust_Cir_Unit"] = "None"

    return df_funct

#getting the actual values for each user by searching the various value columns
def get_values(df):
    df_w_u = df.copy()
    
    df_w_u["Weight_Values"] = ""
    df_w_u["Height_Values"] = ""
    df_w_u["Hip_Values"] = ""
    df_w_u["Waist_Values"] = ""
    df_w_u["Bust_Cir_Values"] = ""
    
    for i in range(len(df_w_u)):
        #1. Getting the weight values
        #Getting the weight values for the Stones and Pounds. Column 5 is for stones and 6 is for pounds
        if (str(df_w_u.iloc[i,5]) not in ["nan", "Cigarettes"]) & (df_w_u.loc[i,"Weight_Unit"] == "Stones"):
            x = df_w_u.iloc[i,5]
            y = 0
            if str(df_w_u.iloc[i,6]) != "nan":
                y = df_w_u.iloc[i,6]
            y = y*0.0714286
            z = x+y
            df_w_u.loc[i,"Weight_Values"] = z
            
        #Getting the weight values for Kilograms. Column 7 is for Kilograms
        if (str(df_w_u.iloc[i,7]) != "nan") & (df_w_u.loc[i,"Weight_Unit"] == "Kilos"):
            df_w_u.loc[i,"Weight_Values"] = df_w_u.iloc[i,7]
            
        #Getting the weight values for Pounds (US). Column 8 is for Pounds (US)
        if (str(df_w_u.iloc[i,8]) != "nan") & (df_w_u.loc[i,"Weight_Unit"] == "Pounds (US)"):
            df_w_u.loc[i,"Weight_Values"] = df_w_u.iloc[i,8]     
            
            
        #2. Getting the height values
        #Getting the height values for the Feet and Inches. Column 27 is for stones and 28 is for pounds
        if (str(df_w_u.iloc[i,27]) != "nan") & (df_w_u.loc[i,"Height_Unit"] == "Inches"):
            x = df_w_u.iloc[i,27] * 12
            y = 0
            if str(df_w_u.iloc[i,28]) != "nan":
                y = df_w_u.iloc[i,28]
            z = x+y
            df_w_u.loc[i,"Height_Values"] = z
            
        #Getting the height values for Centimeters. Column 29 is for Centimeters
        if (str(df_w_u.iloc[i,29]) != "nan") & (df_w_u.loc[i,"Height_Unit"] == "Centimeters"):
            df_w_u.loc[i,"Height_Values"] = df_w_u.iloc[i,29]
            
            
        #3. Getting the hip values
        if (str(df_w_u.iloc[i,12]) != "nan"):
            df_w_u.loc[i,"Hip_Values"] = df_w_u.iloc[i,12]     
            
        #4. Getting the waist values
        if (str(df_w_u.iloc[i,19]) != "nan"):
            df_w_u.loc[i,"Waist_Values"] = df_w_u.iloc[i,19]
            
        #5. Getting the burst circumference values
        if (str(df_w_u.iloc[i,23]) != "nan"):
            df_w_u.loc[i,"Bust_Cir_Values"] = df_w_u.iloc[i,23]
            
    return df_w_u

#standardizing the values
def get_standard_values(df):
    df_funct = df.copy()
    df_funct["Weight(KG)"] = ""
    df_funct["Height(m)"] = ""
    df_funct["Waist(Inches)"] = ""
    df_funct["Hip(Inches)"] = ""
    df_funct["Bust_Cir(Inches)"] = ""

    
    for i in range(len(df_funct)):
        #standardizing the weights, Stones and Pounds are converted to KG
        if (df_funct.loc[i, "Weight_Unit"] == "Stones") & (df_funct.loc[i, "Weight_Values"] != ""):
            df_funct.loc[i, "Weight(KG)"] = "{0:.1f}".format(df_funct.loc[i, "Weight_Values"] * 6.35029)
        elif (df_funct.loc[i, "Weight_Unit"] == "Pounds (US)") & (df_funct.loc[i, "Weight_Values"] != ''):
            df_funct.loc[i, "Weight(KG)"] = "{0:.1f}".format(df_funct.loc[i, "Weight_Values"] * 0.453592)
        elif (df_funct.loc[i, "Weight_Unit"] == "Kilos") & (df_funct.loc[i, "Weight_Values"] != ''):
            df_funct.loc[i, "Weight(KG)"] = "{0:.1f}".format(df_funct.loc[i, "Weight_Values"])
            
        #standardizing the heights, Inches and Centimeters are converted to Meters
        if (df_funct.loc[i, "Height_Unit"] == "Inches") & (df_funct.loc[i, "Height_Values"] != ""):
            df_funct.loc[i, "Height(m)"] = "{0:.2f}".format(df_funct.loc[i, "Height_Values"] * 0.0254)
        elif (df_funct.loc[i, "Height_Unit"] == "Centimeters") & (df_funct.loc[i, "Height_Values"] != ""):
            df_funct.loc[i, "Height(m)"] = "{0:.2f}".format(df_funct.loc[i, "Height_Values"] * 0.01)
            
        #standardizing the hip sizes, Centimeters converted to Inches
        if (df_funct.loc[i, "Hip_Unit"] == "Inches") & (df_funct.loc[i, "Hip_Values"] != ""):
            df_funct.loc[i, "Hip(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Hip_Values"])
        elif (df_funct.loc[i, "Hip_Unit"] == "Centimeters") & (df_funct.loc[i, "Hip_Values"] != ""):
            df_funct.loc[i, "Hip(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Hip_Values"] * 0.393701)
        
        #standardizing the waist sizes, Centimeters converted to Inches
        if (df_funct.loc[i, "Waist_Unit"] == "Inches") & (df_funct.loc[i, "Waist_Values"] != ""):
            df_funct.loc[i, "Waist(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Waist_Values"])
        elif (df_funct.loc[i, "Waist_Unit"] == "Centimeters") & (df_funct.loc[i, "Waist_Values"] != ""):
            df_funct.loc[i, "Waist(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Waist_Values"] * 0.393701)        
        
        #standardizing the  sizes, Centimeters converted to Inches
        if (df_funct.loc[i, "Bust_Cir_Unit"] == "Inches") & (df_funct.loc[i, "Bust_Cir_Values"] != ""):
            df_funct.loc[i, "Bust_Cir(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Bust_Cir_Values"])
        elif (df_funct.loc[i, "Bust_Cir_Unit"] == "Centimeters") & (df_funct.loc[i, "Bust_Cir_Values"] != ""):
            df_funct.loc[i, "Bust_Cir(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Bust_Cir_Values"] * 0.393701)
              
    return df_funct

#getting the BMI
def get_bmi(df):
    df_funct = df.copy()
    df_funct["BMI"] = ""
    
    for i in range(len(df_funct)):
        if (df_funct.loc[i, "Weight(KG)"] != "" ) & (df_funct.loc[i, "Height(m)"] != ""):
            weight = float(df_funct.loc[i, "Weight(KG)"])
            height = float(df_funct.loc[i, "Height(m)"])
            df_funct.loc[i, "BMI"] = "{0:.1f}".format(weight/height**2)
    return df_funct.iloc[:, np.r_[0, 1, -1]]

#imputation for missing BMIs
def missing_bmi_imputation(df):
    df_funct = df.copy()
    
    median_bmi = np.median(df_funct[df_funct["BMI"] != ""]["BMI"].astype(float))
    
    for i in range(len(df_funct)):    
        if (df_funct.loc[i, "BMI"] == ""):
            #df_funct.loc[i, "BMI"] = median_bmi
            df_funct.loc[i, "BMI"] = "No response"
          
    #df_funct['BMI'] = df_funct['BMI'].apply(pd.to_numeric, errors='coerce')
    return df_funct