import pandas as pd
import csv
import os

#llamo a la ruta donde esta el csv y la guardo
base_dir = os.path.dirname(__file__)
ruta_csv = os.path.join(base_dir, "EMAE_Limpio.csv")

#creo la carpeta donde iran todas las tablas generadas en este pipeline, con nombre outputs
output_dir = os.path.join(base_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

#guardo el archivo en la variable df, le aclaro que el separador del csv es ";" y los decimales van con "," (Excel en español)
df = pd.read_csv(ruta_csv, sep=";", decimal=",")

# Convertir número Excel a fecha calendario
df["fecha"] = pd.to_datetime(df["fecha"], origin="1899-12-30", unit="D")

#renombrando las columnas del Excel para que sean más fáciles de trabajar
df = df.rename(columns={
    "EMAE desestacionalizado": "emae_total",
    '"AGRO" desestacionalizado': "emae_agro",
    "Industria desestacionalizado": "emae_industria"
})

#eligiendo las columnas del csv que me interesan para el analisis
df = df[["fecha", "emae_total", "emae_agro", "emae_industria"]]

#reorganizando las fechas cronologicamente (no es necesario porque ya venian asi pero es buena práctica)
df = df.sort_values("fecha")
df = df.reset_index(drop=True)

#calculamos variación mensual para todos los sectores
df["var_mensual_total"] = df["emae_total"].pct_change() * 100
df["var_mensual_agro"] = df["emae_agro"].pct_change() * 100
df["var_mensual_industria"] = df["emae_industria"].pct_change() * 100

#seteo la opción para que me muestre todas las columnas
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

#para testear a ver si los valores son mas o menos razonables
#print(df[["var_mensual_agro"]].describe())

#-----------------------------------------------------------------------------------------------
#armando tabla para los kpis de Power BI, con el crecimiento promedio y la volatilidad promedio
tabla_estructural = []

sectores = {
    "total": "var_mensual_total",
    "agro": "var_mensual_agro",
    "industria": "var_mensual_industria"
}

for nombre, col in sectores.items():
    tabla_estructural.append({
        "sector": nombre,
        "crecimiento_promedio_mensual": df[col].mean(),
        "volatilidad_mensual": df[col].std()
    })

tabla_estructural_df = pd.DataFrame(tabla_estructural)
#-------------------------------------------------------------------------------

#distribución de shocks
shocks = [2009, 2020, 2022]

df = df.sort_values("fecha").reset_index(drop=True)
df["anio"] = df["fecha"].dt.year

shocks_centro = {
    "crisis_2009": "2009-03-01",
    "pandemia_2020": "2020-04-01",
    "sequia_2022": "2022-12-01",
    #"sequia_2023": "2023-05-01",
}

import pandas as pd
import numpy as np

SERIES = {
    "total": "emae_total",
    "agro": "emae_agro",
    "industria": "emae_industria",
}

def peak_trough_window(df, center_date, pre_months=12, post_months=12):
    center = pd.to_datetime(center_date)
    start_pre = center - pd.DateOffset(months=pre_months)
    end_pre   = center - pd.DateOffset(months=1)

    start_post = center
    end_post   = center + pd.DateOffset(months=post_months-1)

    df_pre  = df[(df["fecha"] >= start_pre) & (df["fecha"] <= end_pre)]
    df_post = df[(df["fecha"] >= start_post) & (df["fecha"] <= end_post)]

    out = []
    for sector, col in SERIES.items():
        pico  = df_pre[col].max()
        valle = df_post[col].min()
        caida = (valle - pico) / pico * 100

        out.append({
            "sector": sector,
            "pico_pre": pico,
            "valle_post": valle,
            "caida_pico_valle": caida,
            "ventana_pre_desde": start_pre.date(),
            "ventana_pre_hasta": end_pre.date(),
            "ventana_post_desde": start_post.date(),
            "ventana_post_hasta": end_post.date(),
        })
    return pd.DataFrame(out)

resultados = []

for shock_name, center_date in shocks_centro.items():
    tmp = peak_trough_window(df, center_date, pre_months=12, post_months=12)
    tmp.insert(0, "shock", shock_name)
    tmp.insert(1, "center_date", pd.to_datetime(center_date).date())
    resultados.append(tmp)

shocks_window_df = pd.concat(resultados, ignore_index=True)
print(shocks_window_df[["shock","sector","caida_pico_valle","pico_pre","valle_post"]])

#-------------------------------------------------------------------------------------------
#tabla 3 recuperacion

SERIES = {"total":"emae_total","agro":"emae_agro","industria":"emae_industria"}

# definimos la ventana post según tipo de shock (igual que antes)
POST_BY_SHOCK = {
    "crisis_2009": 12,
    "pandemia_2020": 12,
    "sequia_2022": 6
}

resultados_recuperacion = []

for _, row in shocks_window_df.iterrows():
    shock = row["shock"]
    sector = row["sector"]
    col = SERIES[sector]

    pico = row["pico_pre"]
    umbral = 0.95 * pico

    center = pd.to_datetime(row["center_date"])
    post_months = POST_BY_SHOCK.get(shock, 12)  # default 12 si faltara

    post_start = center
    post_end = center + pd.DateOffset(months=post_months - 1)

    # 1) ubicar el valle dentro de la ventana post
    df_post_window = df[(df["fecha"] >= post_start) & (df["fecha"] <= post_end)].copy()

    if df_post_window.empty:
        resultados_recuperacion.append({
            "shock": shock, "sector": sector,
            "umbral_recuperacion": umbral,
            "fecha_valle": None,
            "fecha_recuperacion": None,
            "meses_recuperacion": None
        })
        continue

    valle_val = df_post_window[col].min()
    fecha_valle = df_post_window.loc[df_post_window[col] == valle_val, "fecha"].iloc[0]

    # 2) buscar recuperación desde el valle en adelante (hasta donde haya datos)
    df_busqueda = df[df["fecha"] > fecha_valle]
    rec = df_busqueda[df_busqueda[col] >= umbral]

    if not rec.empty:
        fecha_rec = rec.iloc[0]["fecha"]
        meses = (fecha_rec.year - fecha_valle.year) * 12 + (fecha_rec.month - fecha_valle.month)
    else:
        fecha_rec = None
        meses = None

    resultados_recuperacion.append({
        "shock": shock,
        "sector": sector,
        "umbral_recuperacion": umbral,
        "fecha_valle": fecha_valle,
        "fecha_recuperacion": fecha_rec,
        "meses_recuperacion": meses
    })

recuperacion_df = pd.DataFrame(resultados_recuperacion)
print(recuperacion_df)



#exportando las tablas a la carpeta outputs
#Tabla 1
df.to_csv(os.path.join(output_dir, "dataset_mensual_emae.csv"), index=False)

# Página 1 - resumen estructural
tabla_estructural_df.to_csv(
    os.path.join(output_dir, "pagina1_tabla_estructural.csv"),
    index=False
)

# Página 2 - shocks (caída pico-valle + picos/valles)
shocks_window_df.to_csv(
    os.path.join(output_dir, "pagina2_shocks.csv"),
    index=False
)

# Página 3 - recuperación
recuperacion_df.to_csv(
    os.path.join(output_dir, "pagina3_recuperacion.csv"),
    index=False
)

print("✅ Exportaciones completas. Archivos en:", output_dir)
print(os.listdir(output_dir))