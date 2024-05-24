import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_plotly
import faicons as fa

# Load the dataset
df = pd.read_csv("./WallCityTap_Consumer.csv")
df.columns = df.columns.str.strip()  # Clean column names
df['Annual_Income'] = pd.to_numeric(df['Annual_Income'], errors='coerce')  # Ensure Annual_Income is numeric
X = df[['Age', 'Annual_Income', 'Spending Score (1-100)']]

# Determine the optimal number of clusters using the Elbow Method
wcss = []
for i in range(1, 21):  # Adjusting to 20 for a more detailed elbow graph
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Plot the Elbow Method
elbow_fig = px.line(x=range(1, 21), y=wcss, markers=True,
                    title='Método del Codo para K óptimo',
                    labels={'x': 'Cantidad de Centroides k', 'y': 'WCSS (Within-Cluster Sum of Square)'})
elbow_fig.update_layout(
    annotations=[{
        'text': (
            "A partir de la curva obtenida podemos ver cómo a medida que se aumenta la cantidad de centroides, "
            "el valor de WCSS disminuye de tal forma que la gráfica adopta una forma de codo. Para seleccionar el valor óptimo de k, "
            "se escoge entonces ese punto en donde ya no se dejan de producir variaciones importantes del valor de WCSS al aumentar k. "
            "En este caso, vemos que esto se produce a partir de k >= 5, por lo que evaluaremos los resultados del agrupamiento, "
            "por ejemplo, con los valores de 5, 6 y 7 a fin de observar el comportamiento del modelo."
        ),
        'xref': 'paper',
        'yref': 'paper',
        'x': 0.5,
        'y': -0.2,
        'showarrow': False,
        'font': {'size': 12}
    }]
)

# Assuming K=5 is optimal based on the Elbow method
kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, n_init=10, random_state=0)
df['Cluster'] = kmeans.fit_predict(X)

# General clustering with all data
kmeans_all = KMeans(n_clusters=5, init='k-means++', max_iter=300, n_init=10, random_state=0)
df['General_Cluster'] = kmeans_all.fit_predict(X)

# Convert unique clusters to a list of strings for the input_select choices
cluster_choices = [str(cluster) for cluster in df['Cluster'].unique()]
payment_methods = df['Payment_Methods'].unique().tolist()  # Convert to list

# Icons setup
ICONS = {
    "user": fa.icon_svg("user", "regular"),
    "wallet": fa.icon_svg("wallet"),
    "currency-dollar": fa.icon_svg("dollar-sign"),
    "ellipsis": fa.icon_svg("ellipsis"),
}

# UI Configuration
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider("age", "Edad:", min=18, max=70, value=(18, 70)),
        ui.input_checkbox_group("payment_methods", "Medios de Pago:", choices=payment_methods, selected=payment_methods),
        ui.input_select("cluster", "Seleccionar Cluster:", choices=cluster_choices),
        open="desktop"
    ),
    ui.layout_columns(
        ui.value_box("Número de consumidores Online E-commerce", ui.output_ui("num_records"), showcase=ICONS["user"]),
        ui.value_box("Edad promedio de consumidores que utilizan como medio de pago efectivo:", ui.output_ui("average_payment_age"), showcase=ICONS["wallet"]),
        ui.value_box("Edad promedio de consumidores que poseen un ingreso anual mayor a $20,000", ui.output_ui("average_high_income_age"), showcase=ICONS["user"]),
        ui.value_box("Medio de pago preferido", ui.output_ui("preferred_payment_method"), showcase=ICONS["wallet"])
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Método del Codo"),
            output_widget("elbow_plot"),
            full_screen=True
        ),
        ui.card(
            ui.card_header("Segmentación de Clientes K-means"),
            output_widget("cluster_plot"),
            full_screen=True
        ),
        ui.card(
            ui.card_header("Conjunto de Datos de Consumidores"),
            ui.output_data_frame("cluster_table"),
            full_screen=True
        ),
    ),
    title="Dashboard de Segmentación de Clientes",
    fillable=True,
    style="max-height: 100vh; overflow-y: auto;"  # For scrolling on smaller screens
)

def server(input, output, session):

    @reactive.calc
    def filtered_df():
        """Filters the dataframe based on the selected cluster and inputs."""
        return df[
            (df['Cluster'] == int(input.cluster())) &
            (df['Age'] >= input.age()[0]) &
            (df['Age'] <= input.age()[1]) &
            (df['Payment_Methods'].isin(input.payment_methods()))
        ]

    @render_plotly
    def elbow_plot():
        """Renders the elbow plot."""
        return elbow_fig

    @render_plotly
    def cluster_plot():
        """Renders the scatter plot for the selected cluster."""
        fig = px.scatter(filtered_df(),
                         x='Annual_Income',
                         y='Spending Score (1-100)',
                         color='Payment_Methods',  # Color by payment methods
                         symbol='Cluster',  # Different symbols for clusters
                         title=f"Cluster {input.cluster()}",
                         labels={'Annual_Income': 'Ingreso Anual',
                                 'Spending Score (1-100)': 'Puntaje de Gasto (1-100)',
                                 'Payment_Methods': 'Métodos de Pago'}
                        )
        fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))  # Adjust margins as needed
        return fig

    @render.data_frame
    def cluster_table():
        """Displays the data for the selected cluster."""
        return filtered_df()

    @render.ui
    def num_records():
        return len(filtered_df())

    @render.ui
    def average_payment_age():
        filtered = filtered_df()
        filtered = filtered[filtered['Payment_Methods'] == 'Cash']  # Considering only those who pay with cash
        if not filtered.empty:
            return f"{filtered['Age'].mean():.2f}"
        return "N/A"

    @render.ui
    def average_high_income_age():
        filtered = df[df['Annual_Income'] > 20]  # Considering 20 means $20,000
        if not filtered.empty:
            return f"{filtered['Age'].mean():.2f}"
        return "N/A"

    @render.ui
    def preferred_payment_method():
        payment_method_counts = df['Payment_Methods'].value_counts()
        if not payment_method_counts.empty:
            return payment_method_counts.idxmax()
        return "N/A"

    @render.ui
    def potential_consumers():
        potential = df[(df['Annual_Income'] > 20) & (df['Spending Score (1-100)'] > 70)]
        if not potential.empty:
            return f"Consumidores Potenciales: {len(potential)}, Edad Promedio: {potential['Age'].mean():.2f}, Medio de Pago Preferido: {potential['Payment_Methods'].mode()[0]}"
        return "N/A"

app = App(app_ui, server)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
