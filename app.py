import streamlit as st
import joblib


# Carga del modelo de prediccion
modelo = joblib.load("smoking_model.joblib")

# Titulo
st.title("Smoking Test")

# Descripcion
st.markdown("""
            El siguiente test presenta la capacidad de clasificar a una persona como fumadora o
            no fumadora en función de unos determinados valores antropométricos y biológicos con
            una exactitud del 82,18%
            
            El test se ha obtenido a partir de una muestra de 44.553 personas de ámbos géneros y
            de distintas edades.
            """)

# Entradas de datos
col1, col2, col3 = st.columns(3)

with col1:
    ALT = st.number_input("Alanina aminotransferasa (U/L)", min_value=0.0, value=7.0, step=0.1)
    AST = st.number_input("Aspartato aminotransferasa (U/L)", min_value=0.0, value=5.0, step=0.1)
    colesterol = st.number_input("Colesterol (mg/dL)", min_value=0, value=200)
    LDL = st.number_input("Lipoproteína baja densidad (mg/dL)", min_value=0, value=30)
    HDL = st.number_input("Lipoproteína alta densidad (mg/dL)", min_value=0, value=40)
    GTP = st.number_input("Guanosina trifosfato (U/L)", min_value=0, value=6)

with col2:
    glucosa = st.number_input("Glucosa en ayuno (mg/dL)", value=70, min_value=0)
    hemoglobina = st.number_input("Hemoglobina (g/dL)", min_value=0.0, value=12.0, step=0.1)
    trigliceridos = st.number_input("Triglicéridos (mg/dL)", min_value=0, value=50)
    edad = st.number_input("Edad", value=18, min_value=0)
    caries_dental = st.selectbox("Caries dental (SI/NO)", options=("SI", "NO"))
    presencia_sarro = st.selectbox("Presencia de sarro dental (SI/NO)", options=("SI", "NO"))

with col3:
    diastolica = st.number_input("Presión arterial diastólica (mmHg)", min_value=0, value=60)
    sistolica = st.number_input("Presión arterial sistólica (mmHg)", min_value=0, value=120)
    altura = st.number_input("Altura (cm)", min_value=0, value=150)
    peso = st.number_input("Peso corporal (kg)", min_value=0, value=60)
    cintura = st.number_input("Anchura de cintura (cm)", min_value=0, value=80)
    genero_masculino = st.selectbox("Género masculino (SI/NO)", options=("SI", "NO"))

caries = 1 if caries_dental == "SI" else 0
hombre = 1 if genero_masculino == "SI" else 0
mujer = 1 if hombre == 0 else 0
sarro = 1 if presencia_sarro == "SI" else 0
IMC = (peso/((altura/100)**2))
overweight = 1 if (IMC >= 25 and IMC < 30) else 0
IMC_rango = "peso bajo" if IMC < 18.5 else ("peso normal" if (IMC >= 18.5 and IMC < 25) else
                                            ("sobrepeso" if IMC >= 25 and IMC < 30 else "obsesidad"))

if hombre == 1:
    st.write(f"El individuo se trata de un hombre de {edad} años de edad.")
else:
    st.write(f"El individuo se trata de una mujer de {edad} años de edad.")

st.write(f"Según el peso y la altura, el individuo tiene un IMC de {round(IMC, 2)}, considerado {IMC_rango}.")


variables = [ALT, AST, colesterol, GTP, HDL, IMC, LDL, edad,
             caries, glucosa, mujer, hombre, altura,
             hemoglobina, overweight, diastolica,
             sistolica, sarro, trigliceridos, cintura,
             peso]

fumador = ""

if st.button("Realizar Test"):
    fumador_pred = modelo.predict([variables])

    if fumador_pred[0] == 1:
        fumador = "El resultado del test confirma que SI se trata de una persona fumadora"
    else:
        fumador = "El resultado del test confirma que NO se trata de una persona fumadora"

    st.success(fumador)
