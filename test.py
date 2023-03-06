from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit as st
import pandas as pd 
import glob
import base64


 
FilePath=r"data/new_data1.xlsx"
grafiLL=glob.glob("graf/grafiLL/*.svg")# pazi na velikost slik max je 200mb
grafiH=glob.glob("graf/grafiH/*.svg")
grafiRL=glob.glob("graf/grafiRL/*.svg")

df= pd.read_excel(FilePath,usecols=["index","label","comment","min","max","mean","std","skew","cluster","FileID"])#katere vrstice rabimo
imagesLL=[]
for file in grafiLL:
    with open(file, "rb") as f:
        img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        imagesLL.append(img_b64)
df["Leg_left"]=imagesLL
imagesH=[]
for file in grafiH:
    with open(file, "rb") as f:
        img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        imagesH.append(img_b64)
df["Hand"]=imagesH
imagesRL=[]
for file in grafiRL:
    with open(file, "rb") as f:
        img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        imagesRL.append(img_b64)
df["Leg_right"]=imagesRL



st.set_page_config(#konfiguracija strani, more biti prva komanda iz streamlita
page_title="ABI",
layout="wide",#da imamo tabelo čez celo stran
)
#naslov
st.header("ABI Anotacije")
st.session_state['answer'] = ''!
#vnos slik
ShowImageLL = JsCode("""function (params) {
      if (params.value) {
            return '<img src="data:image/svg+xml;base64,' + params.value + '" style="max-height: 95px;">';
        } else {
            return '';
        }
    }
    """
)
ShowImageH = JsCode("""function (params) {
      if (params.value) {
            return '<img src="data:image/svg+xml;base64,' + params.value + '" style="max-height: 95px;">';
        } else {
            return '';
        }
    }
    """
)
ShowImageRL = JsCode("""function (params) {
      if (params.value) {
            return '<img src="data:image/svg+xml;base64,' + params.value + '" style="max-height: 95px;">';
        } else {
            return '';
        }
    }
    """
)
#dropable menu
NameList = ( "Normal", "PAD", "Mediocal", "Undefined", "Error")  

df=df[["index","Leg_left","label","comment","min","max","mean","std","skew","cluster","Hand","Leg_right","FileID"]]#vrstni red prikaza
#Infer basic colDefs from dataframe types
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()#strani, brz tega skrolamo
gb.configure_column("Leg_left", editable=False,autoHeight=True,cellRenderer=ShowImageLL,width=230) 
gb.configure_column("Hand", editable=False,autoHeight=True,cellRenderer=ShowImageH,width=230) 
gb.configure_column("Leg_right", editable=False,autoHeight=True,cellRenderer=ShowImageRL,width=230) 
gb.configure_column("index",editable=False,width=60)
gb.configure_column("cluster",editable=False,width=60)
gb.configure_column("min",editable=False,width=80)
gb.configure_column("max",editable=False,width=80)
gb.configure_column("mean",editable=False,width=70)
gb.configure_column("std",editable=False,width=90)
gb.configure_column("skew",editable=False,width=70)
gb.configure_column("comment",editable=True,width=240) 
gb.configure_column("label",editable=True,cellEditor="agSelectCellEditor", cellEditorParams={'values': NameList },width=90)  
gb.configure_column("FileID",editable=False,width=220)
gb.configure_grid_options(domLayout='normal')#rowHeight=50
gridOptions = gb.build()


#Display the grid
grid_response = AgGrid(
    df, 
    gridOptions=gridOptions,
    height=800, 
    width='100%',
    sample_size=100,#lahko fiksno število vnosov
    enable_enterprise_modules=True,
    #fit_columns_on_grid_load=True,#ob zagono strani podatki zasedejo celo tabelo
    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
    allow_unsafe_html=True
    )

grid_result = grid_response['data']
columns = ["index","leg_left","label","comment","min","max","mean","std","skew","cluster","FileID"]#vrstni red 
grid_result = pd.DataFrame(grid_result, columns=columns)

def save():
    # Get the updated data from the grid result
    updated_data = pd.DataFrame(grid_result, columns=columns)
    updated_data[['label','comment']] = grid_result[['label','comment']]
    # Save the updated data to a new Excel file
    with pd.ExcelWriter(FilePath) as writer:
        updated_data.to_excel(writer, sheet_name='Sheet1', index=False)                                                           
    
st.button(
        "Save changes",
        help="Click this button to save your results",
        on_click=save,
)



