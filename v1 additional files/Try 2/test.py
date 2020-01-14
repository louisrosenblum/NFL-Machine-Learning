import requests
from bs4 import BeautifulSoup
import re
import csv

# Constants

# Hardcoding 2019 schedules
schedules = {}

schedules['ARI'] = ['DET','BAL','CAR','SEA','CIN','ATL','NYG','NOR','SFO','TAM','SFO','BYE','LAR','PIT','CLE','SEA','LAR']
schedules['ATL'] = ['MIN','PHI','IND','TEN','HOU','ARI','LAR','SEA','BYE','NOR','CAR','TAM','NOR','CAR','SFO','JAX','TAM']
schedules['BAL'] = ['MIA','ARI','KAN','CLE','PIT','CIN','SEA','BYE','NWE','CIN','HOU','LAR','SFO','BUF','NYJ','CLE','PIT']
schedules['BUF'] = ['NYJ','NYG','CLE','NWE','TEN','BYE','MIA','PHI','WAS','CLE','MIA','DEN','DAL','BAL','PIT','NWE','NYJ']
schedules['CAR'] = ['LAR','TAM','ARI','HOU','JAX','TAM','BYE','SFO','TEN','GNB','ATL','NOR','WAS','ATL','SEA','IND','NOR']
schedules['CHI'] = ['GNB','DEN','WAS','MIN','OAK','BYE','NOR','LAC','PHI','DET','LAR','NYG','DET','DAL','GNB','KAN','MIN']
schedules['CIN'] = ['SEA','SFO','BUF','PIT','ARI','BAL','JAX','LAR','BYE','BAL','OAK','PIT','NYJ','CLE','NWE','MIA','CLE']                   
schedules['CLE'] = ['TEN','NYJ','LAR','BAL','SFO','SEA','BYE','NWE','DEN','BUF','PIT','MIA','PIT','CIN','ARI','BAL','CIN']                   
schedules['DAL'] = ['NYG','WAS','MIA','NOR','GNB','NYJ','PHI','BYE','NYG','MIN','DET','NWE','BUF','CHI','LAR','PHI','WAS']                   
schedules['DEN'] = ['OAK','CHI','GNB','JAX','LAC','TEN','KAN','IND','CLE','BYE','MIN','BUF','LAC','HOU','KAN','DET','OAK']                   
schedules['DET'] = ['ARI','LAC','PHI','KAN','BYE','GNB','MIN','NYG','OAK','CHI','DAL','WAS','CHI','MIN','TAM','DEN','GNB']                   
schedules['GNB'] = ['CHI','MIN','DEN','PHI','DAL','DET','OAK','KAN','LAC','CAR','BYE','SFO','NYG','WAS','CHI','MIN','DET']                   
schedules['HOU'] = ['NOR','JAX','LAC','CAR','ATL','KAN','IND','OAK','JAX','BYE','BAL','IND','NWE','DEN','TEN','TAM','TEN']                   
schedules['IND'] = ['LAC','TEN','ATL','OAK','KAN','BYE','HOU','DEN','PIT','MIA','JAX','HOU','TEN','TAM','NOR','CAR','JAX']                   
schedules['JAX'] = ['KAN','HOU','TEN','DEN','CAR','NOR','CIN','NYJ','HOU','BYE','IND','TEN','TAM','LAC','OAK','ATL','IND']                   
schedules['KAN'] = ['JAX','OAK','BAL','DET','IND','HOU','DEN','GNB','MIN','TEN','LAC','BYE','OAK','NWE','DEN','CHI','LAC']
schedules['LAC'] = ['IND','DET','HOU','MIA','DEN','PIT','TEN','CHI','GNB','OAK','KAN','BYE','DEN','JAX','MIN','OAK','KAN']
schedules['LAR'] = ['CAR','NOR','CLE','TAM','SEA','SFO','ATL','CIN','BYE','PIT','CHI','BAL','ARI','SEA','DAL','SFO','ARI']
schedules['MIA'] = ['BAL','NWE','DAL','LAC','BYE','WAS','BUF','PIT','NYJ','IND','BUF','CLE','PHI','NYJ','NYG','CIN','NWE']
schedules['MIN'] = ['ATL','GNB','OAK','CHI','NYG','PHI','DET','WAS','KAN','DAL','DEN','BYE','SEA','DET','LAC','GNB','CHI']
schedules['NWE'] = ['PIT','MIA','NYJ','BUF','WAS','NYG','NYJ','CLE','BAL','BYE','PHI','DAL','HOU','KAN','CIN','BUF','MIA']
schedules['NOR'] = ['HOU','LAR','SEA','DAL','TAM','JAX','CHI','ARI','BYE','ATL','TAM','CAR','ATL','SFO','IND','TEN','CAR']
schedules['NYG'] = ['DAL','BUF','TAM','WAS','MIN','NWE','ARI','DET','DAL','NYJ','BYE','CHI','GNB','PHI','MIA','WAS','PHI']
schedules['NYJ'] = ['BUF','CLE','NWE','BYE','PHI','DAL','NWE','JAX','MIA','NYG','WAS','OAK','CIN','MIA','BAL','PIT','BUF']
schedules['OAK'] = ['DEN','KAN','MIN','IND','CHI','BYE','GNB','HOU','DET','LAC','CIN','NYJ','KAN','TEN','JAX','LAC','DEN']
schedules['PHI'] = ['WAS','ATL','DET','GNB','NYJ','MIN','DAL','BUF','CHI','BYE','NWE','SEA','MIA','NYG','WAS','DAL','NYG']
schedules['PIT'] = ['NWE','SEA','SFO','CIN','BAL','LAC','BYE','MIA','IND','LAR','CLE','CIN','CLE','ARI','BUF','NYJ','BAL']
schedules['SFO'] = ['TAM','CIN','PIT','BYE','CLE','LAR','WAS','CAR','ARI','SEA','ARI','GNB','BAL','NOR','ATL','LAR','SEA']
schedules['SEA'] = ['CIN','PIT','NOR','ARI','LAR','CLE','BAL','ATL','TAM','SFO','BYE','PHI','MIN','LAR','CAR','ARI','SFO']
schedules['TAM'] = ['SFO','CAR','NYG','LAR','NOR','CAR','BYE','TEN','SEA','ARI','NOR','ATL','JAX','IND','DET','HOU','ARI']
schedules['TEN'] = ['CLE','IND','JAX','ATL','BUF','DEN','LAC','TAM','CAR','KAN','BYE','JAX','IND','OAK','HOU','NOR','HOU']
schedules['WAS'] = ['PHI','DAL','CHI','NYG','NWE','MIA','SFO','MIN','BUF','BYE','NYJ','DET','CAR','GNB','PHI','NYG','DAL']

# Convert team abbreviation to CBS data
rb_teams = {}
wr_teams = {}
te_teams = {}

# RB conversion
rb_teams['ARI'] = 'RB vs Cardinals'
rb_teams['ATL'] = 'RB vs Falcons'
rb_teams['BAL'] = 'RB vs Ravens'
rb_teams['BUF'] = 'RB vs Bills'
rb_teams['CAR'] = 'RB vs Panthers'
rb_teams['CHI'] = 'RB vs Bears'
rb_teams['CIN'] = 'RB vs Bengals'               
rb_teams['CLE'] = 'RB vs Browns'                 
rb_teams['DAL'] = 'RB vs Cowboys'                
rb_teams['DEN'] = 'RB vs Broncos'                 
rb_teams['DET'] = 'RB vs Lions'              
rb_teams['GNB'] = 'RB vs Packers'               
rb_teams['HOU'] = 'RB vs Texans'            
rb_teams['IND'] = 'RB vs Colts'                
rb_teams['JAX'] = 'RB vs Jaguars'          
rb_teams['KAN'] = 'RB vs Chiefs'
rb_teams['LAC'] = 'RB vs Chargers'
rb_teams['LAR'] = 'RB vs Rams'
rb_teams['MIA'] = 'RB vs Dolphins'
rb_teams['MIN'] = 'RB vs Vikings'
rb_teams['NWE'] = 'RB vs Patriots'
rb_teams['NOR'] = 'RB vs Saints'
rb_teams['NYG'] = 'RB vs Giants'
rb_teams['NYJ'] = 'RB vs Jets'
rb_teams['OAK'] = 'RB vs Raiders'
rb_teams['PHI'] = 'RB vs Eagles'
rb_teams['PIT'] = 'RB vs Steelers'
rb_teams['SFO'] = 'RB vs 49ers'
rb_teams['SEA'] = 'RB vs Seahawks'
rb_teams['TAM'] = 'RB vs Buccaneers'
rb_teams['TEN'] = 'RB vs Titans'
rb_teams['WAS'] = 'RB vs Redskins'

# WR conversion
wr_teams['ARI'] = 'WR vs Cardinals'
wr_teams['ATL'] = 'WR vs Falcons'
wr_teams['BAL'] = 'WR vs Ravens'
wr_teams['BUF'] = 'WR vs Bills'
wr_teams['CAR'] = 'WR vs Panthers'
wr_teams['CHI'] = 'WR vs Bears'
wr_teams['CIN'] = 'WR vs Bengals'               
wr_teams['CLE'] = 'WR vs Browns'                 
wr_teams['DAL'] = 'WR vs Cowboys'                
wr_teams['DEN'] = 'WR vs Broncos'                 
wr_teams['DET'] = 'WR vs Lions'              
wr_teams['GNB'] = 'WR vs Packers'               
wr_teams['HOU'] = 'WR vs Texans'            
wr_teams['IND'] = 'WR vs Colts'                
wr_teams['JAX'] = 'WR vs Jaguars'          
wr_teams['KAN'] = 'WR vs Chiefs'
wr_teams['LAC'] = 'WR vs Chargers'
wr_teams['LAR'] = 'WR vs Rams'
wr_teams['MIA'] = 'WR vs Dolphins'
wr_teams['MIN'] = 'WR vs Vikings'
wr_teams['NWE'] = 'WR vs Patriots'
wr_teams['NOR'] = 'WR vs Saints'
wr_teams['NYG'] = 'WR vs Giants'
wr_teams['NYJ'] = 'WR vs Jets'
wr_teams['OAK'] = 'WR vs Raiders'
wr_teams['PHI'] = 'WR vs Eagles'
wr_teams['PIT'] = 'WR vs Steelers'
wr_teams['SFO'] = 'WR vs 49ers'
wr_teams['SEA'] = 'WR vs Seahawks'
wr_teams['TAM'] = 'WR vs Buccaneers'
wr_teams['TEN'] = 'WR vs Titans'
wr_teams['WAS'] = 'WR vs Redskins'

# TE conversion
te_teams['ARI'] = 'TE vs Cardinals'
te_teams['ATL'] = 'TE vs Falcons'
te_teams['BAL'] = 'TE vs Ravens'
te_teams['BUF'] = 'TE vs Bills'
te_teams['CAR'] = 'TE vs Panthers'
te_teams['CHI'] = 'TE vs Bears'
te_teams['CIN'] = 'TE vs Bengals'               
te_teams['CLE'] = 'TE vs Browns'                 
te_teams['DAL'] = 'TE vs Cowboys'                
te_teams['DEN'] = 'TE vs Broncos'                 
te_teams['DET'] = 'TE vs Lions'              
te_teams['GNB'] = 'TE vs Packers'               
te_teams['HOU'] = 'TE vs Texans'            
te_teams['IND'] = 'TE vs Colts'                
te_teams['JAX'] = 'TE vs Jaguars'          
te_teams['KAN'] = 'TE vs Chiefs'
te_teams['LAC'] = 'TE vs Chargers'
te_teams['LAR'] = 'TE vs Rams'
te_teams['MIA'] = 'TE vs Dolphins'
te_teams['MIN'] = 'TE vs Vikings'
te_teams['NWE'] = 'TE vs Patriots'
te_teams['NOR'] = 'TE vs Saints'
te_teams['NYG'] = 'TE vs Giants'
te_teams['NYJ'] = 'TE vs Jets'
te_teams['OAK'] = 'TE vs Raiders'
te_teams['PHI'] = 'TE vs Eagles'
te_teams['PIT'] = 'TE vs Steelers'
te_teams['SFO'] = 'TE vs 49ers'
te_teams['SEA'] = 'TE vs Seahawks'
te_teams['TAM'] = 'TE vs Buccaneers'
te_teams['TEN'] = 'TE vs Titans'
te_teams['WAS'] = 'TE vs Redskins'

# Week 13 scores
w13 = {}

w13['Michael Thomas'] = 30.8
w13['Christian McCaffrey'] = 37.5
w13['Austin Ekeler'] = 13.1
w13['Chris Godwin'] = 17.1
w13['Dalvin Cook'] = 7.3
w13['Leonard Fournette'] = 12.3
w13['Derrick Henry'] = 8.6
w13['Josh Jacobs'] = 12.9
w13['DeAndre Hopkins'] = 17.9
w13['Kenny Golladay'] = 7.4
w13['Ezekiel Elliott'] = 31
w13['Cooper Kupp'] = 16.1
w13['Amari Cooper'] = 2.9
w13['Nick Chubb'] = 23.8
w13['Jarvis Landry'] = 7.3
w13['Julian Edelman'] = 2.9
w13['Keenan Allen'] = 18.9
w13['Chris Carson'] = 26.7
w13['D.J. Moore'] = 20.3
w13['Alvin Kamara'] = 13.9
w13['Robert Woods'] = 5.7
w13['Allen Robinson'] = 19.5
w13['Darius Slayton'] = 11.1
w13['Courtland Sutton'] = 11.9
w13['James White'] = 15.2
w13['Aaron Jones'] = 17.1
w13['Julio Jones'] = 38.4
w13['Stefon Diggs'] = 12
w13['DeVante Parker'] = 23.2
w13['Travis Kelce'] = 25.2
w13['Zach Ertz'] = 17.1
w13['Saquon Barkley'] = 30.3
w13['Phillip Lindsay'] = 3.2
w13['Darren Waller'] = 20.2
w13['Tyler Lockett'] = 26
w13['Michael Gallup'] = 1.6
w13['John Brown'] = 16.9
w13['Terry McLaurin'] = 24
w13['Devin Singletary'] = 8.9
w13['A.J. Brown'] = 25.4
w13['Mark Andrews'] = 15.2
w13['Royce Freeman'] = 6.6
w13['George Kittle'] = 26.4
w13['Odell Beckham'] = 14.6
w13['Sterling Shepard'] = 20.1
w13['Austin Hooper'] = 5
w13['LeVeon Bell'] = 10.8
w13['Christian Kirk'] = 10.1
w13['Emmanuel Sanders'] = 2.9
w13['Tyreek Hill'] = 23.8
w13['Golden Tate'] = 12.1
w13['Cole Beasley'] = 1.6
w13['Mike Williams'] = 17.1
w13['David Johnson'] = 0.6
w13['James Conner'] = 15.1
w13['D.K. Metcalf'] = 11.6
w13['Davante Adams'] = 23.3
w13['Deebo Samuel'] = 4.7
w13['Tyler Boyd'] = 5.6
w13['Raheem Mostert'] = 10.9
w13['Marquise Brown'] = 14.5
w13['Duke Johnson'] = 4.3
w13['Kenyan Drake'] = 39.6
w13['Mark Ingram'] = 23.6
w13['Curtis Samuel'] = 16.4
w13['Miles Sanders'] = 35.2
w13['Melvin Gordon'] = 7.4
w13['Tarik Cohen'] = 15.5
w13['Marlon Mack'] = 1.9
w13['Todd Gurley'] = 20.8
w13['Larry Fitzgerald'] = 7.2
w13['Dede Westbrook'] = 4.1
w13['Joe Mixon'] = 18.6
w13['Kareem Hunt'] = 15.6
w13['Ronald Jones'] = 5.9
w13['David Montgomery'] = 5.9
w13['Randall Cobb'] = 0.7
w13['Zach Pascal'] = 8.4
w13['Danny Amendola'] = 18.2
w13['Jamaal Williams'] = 4.3
w13['Will Fuller'] = 11.1
w13['T.Y. Hilton'] = 6.5
w13['Matt Breida'] = 1.7
w13['DeAndre Washington'] = 4.2
w13['Sammy Watkins'] = 9.9
w13['Chris Conley'] = 20.9
w13['Mecole Hardman'] = 2
w13['Jared Cook'] = 9.4
w13['Jamison Crowder'] = 27
w13['Devonta Freeman'] = 7.5
w13['Hunter Henry'] = 2.9
w13['Latavius Murray'] = 6.9
w13['Justin Jackson'] = 3.7
w13['Jalen Richard'] = 5.6
w13['Tyrell Williams'] = 12.5
w13['Adam Thielen'] = 6
w13['Kerrith Whyte'] = 0.5
w13['Corey Davis'] = 8.7
w13['Robby Anderson'] = 12.6
w13['Dallas Goedert'] = 10.5
w13['Kendrick Bourne'] = 2.1
w13['Anthony Miller'] = 26.8
w13['Sony Michel'] = 11.3
w13['Carlos Hyde'] = 16.4
w13['Jaylen Samuels'] = 1.4
w13['Mike Gesicki'] = 8.7
w13['Chase Edmonds'] = 0
w13['James Washington'] = 13.3
w13['Kenny Stills'] = 18.5
w13['Noah Fant'] = 7.6
w13['Bennie Fowler'] = 0
w13['Rex Burkhead'] = 13.9
w13['Mohamed Sanu'] = 3.3
w13['Phillip Dorsett'] = 0
w13['Brandin Cooks'] = 8.6
w13['Tevin Coleman'] = 4
w13['Jacob Hollister'] = 5.3
w13['Willie Snead'] = 2.5
w13['Chris Thompson'] = 4.6
w13['Jason Witten'] = 13.6
w13['Adrian Peterson'] = 18.1
w13['LeSean McCoy'] = 1.6
w13['Kyle Rudolph'] = 7.8
w13['Allen Hurns'] = 1.9
w13['Peyton Barber'] = 6
w13['Tyler Higbee'] = 23.1
w13['Diontae Johnson'] = 9.2
w13['Ted Ginn'] = 2.3
w13['Dion Lewis'] = 9.1
w13['Demarcus Robinson'] = 4.1
w13['Jimmy Graham'] = 1
w13['Nyheim Hines'] = 3.2
w13['Olabisi Johnson'] = 3.5
w13['Darren Fells'] = 1.2
w13['Allen Lazard'] = 3.4
w13['Jordan Akins'] = 2.7
w13['Jack Doyle'] = 4.1
w13['Dawson Knox'] = 2.1
w13['Ricky Seals-Jones'] = 15.9
w13['Dare Ogunbowale'] = 2.6
w13['Russell Gage'] = 8.3
w13['Blake Jarwin'] = 6
w13['Tyler Eifert'] = 7.4
w13['Tony Pollard'] = 22.3
w13['Kelvin Harmon'] = 4.2
w13['Irv Smith Jr.'] = 8.8
w13['Marcus Johnson'] = 5.7
w13['Cody Latimer'] = 3.1
w13['Jonathan Williams'] = 0
w13['Josh Gordon'] = 4.8
w13['Hayden Hurst'] = 2.9
w13['Jakobi Meyers'] = 0
w13['Jonnu Smith'] = 16.7
w13['Keelan Cole'] = 10.6
w13['Benny Snell'] = 0.1
w13['Josh Reynolds'] = 5.6
w13['Tajae Sharpe'] = 4.8
w13['Marquez Valdes-Scantling'] = 0
w13['John Ross'] = 4.4
w13['Demetrius Harris'] = 2.3
w13['Pharoh Cooper'] = 2.7
w13['C.J. Prosise'] = 3.5
w13['Cameron Brate'] = 6.3
w13['Anthony Firkser'] = 1.7
w13['Breshad Perriman'] = 34.6
w13['Laquon Treadwell'] = 0
w13['Albert Wilson'] = 10.9
w13['Seth Roberts'] = 15.6
w13['Alec Ingold'] = 5.2
w13['Alex Erickson'] = -0.4
w13['Ryquell Armstead'] = 0.1
w13['Brandon Bolden'] = 0
w13['David Moore'] = 0
w13['Khari Blasingame'] = 1
w13['Andy Isabella'] = 1.3
w13['O.J. Howard'] = 8.6
w13['Nick Bellore'] = 0
w13['Greg Ward'] = 19.1
w13['Geronimo Allison'] = 3.9
w13['Boston Scott'] = 13.5
w13['Nick Boyle'] = 0
w13['Frank Gore'] = 1.5
w13['Andrew Beck'] = 3.3
w13['Logan Thomas'] = 0
w13['Kalif Raymond'] = 1.2
w13['Damiere Byrd'] = 14.6
w13['Cody Core'] = 0
w13['Byron Pringle'] = 0
w13['Isaiah McKenzie'] = 0
w13['JJ Arcega-Whiteside'] = 0
w13['T.J. Jones'] = 0
w13['Devontae Booker'] = 0.5
w13['Malik Turner'] = 5.6
w13['Steven Sims'] = 15.5
w13['Dontrelle Inman'] = 4.5
w13['Patrick Laird'] = 7.4
w13['Miles Boykin'] = 7.5
w13['Gus Edwards'] = 3.5
w13['Jaron Brown'] = 1.9
w13['Jaeden Graham'] = 0
w13['Antonio Callaway'] = 0
w13['Richie James'] = 0
w13['Dontrell Hilliard'] = 0
w13['DaeSean Hamilton'] = 3.3
w13['Jesper Horsted'] = 0.8
w13['Elijhaa Penny'] = -0.2
w13['Isaiah Ford'] = 5.1
w13['Jarius Wright'] = 1.9
w13['Stephen Carlson'] = 0
w13['Josh Hill'] = 7.5
w13['Ameer Abdullah'] = 2.5
w13['Rico Gafford'] = 0
w13['Charles Clay'] = 2.8
w13['Justin Hardy'] = 0
w13['C.J. Ham'] = 4.8
w13['Travis Homer'] = 0.7
w13['J.D. McKissic'] = 2.9
w13['Damion Ratley'] = 5.3
w13['Kaden Smith'] = 6.8
w13['Joshua Perkins'] = 0
w13['Dante Pettis'] = 0
w13['Derek Carrier'] = 1.5
w13['Mack Hollins'] = 0
w13['Jon Hilliman'] = 0
w13['Jeff Wilson'] = 0
w13['Seth Devalve'] = 4.3
w13['Ross Dwelley'] = 0
w13['Ian Thomas'] = 4.3
w13['Zay Jones'] = 1.5
w13['Tim Patrick'] = 5.6
w13['Malcolm Brown'] = 0
w13['Kyle Juszczyk'] = 8.7
w13['Ashton Dulin'] = 1.4
w13['Deonte Harris'] = 1.1
w13['KhaDarel Hodge'] = 0
w13['Maxx Williams'] = 1.4
w13['Jeremy Sprinkle'] = 3.3
w13['Rashard Higgins'] = 0
w13['Robert Tonyan'] = 1.5
w13['Christian Blake'] = 0
w13['Giovani Bernard'] = 5.7
w13['Javon Wims'] = 0
w13['Darrell Henderson'] = 0
w13['Keelan Doss'] = 2.7
w13['Tyler Conklin'] = 0
w13['Cody Hollister'] = 0
w13['Trey Edmunds'] = 0
w13['Jesse James'] = 6.1
w13['Brian Hill'] = 1.6
w13['Jake Kumerow'] = 5.9
w13['Tavon Austin'] = 13.2
w13['Jason Moore'] = 0
w13['Javorius Allen'] = 8.8
w13['J.P. Holtz'] = 0.9
w13['Robert Davis'] = 0
w13['Trent Sherfield'] = 0
w13['Olamide Zaccheaus'] = 0
w13['Scott Miller'] = 13.9
w13['Derek Watt'] = 0
w13['Nick Vannett'] = 9
w13['Darwin Thompson'] = 4.9
w13['Chris Moore'] = 0
w13['Isaac Nauta'] = 2
w13['Trevon Wesco'] = 0
w13['Darius Jennings'] = 0
w13['JJ Nelson'] = 0
w13['Trevor Davis'] = 0
w13['Ty Johnson'] = 4
w13['Jeff Heuerman'] = 0
w13['Wendell Smallwood'] = 0
w13['Ben Koyack'] = 0
w13['Marcedes Lewis'] = 1.6
w13['Ben Watson'] = 0
w13['Daniel Brown'] = 1.4
w13['Ventell Bryant'] = 0
w13['Justin Watson'] = 3.7
w13['Tyler Kroft'] = 8.4
w13['Levine Toilolo'] = 0
w13['Mo Alie-Cox'] = 0
w13['Matt LaCosse'] = 5.2
w13['Marcell Ateman'] = 0
w13['Troymaine Pope'] = 0
w13['Diontae Spencer'] = 0
w13['Mike Thomas'] = 1.5
w13['Michael Crabtree'] = 0
w13['Jordan Wilkins'] = 8.7
w13['Dalton Schultz'] = 0
w13['Lee Smith'] = 0
w13['Michael Walker'] = 0
w13['C.J. Uzomah'] = 1.8
w13['Danny Vitale'] = 0
w13['Myles Gaskin'] = 9.2
w13['Andre Patton'] = 1.8
w13['Mike Boone'] = 17.6
w13['Vyncint Smith'] = 7
w13['Ty Montgomery'] = 2
w13['C.J. Board'] = 1.8
w13['Fred Brown'] = 0
w13['Robert Foster'] = 0
w13['MyCole Pruitt'] = 0
w13['Justice Hill'] = 1.5
w13['Dan Arnold'] = 7.6
w13['Chris Manhertz'] = 0
w13['Troy Fumagalli'] = 1.7
w13['DeAndre Carter'] = 0
w13['Scott Simonson'] = 1.1
w13['Braxton Berrios'] = 0
w13['DeAndrew White'] = 0
w13['Buddy Howell'] = 0
w13['Virgil Green'] = 0
w13['Riley Ridley'] = 3
w13['Anthony Sherman'] = 0
w13['Chris Hogan'] = 2.3
w13['Patrick DiMarco'] = 0
w13['Alfred Morris'] = 0
w13['Clive Walford'] = 5.4
w13['Cordarrelle Patterson'] = 1.6
w13['Zach Line'] = 0.4
w13['Alex Armah'] = 0
w13['Durham Smythe'] = 0
w13['Mike Davis'] = 0
w13['Dwayne Washington'] = 2
w13['Hale Hentges'] = 0
w13['Deon Cain'] = 0
w13['Johnny Mundt'] = 3.5
w13['Zach Zenner'] = 0
w13['Dalyn Dawkins'] = 0
w13['Andre Roberts'] = 1.7
w13['Tevin Jones'] = 0
w13['Brandon Zylstra'] = 0
w13['Jay Ajayi'] = 0
w13['Lance Kendricks'] = 0
w13['Blake Bell'] = 6.1
w13['Tanner Hudson'] = 2.4
w13['Darrius Shepherd'] = 0
w13['Luke Stocker'] = 1.9
w13['John Kelly'] = 0
w13['Reggie Bonnafon'] = 0
w13['Kenjon Barner'] = -0.6
w13['Bobo Wilson'] = 0
w13['Stanley Morgan'] = 0
w13['Johnny Holton'] = 1.9
w13['Qadree Ollison'] = 6.1
w13['Josh Adams'] = 0
w13['Keith Smith'] = 0
w13['Tony Brooks-James'] = 0
w13['Paul Perkins'] = 0
w13['Spencer Ware'] = 5.5
w13['C.J. Anderson'] = 0




# Change this value to reflect ppr scoring (0, 0.5, 1)
ppr = 1

# Change this value for the current week of projections
week = 16

# URLs for position data

rb_url = 'https://www.cbssports.com/fantasy/football/stats/posvsdef/RB/all/avg/standard'
wr_url = 'https://www.cbssports.com/fantasy/football/stats/posvsdef/WR/all/avg/standard'
te_url = 'https://www.cbssports.com/fantasy/football/stats/posvsdef/TE/all/avg/standard'

# HTML cleaner

def _strip_html(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', str(text))

## Scrape for RB stats
res = requests.get(rb_url)
soup = BeautifulSoup(res.text,features="html.parser")

parsed = soup.findAll(
    'table', {
        'class': 'data compact',
    }
)
rows = parsed[0].findAll('td')

column_len = 13

grouped_rows = [
    rows[i:i+column_len] for i in range(18, len(rows), column_len)
]


rb_table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]

rb_list = []

for i in rb_table:
    rb_list.append(list(i))


## Scrape for WR stats
res = requests.get(wr_url)
soup = BeautifulSoup(res.text,features="html.parser")

parsed = soup.findAll(
    'table', {
        'class': 'data compact',
    }
)
rows = parsed[0].findAll('td')

column_len = 13

grouped_rows = [
    rows[i:i+column_len] for i in range(18, len(rows), column_len)
]


wr_table = [map(lambda x: _strip_html(x), row) for row in grouped_rows]

wr_list = []

for i in wr_table:
    wr_list.append(list(i))


## Scrape for TE stats
res = requests.get(te_url)
soup = BeautifulSoup(res.text,features="html.parser")

parsed = soup.findAll(
    'table', {
        'class': 'data compact',
    }
)
rows = parsed[0].findAll('td')

column_len = 13

grouped_rows = [
    rows[i:i+column_len] for i in range(18, len(rows), column_len)
]


te_table =[map(lambda x: _strip_html(x), row) for row in grouped_rows]

te_list = []

for i in te_table:
    te_list.append(list(i))

cell = []
z = 0
with open('scrimmage.csv', mode='r') as scrimmage:
    reader = csv.reader(scrimmage, delimiter=',', quoting=csv.QUOTE_NONE)
    with open('test.csv',mode='w') as matchups:
        writer = csv.writer(matchups, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')
        for row in reader:
            cell = []
            if(z==0):
                z = z+1
                continue
            cell.append(row[0])
            pos = str(row[3]).upper()

            if(pos == 'RB'):
                table = rb_list
                conv = rb_teams
            elif(pos == 'WR'):
                table = wr_list
                conv = wr_teams
            elif (pos == 'TE'):
                table = te_list
                conv = te_teams
            else:
                continue
                     
            opp = schedules[row[1]]

            i = week -1

            
            #if(row[0] in w13):
                #cell.append(w13[row[0]])
            #else:
               #continue

            for k in range(2,28):
                if (k == 3):
                    continue
                cell.append(row[k])
                
            key = conv[opp[i]]
            for j in table:
                if (key == j[1]):
                    for k in range(10):
                        cell.append(j[k+2])
                                
            writer.writerow(cell)


            
    

