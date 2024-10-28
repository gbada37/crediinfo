import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

# Supposons que df_renamed est votre DataFrame contenant les données nécessaires.
df_renamed = pd.read_csv('creditdata_cleaned.csv')

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

# Graphique de la distribution des statuts de logement
st.subheader('Distribution des Statuts de Logement')
logement_counts = df_renamed['statut_logement'].value_counts()
plt.figure(figsize=(10, 6))
logement_counts.plot(kind='bar', color='skyblue')
plt.title('Distribution des Statuts de Logement')
plt.xlabel('Statut de Logement')
plt.ylabel('Nombre de Clients')
plt.xticks(rotation=45)
plt.grid(axis='y')
st.pyplot(plt)

# Histogramme de la distribution du total des comptes de crédit
st.subheader('Distribution du Total des Comptes de Crédit')
plt.figure(figsize=(10, 6))
plt.hist(df_renamed['comptes_credit_total'], bins=30, color='lightgreen', edgecolor='black')
plt.title('Distribution du Total des Comptes de Crédit')
plt.xlabel('Total des Comptes de Crédit')
plt.ylabel('Nombre de Clients')
plt.grid(axis='y')
st.pyplot(plt)


