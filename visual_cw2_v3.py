import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Get path to .csv file
script_dir = os.path.dirname(os.path.abspath(__file__))
inv_script_dir = script_dir.replace('\\', '/')
csv_path = inv_script_dir + '/Results_21Mar2022.csv'

# Load the dataset
df = pd.read_csv(csv_path)

# Selecting environmental mean columns
env_metrics = [
    'mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut',
    'mean_ghgs_ch4', 'mean_ghgs_n2o', 'mean_bio', 'mean_watuse', 'mean_acid'
]

# Group the data by 'diet_group' and 'sex'
diet_summary = df.groupby(['diet_group', 'sex'])[env_metrics + ['n_participants']].mean().reset_index()

# Separate male and female datasets
diet_summary_male = diet_summary[diet_summary['sex'] == 'male']
diet_summary_female = diet_summary[diet_summary['sex'] == 'female']

# Build Diet Group dimension separately
def build_diet_group_dimension(subset):
    return dict(
        label="Diet Group",
        values=list(range(len(subset))),
        tickvals=list(range(len(subset))),
        ticktext=subset['diet_group'],
        range=[-1, len(subset)],  # Slightly expanded
        visible=True  # Still visible but compact
    )

# Create male figure
fig_male = px.parallel_coordinates(
    diet_summary_male,
    dimensions=[
        build_diet_group_dimension(diet_summary_male),
        'mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut',
        'mean_ghgs_ch4', 'mean_ghgs_n2o', 'mean_bio', 'mean_watuse', 'mean_acid'
    ],
    color='mean_ghgs',
    color_continuous_scale=px.colors.diverging.Tealrose,
    labels={
        'mean_ghgs': 'GHG Emissions (kg CO₂e/day)',
        'mean_land': 'Land Use (m²/day)',
        'mean_watscar': 'Water Scarcity (liters/kg)',
        'mean_eut': 'Eutrophication (g PO₄³⁻ eq/day)',
        'mean_ghgs_ch4': 'Methane Emissions (kg CH₄/day)',
        'mean_ghgs_n2o': 'Nitrous Oxide Emissions (kg N₂O/day)',
        'mean_bio': 'Biodiversity Impact (loss units)',
        'mean_watuse': 'Water Use (liters/day)',
        'mean_acid': 'Acidification (g SO₂ eq/day)'
    },
    title="Environmental Impacts by Diet Group (Male)"
)

# Create female figure
fig_female = px.parallel_coordinates(
    diet_summary_female,
    dimensions=[
        build_diet_group_dimension(diet_summary_female),
        'mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut',
        'mean_ghgs_ch4', 'mean_ghgs_n2o', 'mean_bio', 'mean_watuse', 'mean_acid'
    ],
    color='mean_ghgs',
    color_continuous_scale=px.colors.diverging.Tealrose,
    labels={
        'mean_ghgs': 'GHG Emissions (kg CO₂e/day)',
        'mean_land': 'Land Use (m²/day)',
        'mean_watscar': 'Water Scarcity (liters/kg)',
        'mean_eut': 'Eutrophication (g PO₄³⁻ eq/day)',
        'mean_ghgs_ch4': 'Methane Emissions (kg CH₄/day)',
        'mean_ghgs_n2o': 'Nitrous Oxide Emissions (kg N₂O/day)',
        'mean_bio': 'Biodiversity Impact (loss units)',
        'mean_watuse': 'Water Use (liters/day)',
        'mean_acid': 'Acidification (g SO₂ eq/day)'
    },
    title="Environmental Impacts by Diet Group (Female)"
)

# Combine both figures
fig = go.Figure()

# Add traces
for trace in fig_male.data:
    fig.add_trace(trace)
for trace in fig_female.data:
    fig.add_trace(trace)

# Set initial visibility
fig.data[0].visible = True
fig.data[1].visible = False

# Add buttons
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.5,
            y=1.2,
            showactive=True,
            buttons=list([
                dict(
                    label="Male",
                    method="update",
                    args=[
                        {"visible": [True, False]},
                        {"title": {"text": "Environmental Impacts by Diet Group (Male) | Bottom to Top: Vegan, Vegetarian, Pescatarian, Low Meat, Medium Meat, High Meat"}}
                    ]
                ),
                dict(
                    label="Female",
                    method="update",
                    args=[
                        {"visible": [False, True]},
                        {"title": {"text": "Environmental Impacts by Diet Group (Female) | Bottom to Top: Vegan, Vegetarian, Pescatarian, Low Meat, Medium Meat, High Meat"}}
                    ]
                )
            ])
        )
    ],
    title={"text": "Environmental Impacts by Diet Group (Male) | Bottom to Top: Vegan, Vegetarian, Pescatarian, Low Meat, Medium Meat, High Meat"},
    plot_bgcolor='white',
    margin=dict(l=50, r=50, t=100, b=50)
)

# Show figure
fig.show()

# Save HTML
# fig.write_html(script_dir + '/parallel_plot_gender_switch_clean.html')
