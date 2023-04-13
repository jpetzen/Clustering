from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit as st
import pandas as pd
import glob
import base64
import openpyxl


st.session_state['answer'] = ''  #za git runnat


FilePath = "data/data.csv"
grafiLL = glob.glob("data/grafiLL/*.svg")  # pazi na velikost slik max je 200mb
grafiH = glob.glob("data/grafiH/*.svg")
grafiRL = glob.glob("data/grafiRL/*.svg")

# df= pd.read_excel(FilePath,usecols=["ID","label","comment","min","max","mean","std","skew","C"])#katere vrstice rabimo
df = pd.read_csv(FilePath)
imagesLL = []
for file in grafiLL:
    with open(file, "rb") as f:
        img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        imagesLL.append(img_b64)
df["Leg_left"] = imagesLL
imagesH = []
for file in grafiH:
    with open(file, "rb") as f:
        img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        imagesH.append(img_b64)
df["Hand"] = imagesH
imagesRL = []
for file in grafiRL:
    with open(file, "rb") as f:
        img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        imagesRL.append(img_b64)
df["Leg_right"] = imagesRL


st.set_page_config(  # konfiguracija strani, more biti prva komanda iz streamlita
    page_title="ABI",
    layout="wide",  # da imamo tabelo čez celo stran
)
# naslov
st.header("ABI Anotacije")

# vnos slik
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



# dropable menu
NameList = ("Normal", "PAD", "Mediocal", "Undefined", "Error")
df = df[["ID", "Leg_left", "label", "comment", "min", "max", "mean",
            "std", "skew", "C", "Hand", "Leg_right"]]  # vrstni red prikaza
# Infer basic colDefs from dataframe types
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()  # strani, brz tega skrolamo
gb.configure_column("Leg_left", editable=False,
                    autoHeight=True, cellRenderer=ShowImageLL)
gb.configure_column("Hand", editable=False,
                    autoHeight=True, cellRenderer=ShowImageH)
gb.configure_column("Leg_right", editable=False,
                    autoHeight=True, cellRenderer=ShowImageRL)
gb.configure_column("ID", editable=False, width=50)
gb.configure_column("C", editable=False, width=50)
gb.configure_column("min", editable=False, width=80)
gb.configure_column("max", editable=False, width=80)
gb.configure_column("mean", editable=False, width=80)
gb.configure_column("std", editable=False, width=80)
gb.configure_column("skew", editable=False, width=80)
gb.configure_column("comment", editable=True, type="string",wrapText = True)
gb.configure_column("label", editable=True, type="string", cellEditor="agSelectCellEditor",
                    cellEditorParams={'values': list(NameList)})
gb.configure_grid_options(domLayout='normal')  # rowHeight=50
gridOptions = gb.build()


# Display the grid
grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    height=800,
    width='100%',
    sample_size=100,  # lahko fiksno število vnosov
    enable_enterprise_modules=True,
    # fit_columns_on_grid_load=True,#ob zagono strani podatki zasedejo celo tabelo
    allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
    allow_unsafe_html=True,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW
)

#grid_result = grid_response['data']
#columns = ["ID", "label", "comment", "min", "max",
#            "mean", "std", "skew", "C"]  # vrstni red
#grid_result = pd.DataFrame(grid_result, columns=columns)


def saved(grid_response):    
    grid_result = grid_response['data']
    columns = ["ID", "label", "comment", "min", "max",
               "mean", "std", "skew", "C"]  # vrstni red
    grid_result = pd.DataFrame(grid_result, columns=columns)
    print(grid_result)

    updated_data = pd.DataFrame(grid_result, columns=columns)
    updated_data[['label', 'comment']] = grid_result[['label', 'comment']]

    updated_data.to_csv('data/data.csv', index=False)


st.button(
    "Save changes",
    help="Click this button to save your results",
    on_click=saved(grid_response)
)
