import streamlit as st
import pandas as pd
import mplsoccer as mpl
from mplsoccer import VerticalPitch
import seaborn as sns
import matplotlib.pyplot as plt


tw = pd.read_csv('C:/Users/user/Desktop/Senior_Proj/str_app_pos/tw.csv')


st.title('Analyzing Goal Scoring Patterns: Insights from Player Positions')
st.subheader('We applied the FP-Growth Algorithm on a dataframe containing goal logs for LALIGA 23/24, we got the following combinations')
map = pd.DataFrame(
    {
        'position': ['LW', 'ST', 'RW', 'CAM', 'CDM', 'MF', 'LB', 'LCB', 'RCB', 'RB', 'GK'],
        'position_id': [11, 9, 10, 8, 4, 7, 3, 6, 5, 2, 1],
        'player': ['LW', 'ST', 'RW', 'CAM', 'CDM', 'MF', 'LB', 'CB', 'RCB', 'RB', 'GK'],
    }
)

# For combinnations only
combinations = tw.groupby(['GCA2-p', 'GCA1-p', 'Scorer-p']).size().reset_index(name='freq')

total_goals = len(tw)
combinations['percentage'] = combinations['freq'] / total_goals * 100

sort_combinations = combinations.sort_values(by='percentage', ascending=False)

top_comb = sort_combinations.head(10)
top_comb.reset_index(drop = True, inplace = True)


pitch = VerticalPitch(pitch_type='opta', pitch_color='#22312b', line_color='white', line_alpha=0.2,
                      line_zorder=3)
fig, axes = pitch.grid(endnote_height=0, figheight=13, title_height=0.1, title_space=0, space=0)
fig.set_facecolor('black')

form = pitch.formations_dataframe
form = form[form['formation'] == '433']


def locater(i, df, player): # function to locate coordinates of player
    shirt = map.loc[map['player'] == df[player][i], 'position_id'].iloc[0] # to locate the shirt number of player
    coord = form.loc[form['opta'] == shirt] # locate the row of coordinates of player
    return coord


def drawer(df, i):
    if (df['GCA2-p'][i] == 'NA' and df['GCA1-p'][i] == 'NA' ):
        coord = locater(i, df, 'Scorer-p')
        pitch.arrows(coord['x'], coord['y'], (form['x'][10] + 10), form['y'][10], width = 2, headwidth = 10, headlength = 10, color = color, ax =axes['pitch'])

    elif (df['GCA2-p'][i] == 'NA'):
        coord = locater(i, df, 'GCA1-p')
        end = locater(i, df, 'Scorer-p')
        pitch.arrows(coord['x'], coord['y'], end['x'], end['y'], width = 2, headwidth = 10, headlength = 10, color = color, ax =axes['pitch'])
    
    else:
        coord = locater(i, df, 'GCA2-p')
        end = locater(i, df, 'GCA1-p')
        score = locater(i, df, 'Scorer-p')
        pitch.arrows(coord['x'], coord['y'], end['x'], end['y'], width = 2, headwidth = 10, headlength = 10, color = color, ax =axes['pitch'])
        pitch.arrows(end['x'], end['y'], score['x'], score['y'], width = 2, headwidth = 10, headlength = 10, color = color, ax =axes['pitch'])


st.write(top_comb)
st.subheader('LEGEND')
st.markdown('''Scorer-p: Position of the scorer of the goal  
GCA1-p: Position of the Assister of the goal  
GCA2-p: Position of the last player that passed the ball to the assister (created a chance)  
freq: Frequency of occurrence of the combination  
percentage: Percentage of occurrence relative to other combinations''')
st.write("***")
# title
axes['title'].axis('off')
axes['title'].text(0.5, 0.6, 'Goal Scoring Combinations', ha='center', va='center', color='white',
                fontsize=20)
axes['title'].text(0.5, 0.3, 'Combinations Only', ha='center', va='center', color='white', fontsize=14)


text_names = pitch.formation('433', kind='text', positions=map.position_id,
                            text=map.player, ax=axes['pitch'],
                            xoffset=-5,  # player names
                            ha='center', va='center', color='white', fontsize=11)

badge_axes = pitch.formation('433', kind='scatter', positions=map.position_id,
                            height=10, ax=axes['pitch'],
                            xoffset=0, color = 'blue'  # players
                            )

perc = sorted(top_comb['percentage'].unique(), reverse = True)
fire = sns.color_palette("plasma", len(perc))
color_dict = dict(zip(perc, fire))

legend_entries = [(percentage, color_dict[percentage]) for percentage in perc]

# Sort legend entries in descending order based on percentages
sorted_legend = sorted(legend_entries, key=lambda x: x[0], reverse=True)

legend_handles = []
for percentage, color in sorted_legend:
    legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', label=f'{percentage:.2f}%', markerfacecolor=color, markersize=10))

# Add legend to the plot
axes['pitch'].legend(handles=legend_handles, loc='upper right', fontsize=10)

for i in range(0, len(top_comb)):
    color = color_dict[top_comb['percentage'][i]]

    drawer(top_comb, i)

st.write(fig)

st.subheader('Conclusion')
st.write('***')
st.write("Based of this plot, we can see that aside of the striker scoring most of the goals by himself, we can see that midfielders are being involved in most of the striker's goals apart from LW and RW or other positions")
st.write("***")
st.write("Also, we noticed that the combination CM => LB => ST and CM => RB => ST are one of the most repetitive amongst LaLiga, while this may be a broad assumption, but it surely indicates that most of the spanish teams rely on the RB or LB to cut in and assist the ST in creating goal opportunities, especially through aerials" )