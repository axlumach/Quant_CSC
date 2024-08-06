import pandas as pd
import peakutils
import plotly.express as px
import streamlit as st
import datetime as dt
import sys

# noinspection PyUnresolvedReferences
# import str_slider
from processing import utils, save_read, upload_portfolios_HG, upload_portfolios_REAG
from vis_helpers import manual, sidebar, data_customisation, charts, vis_utils
from vis_helpers.vis_utils import print_widgets_separator
from visualisation import visualisation_options as vis_opt
from processing.utils import portfolio_uploaded_checking



# Função para exibir texto alinhado à esquerda
# def left_aligned_text(text):
#     html_str = f"""
#     <div style="text-align: left;">{text}</div>
#     """
#     st.markdown(html_str, unsafe_allow_html=True)


def left_aligned_text(text):
    html_str = f"""
    <div style="text-align: left; height: 24px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
        {text}
    </div>
    """
    st.markdown(html_str, unsafe_allow_html=True)

# def led_indicator(is_success):
#     # Define o estilo do "LED"
#     color = "green" if is_success else "red"
#     html_str = f"""
#     <style>
#     .led-box {{
#         height: 24px;
#         width: 24px;
#         border-radius: 50%;
#         background-color: {color};
#     }}
#     </style>
#     <div class="led-box"></div>
#     """
#     st.markdown(html_str, unsafe_allow_html=True)

def led_indicator1(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def led_indicator2(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box2 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box2"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)

def led_indicator3(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box3 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box3"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def led_indicator4(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box4 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box4"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def led_indicator5(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box5 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box5"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)




def led_indicator6(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box6 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box6"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def led_indicator7(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box7 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box7"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)



def led_indicator8(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box8 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box8"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)


def led_indicator9(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box9 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box9"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)



def led_indicator10(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box10 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box10"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)



def led_indicator11(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box11 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box11"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)




def led_indicator12(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box12 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box12"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)



def led_indicator13(status):
    # Define o estilo do "LED" com base no status
    if status is True:
        color = "green"
        gradient_color = "lime"
        box_shadow_color = "green"
    elif status is False:
        color = "red"
        gradient_color = "tomato"
        box_shadow_color = "red"
    else:  # Caso o status seja None
        color = "gray"
        gradient_color = "darkgray"
        box_shadow_color = "gray"
    
    html_str = f"""
    <style>
    .led-box13 {{
        height: 24px;
        width: 24px;
        border-radius: 50%;
        background: radial-gradient(circle, {gradient_color} 35%, {color} 70%);
        box-shadow: 0 0 8px {box_shadow_color}, 0 0 12px {box_shadow_color};
    }}
    </style>
    <div class="led-box13"></div>
    """
    st.markdown(html_str, unsafe_allow_html=True)




def visualisation():
    #
    # # Spectrometer type `- BWTek / Renishaw / Witec / Wasatch / Teledyne
    #
    # spectrometer = sidebar.choose_spectra_type()
    
    # Adicionar um seletor de data    
    selected_date = st.date_input("Data de referência:", dt.datetime.now())
    # st.write(f"Data selecionada: {selected_date}")

    st.header('Portfolios Uploaded to Database')
    st.subheader('')
    

    # Criando layout de colunas
    col1, col2, col3, col4 = st.columns([1,7,1,7])

    portfolios = ['ARC FIM Master', 'ARC FIA CS Master', 'ARC FIA ARC Master',                  
                  'ARC FIA Serena', 'ARC FIDC Auxiliar', 'ARC FIDC DIP JS', 'ARC FIDC I',
                  'ARC FIDC III', 'ARC FII', 'ARC FII Plaza', 'ARC FII V', 'ARC FIDC MASTER', 'ARC FIP TECH']

    depara_adm = ['HGRIFFO63639', 'HGRIFFO67507', 'HGRIFFO67407',                  
                  'FIA SERENA I', 'FIAGRO ARC AUXI', 'FIDC ARC DIP JS', 'FIDC ARC I',
                  'FIDC ARC III', 'FII ARC III', 'FII ARC PL II', 'FII ARC V', 'FIDC MASTER', 'FIP ARC TECH']

    # status_list = [None] * portfolios.count()  # Lista para armazenar o status dos LEDs

    # Adicionando indicadores e textos
    for i in range(0, 12):
        status = True if i % 2 == 0 else False  # Exemplo de status alternado

        # Construir o nome da função dinamicamente
        led_function_name = f'led_indicator{i+1}'


        # Obter a função pelo nome
        led_function = getattr(sys.modules[__name__], led_function_name)

        if i <= 5:
            with col1:
                led_function(portfolio_uploaded_checking(selected_date, depara_adm[i]))
                st.write('')                
            with col2:
                left_aligned_text(portfolios[i])
                st.write('')
        else:
            with col3:
                led_function(portfolio_uploaded_checking(selected_date, depara_adm[i]))
                st.write('')
            with col4:
                left_aligned_text(portfolios[i])
                st.write('')



    # sidebar separating line
    print_widgets_separator(1, sidebar=True)
    # led_indicator(None)
    # User data loader
    # sidebar.print_widget_labels('Upload your data or try with ours', 10, 0)
    
    files = st.sidebar.file_uploader(label='Upload your data or try with ours',
                                     accept_multiple_files=True,
                                     type=['xls', 'xlsx'])
    
    # Allow example data loading when no custom data are loaded
    # if not files and st.sidebar.checkbox("Load example data"):
    #     if spectrometer == "EMPTY":
    #         st.sidebar.error('First Choose Spectra type')
    #     else:
    #         files = utils.load_example_files(spectrometer)
    
    # Check if data loaded, if yes, perform actions
    if files:
        st.spinner('Uploading data in progress')
        # sidebar separating line
        print_widgets_separator(1, sidebar=True)
        # df = save_read.files_to_df(files, spectrometer)
        # Select chart type
        # chart_type = vis_opt.vis_options()
        


        for file in files:
            if 'Carteira_ARC' in file.name or 'Carteira_CSHG' in file.name:
                result = upload_portfolios_HG.execute_HG(file)
                # status_list[portfolios.index('ARC FIM Master')] = result  # Atualize o status correspondente                
                # led_indicator(port_check.portfolio_uploaded_checking(selected_date, depara_adm[i]))
                if not result:
                    st.error(f"Ocorreu um erro ao processar o arquivo {file.name}")
            else:
                result = upload_portfolios_REAG.execute_REAG(file)
                # status_list[portfolios.index('ARC FIDC Auxiliar')] = result  # Atualize o status correspondente
                # led_indicator(port_check.portfolio_uploaded_checking(selected_date, depara_adm[i]))
                if not result:
                    st.error(f"Ocorreu um erro ao processar o arquivo {file.name}")
        
        st.experimental_rerun()

        # Atualize os LEDs com base nos resultados dos uploads
        # for i in range(0, 12):
        #     if i <= 5:
        #         with col1:
        #             led_function(portfolio_uploaded_checking(selected_date, depara_adm[i]))
        #             st.write('')
        #         with col2:
        #             left_aligned_text(portfolios[i])
        #             st.write('')
        #     else:
        #         with col3:
        #             led_function(portfolio_uploaded_checking(selected_date, depara_adm[i]))
        #             st.write('')
        #         with col4:
        #             left_aligned_text(portfolios[i])
        #             st.write('')

        return
    
    else:
        manual.show_manual()
