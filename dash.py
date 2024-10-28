import streamlit as st
import pandas as pd
import plotly.express as px

# Supposons que df_renamed est votre DataFrame contenant les données nécessaires.
df_renamed = pd.read_parquet('fichier_compresse.parquet')

# Calcul des revenus moyens par solvabilité
mean_revenue = df_renamed.groupby('solvabilite')['revenu_annuel'].mean().reset_index()

# Visualisation 1 : Revenu moyen par solvabilité
fig1 = px.bar(mean_revenue, x='solvabilite', y='revenu_annuel', color='solvabilite',
              title='Revenu Moyen des Clients par Solvabilité',
              labels={'revenu_annuel': 'Revenu Annuel Moyen', 'solvabilite': 'Solvabilité'})
fig1.update_layout(xaxis_title="Solvabilité", yaxis_title="Revenu Annuel Moyen")

# Calcul des moyennes des caractéristiques par solvabilité
mean_characteristics = df_renamed.groupby('solvabilite')[['montant_pret', 'revenu_annuel', 'mensualite']].mean().reset_index()
mean_characteristics = mean_characteristics.melt(id_vars="solvabilite", value_vars=['montant_pret', 'revenu_annuel', 'mensualite'])

# Visualisation 2 : Caractéristiques moyennes par solvabilité
fig2 = px.bar(mean_characteristics, x='variable', y='value', color='solvabilite', barmode='group',
               title="Caractéristiques Moyennes des Clients",
               labels={'variable': 'Caractéristiques', 'value': 'Valeur Moyenne'})
fig2.update_layout(xaxis_title="Caractéristiques", yaxis_title="Valeur Moyenne")

# Calculer la répartition des clients par note d'emprunteur
emprunteur_counts = df_renamed['note_emprunteur'].value_counts()

# Visualisation 3 : Répartition des clients par note d'emprunteur
fig3 = px.pie(values=emprunteur_counts.values, names=emprunteur_counts.index,
               title="Répartition des Clients par Note d'Emprunteur")
fig3.update_traces(textposition='inside', textinfo='percent+label')

# Visualisation 4 : Distribution de la solvabilité des clients
fig4 = px.histogram(df_renamed, x='solvabilite', color='solvabilite',
                    title='Distribution de la Solvabilité des Clients',
                    labels={'solvabilite': 'Solvabilité'})
fig4.update_layout(xaxis_title="Solvabilité", yaxis_title="Nombre de Clients")

# Calculer le revenu total et moyen par catégorie de solvabilité
revenu_par_solvabilite = df_renamed.groupby('solvabilite')['revenu_annuel'].sum()
revenu_moyen_par_solvabilite = df_renamed.groupby('solvabilite')['revenu_annuel'].mean()
labels = [f"{solvabilite}\nRevenu Moyen: {revenu_moyen_par_solvabilite[solvabilite]:,.0f}" for solvabilite in revenu_par_solvabilite.index]

# Affichage des visualisations dans l'application Streamlit
st.title("Analyses de Solvabilité des Clients")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

# Graphique de la distribution des statuts de logement avec Plotly Express
st.subheader('Distribution des Statuts de Logement')
logement_counts = df_renamed['statut_logement'].value_counts().reset_index()
logement_counts.columns = ['statut_logement', 'nombre_clients']
fig_logement = px.bar(logement_counts, x='statut_logement', y='nombre_clients',
                       title='Distribution des Statuts de Logement',
                       labels={'statut_logement': 'Statut de Logement', 'nombre_clients': 'Nombre de Clients'},
                       color='nombre_clients')
fig_logement.update_layout(xaxis_title="Statut de Logement", yaxis_title="Nombre de Clients")

st.plotly_chart(fig_logement, use_container_width=True)

# Histogramme de la distribution du total des comptes de crédit avec Plotly Express
st.subheader('Distribution du Total des Comptes de Crédit')
fig_credit = px.histogram(df_renamed, x='comptes_credit_total', nbins=30, 
                          title='Distribution du Total des Comptes de Crédit',
                          labels={'comptes_credit_total': 'Total des Comptes de Crédit'})
fig_credit.update_layout(xaxis_title="Total des Comptes de Crédit", yaxis_title="Nombre de Clients")

st.plotly_chart(fig_credit, use_container_width=True)
