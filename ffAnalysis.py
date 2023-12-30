#!/usr/bin/env python3
#--------------------------------------------------------------- -------------
# Script used to generate plots for a Fantasy Football league.
#
# Author:         Zachariah Irwin
# Last modified:  December 30, 2023
#-----------------------------------------------------------------------------
import sys, os, argparse, subprocess

try:
  import numpy as np
except ImportError:
  sys.exit("ERROR. NumPy not installed.")

try:
  import matplotlib.pyplot as plt
except ImportError:
  sys.exit("ERROR. Matplotlib not installed.")

try:
  import pandas as pd
except ImportError:
  sys.exit("ERROR. Pandas not installed.")

try:
  from statsmodels.formula.api import ols
except ImportError:
  sys.exit("ERROR. statsmodels not installed.")

#----------------------------------------------------------------------
# Function to convert .xlsx sheet to pandas dataframe object.
# ----------
# Arguments:
# ----------
# args     (object)  command line arguments
#----------------------------------------------------------------------
def readData(args):
  #---------------------
  # Read in league data.
  #---------------------
  xlsx = pd.read_excel(args.inputFile, sheet_name=None)
  #------------------------------------
  # Transform into a single data frame.
  #------------------------------------
  all_sheets = []
  for name, sheet in xlsx.items():
    sheet['Sheet'] = name
    sheet = sheet.rename(columns=lambda x: x.split('\n')[-1])
    all_sheets.append(sheet)

  leagueData = pd.concat(all_sheets)
  leagueData.reset_index(inplace=True, drop=True)
  
  return leagueData
#----------------------------------------------------------------------
# Example for box plot explanation.
#
# Adapted from Robert Wilson:
# https://blog.rtwilson.com/automatically-annotating-a-boxplot-in-matplotlib/
#----------------------------------------------------------------------
def annotate_boxplot(bpdict, args, annotate_params=None,
                     x_offset=0.05, x_loc=0,
                     text_offset_x=35,
                     text_offset_y=20):
  """Annotates a matplotlib boxplot with labels marking various centile levels.

  Parameters:
  - bpdict: The dict returned from the matplotlib `boxplot` function. If you're using pandas you can
  get this dict by setting `return_type='dict'` when calling `df.boxplot()`.
  - annotate_params: Extra parameters for the plt.annotate function. The default setting uses standard arrows
  and offsets the text based on other parameters passed to the function
  - x_offset: The offset from the centre of the boxplot to place the heads of the arrows, in x axis
  units (normally just 0-n for n boxplots). Values between around -0.15 and 0.15 seem to work well
  - x_loc: The x axis location of the boxplot to annotate. Usually just the number of the boxplot, counting
  from the left and starting at zero.
  text_offset_x: The x offset from the arrow head location to place the associated text, in 'figure points' units
  text_offset_y: The y offset from the arrow head location to place the associated text, in 'figure points' units
  """
  if annotate_params is None:
      annotate_params = dict(xytext=(text_offset_x, text_offset_y), textcoords='offset points', arrowprops={'arrowstyle':'->'})

#  plt.annotate('Median', (x_loc + 1 + x_offset, bpdict['medians'][x_loc].get_ydata()[0]), **annotate_params)
#  plt.annotate('Mean', (x_loc + 1 + x_offset, bpdict['means'][x_loc].get_ydata()[0]), **dict(xytext=(text_offset_x+1, -text_offset_y), textcoords='offset points', arrowprops={'arrowstyle':'->'}))
  plt.annotate('25%', (x_loc + 1 + x_offset, bpdict['boxes'][x_loc].get_ydata()[0]), **dict(xytext=(text_offset_x, -text_offset_y), textcoords='offset points', arrowprops={'arrowstyle':'->'}))
  plt.annotate('75%', (x_loc + 1 + x_offset, bpdict['boxes'][x_loc].get_ydata()[2]), **annotate_params)
  plt.annotate('5%', (x_loc + 1 + x_offset, bpdict['caps'][x_loc*2].get_ydata()[0]), **dict(xytext=(text_offset_x, -text_offset_y), textcoords='offset points', arrowprops={'arrowstyle':'->'}))
  plt.annotate('95%', (x_loc + 1 + x_offset, bpdict['caps'][(x_loc*2)+1].get_ydata()[0]), **annotate_params)
  
  plt.savefig(LEAGUE + '/' + args.year + '/figures/box_plot_example.pdf', dpi=300, bbox_inches='tight') 

  return
#----------------------------------------------------------------------
# Function to analyze and plot scores based on teams' starting lineup.
# ----------
# Arguments:
# ----------
# a_LeagueData    (object)  pandas dataframe object for league data
#                           given by .xls sheets
# a_TeamOwnerList (list)    list of team owner names
# args            (object)  command line arguments
#----------------------------------------------------------------------
def actualScoreAnalysis(a_LeagueData, a_TeamOwnerList, args):
  #----------------------------------
  # Plot all the league data at once.
  #
  # This is commented out because
  # it's a little overwhelming.
  #----------------------------------
#  print("Plotting league data for weekly actual scores...") 
#  plt.figure() 
#  for teamID in range(0, len(a_TeamOwnerList)):
#    plt.plot(np.linspace(1, 14, 14), a_LeagueData.loc[leagueData["Sheet"] == "Actual", a_TeamOwnerList[teamID]].to_numpy(), '-', label=a_TeamOwnerList[teamID])
#  plt.xticks(np.linspace(1,14,14)) 
#  plt.legend(bbox_to_anchor=(1.02, 1.02), loc='upper left',\
#               handlelength=1, fontsize=14,\
#               edgecolor='k', framealpha=1.0)
#  plt.xlim([1,14])
#  plt.ylim([40,200])
#  plt.grid(axis='y')
#  plt.ylabel("Score", fontsize=14)
#  plt.xlabel("Week", fontsize=14)
#  plt.suptitle('Weekly scoring data', y=0.98, fontsize=18)
#  plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/scores/weekly_all.pdf', bbox_inches='tight', dpi=300)
#  plt.close()
#  print("Finished plotting league data for weekly actual scores.\n")
  #--------------------------
  # Individual plot per team.
  #--------------------------
  print("Plotting team data for weekly actual scores...")
  #----------------
  # Create texfile.
  #----------------
  texfile = open(LEAGUE + '/' + args.year + '/score_actual.tex', 'w')
  #------------
  # Make plots.
  #------------
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  for teamID in range(0, len(a_TeamOwnerList)):
    plt.figure() 
    plt.plot(np.linspace(1, 14, 14), a_LeagueData.loc[leagueData["Sheet"] == "Actual", a_TeamOwnerList[teamID]].to_numpy(), 'k.-')
    plt.xticks(np.linspace(1,14,14)) 
    plt.xlim([1,14])
    plt.ylim([40,200])
    plt.grid(axis='y')
    plt.ylabel("Score", fontsize=14)
    plt.xlabel("Week", fontsize=14)
    plt.suptitle('Weekly scoring data for ' + a_TeamOwnerList[teamID], y=0.98, fontsize=18)
    plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/actual/weekly_' + a_TeamOwnerList[teamID] + '.pdf', bbox_inches='tight', dpi=300)
    plt.close()
    #---------------------
    # Put plot in texfile.
    #---------------------
    texfile.write('\\subfigure{\includegraphics[width=0.3\\textwidth]{./figures/actual/weekly_' + a_TeamOwnerList[teamID] + '.pdf}}')
    if (teamID + 1) % 3 == 0 and 0 < teamID < len(a_TeamOwnerList):
      texfile.write('\\\\')
    texfile.write('\n')
  
  texfile.write('\\caption{Team scoring week-by-week.}\n')
  texfile.write('\\label{fig:Actual_Weekly_Team}\n')
  texfile.write('\\end{figure}\n\n')
    
  print("Finished plotting team data for weekly actual scores.\n")
  #-------------------------------
  # Compute the mean and variance.
  #-------------------------------
  mean_team  = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  std_team   = np.std(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  mean_total = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy())
  #-------------------------
  # Make box plots per week.
  #-------------------------
  print("Plotting team score variance...")
  plt.figure()
  plt.boxplot(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), showmeans=True)
  plt.plot(np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)), mean_total*np.ones(len(a_TeamOwnerList)), 'k--', label='League mean')
  plt.ylabel("Score",fontsize=16)
  plt.xlabel("Team",fontsize=16)
  plt.xticks(ticks=np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)),labels=a_LeagueData.columns.to_list()[1:-1])
  plt.ylim([40,200])
  plt.suptitle("Variance of team performances", y=0.98, fontsize=18) 
  plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/actual/variance_all.pdf', bbox_inches='tight', dpi=300)
  plt.close()
  #---------------------
  # Put plot in texfile.
  #---------------------
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  texfile.write('\\includegraphics[width=0.9\\textwidth]{./figures/actual/variance_all.pdf}\n')
  texfile.write('\\caption{Variance of team performances over the duration of the season. Dashed black line indicates the league average score.}\n')
  texfile.write('\\end{figure}')
  texfile.close()

  print("Finished plotting team score variance.\n")

  return
#----------------------------------------------------------------------
# Function to analyze and plot projected scores based on teams' 
# starting lineup.
# ----------
# Arguments:
# ----------
# a_LeagueData    (object)  pandas dataframe object for league data
#                           given by .xls sheets
# a_TeamOwnerList (list)    list of team owner names
# args            (object)  command line arguments
#----------------------------------------------------------------------
def projectedScoreAnalysis(a_LeagueData, a_TeamOwnerList, args):
  #----------------------------------
  # Plot all the league data at once.
  #
  # This is commented out because
  # it's a little overwhelming.
  #----------------------------------
#  print("Plotting league data for weekly projected scores...") 
#  plt.figure() 
#  for teamID in range(0, len(a_TeamOwnerList)):
#    plt.plot(np.linspace(1, 14, 14), a_LeagueData.loc[leagueData["Sheet"] == "Projected", a_TeamOwnerList[teamID]].to_numpy(), '-', label=a_TeamOwnerList[teamID])
#  plt.xticks(np.linspace(1,14,14)) 
#  plt.legend(bbox_to_anchor=(1.02, 1.02), loc='upper left',\
#               handlelength=1, fontsize=14,\
#               edgecolor='k', framealpha=1.0)
#  plt.xlim([1,14])
#  plt.ylim([40,120])
#  plt.grid(axis='y')
#  plt.ylabel("Projected score", fontsize=14)
#  plt.xlabel("Week", fontsize=14)
#  plt.suptitle('Projected weekly scoring data', y=0.98, fontsize=18)
#  plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/projected/weekly_all.pdf', bbox_inches='tight', dpi=300)
#  plt.close()
#  print("Finished plotting league data for weekly projected scores.\n")
  #--------------------------
  # Individual plot per team.
  #--------------------------
  print("Plotting team data for weekly projected scores...")
  #----------------
  # Create texfile.
  #----------------
  texfile = open(LEAGUE + '/' + args.year + '/score_projected.tex', 'w')
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  #------------
  # Make plots.
  #------------
  for teamID in range(0, len(a_TeamOwnerList)):
    plt.figure() 
    plt.plot(np.linspace(1, 14, 14), a_LeagueData.loc[leagueData["Sheet"] == "Projected", a_TeamOwnerList[teamID]].to_numpy(), 'k.-', label="Projected")
    plt.plot(np.linspace(1, 14, 14), a_LeagueData.loc[leagueData["Sheet"] == "Actual", a_TeamOwnerList[teamID]].to_numpy(), 'r.-', label="Actual")
    plt.legend(bbox_to_anchor=(0.867, 0.084), loc='center',\
               handlelength=1, fontsize=14,\
               edgecolor='k', framealpha=1.0)
    plt.xticks(np.linspace(1,14,14)) 
    plt.xlim([1,14])
    plt.ylim([40,200])
    plt.grid(axis='y')
    plt.ylabel("Score", fontsize=14)
    plt.xlabel("Week", fontsize=14)
    plt.suptitle('Projected vs. actual weekly scoring data for ' + a_TeamOwnerList[teamID], y=0.98, fontsize=18)
    plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/projected/weekly_' + a_TeamOwnerList[teamID] + '.pdf', bbox_inches='tight', dpi=300)
    plt.close()
    #---------------------
    # Put plot in texfile.
    #---------------------
    texfile.write('\\subfigure{\includegraphics[width=0.3\\textwidth]{./figures/projected/weekly_' + a_TeamOwnerList[teamID] + '.pdf}}')
    if (teamID + 1) % 3 == 0 and 0 < teamID < len(a_TeamOwnerList):
      texfile.write('\\\\')
    texfile.write('\n')
  
  texfile.write('\\caption{Projected team scoring week-by-week. Black lines indicate the Sleeper projection generated pre-kickoffs, and red lines indicate the actual score.}\n')
  texfile.write('\\label{fig:Projected_Weekly_Team}\n')
  texfile.write('\\end{figure}\n\n')
    
  print("Finished plotting team data for weekly projected scores.\n")
  #---------------------------------------------------
  # Compute the mean and variance for projected scores.
  #---------------------------------------------------
  mean_team  = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Projected", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  std_team   = np.std(a_LeagueData.loc[a_LeagueData["Sheet"] == "Projected", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  mean_total = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Projected", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy())
  #-------------------------
  # Make box plots per week.
  #-------------------------
  print("Plotting projected team score variance...")
  plt.figure()
  plt.boxplot(a_LeagueData.loc[a_LeagueData["Sheet"] == "Projected", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), showmeans=True)
  plt.plot(np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)), mean_total*np.ones(len(a_TeamOwnerList)), 'k--', label='League mean')
  plt.ylabel("Projected score",fontsize=16)
  plt.xlabel("Team",fontsize=16)
  plt.xticks(ticks=np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)),labels=a_LeagueData.columns.to_list()[1:-1])
  plt.ylim([60,120])
  plt.suptitle("Variance of projected team performances", y=0.98, fontsize=18) 
  plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/projected/variance_all.pdf', bbox_inches='tight', dpi=300)
  plt.close()
  #---------------------
  # Put plot in texfile.
  #---------------------
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  texfile.write('\\includegraphics[width=0.9\\textwidth]{./figures/projected/variance_all.pdf}\n')
  texfile.write('\\caption{Variance of \textit{projected} team performances over the duration of the season. Dashed black line indicates the league average projected score.}\n')
  texfile.write('\\end{figure}\n\n')

  print("Finished plotting projected team score variance.\n")
  #--------------------------------------------------------
  # Compute the mean and variance for scores differentials.
  #--------------------------------------------------------
  mean_team  = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy() - a_LeagueData.loc[a_LeagueData["Sheet"] == "Projected", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0) 
  std_team   = np.std(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy() - a_LeagueData.loc[a_LeagueData["Sheet"] == "Projected", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  mean_total = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy() - a_LeagueData.loc[a_LeagueData["Sheet"] == "Projected", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy())
  #-------------------------
  # Make box plots per week.
  #-------------------------
  print("Plotting team projected vs. actual variance...")
  plt.figure()
  plt.boxplot(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy() - a_LeagueData.loc[a_LeagueData["Sheet"] == "Projected", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), showmeans=True)
  plt.plot(np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)), mean_total*np.ones(len(a_TeamOwnerList)), 'k--', label='League mean')
  plt.ylabel("Point differential",fontsize=16)
  plt.xlabel("Team",fontsize=16)
  plt.xticks(ticks=np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)),labels=a_LeagueData.columns.to_list()[1:-1])
  plt.ylim([-60,80])
  plt.suptitle("Variance of difference between team actual and projected score", y=0.98, fontsize=18) 
  plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/projected/variance_differential_all.pdf', bbox_inches='tight', dpi=300)
  plt.close()
  #---------------------
  # Put plot in texfile.
  #---------------------
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  texfile.write('\\includegraphics[width=0.9\\textwidth]{./figures/projected/variance_differential_all.pdf}\n')
  texfile.write('\\caption{Variance of \textit{projected} team performances subtracted from \textit{actual} team scores over the duration of the season. Dashed black line indicates the league average differential, which was positive over the season, meaning that on average everyone out-performed the Sleeper projection. A higher number indicates that a team out-performed projection, while a lower number indicates a team under-performed projection.}\n')
  texfile.write('\\end{figure}')
  texfile.close()

  print("Finished plotting efficiency variance.\n")

  return
#----------------------------------------------------------------------
# Function to analyze and plot possible scores based on the performance
# of teams' entire roster, rather than starting lineup.
# ----------
# Arguments:
# ----------
# a_LeagueData    (object)  pandas dataframe object for league data
#                           given by .xls sheets
# a_TeamOwnerList (list)    list of team owner names
# args            (object)  command line arguments
#----------------------------------------------------------------------
def possibleScoreAnalysis(a_LeagueData, a_TeamOwnerList, args):
  #----------------------------------
  # Plot all the league data at once.
  #
  # This is commented out because
  # it's a little overwhelming.
  #----------------------------------
#  print("Plotting league data for weekly possible scores...") 
#  #------------
#  # Make plots.
#  #------------
#  plt.figure() 
#  for teamID in range(0, len(a_TeamOwnerList)):
#    plt.plot(np.linspace(1, 14, 14), a_LeagueData.loc[leagueData["Sheet"] == "Possible", a_TeamOwnerList[teamID]].to_numpy(), '-', label=a_TeamOwnerList[teamID])
#  plt.xticks(np.linspace(1,14,14)) 
#  plt.legend(bbox_to_anchor=(1.02, 1.02), loc='upper left',\
#               handlelength=1, fontsize=14,\
#               edgecolor='k', framealpha=1.0)
#  plt.xlim([1,14])
#  plt.ylim([40,200])
#  plt.grid(axis='y')
#  plt.ylabel("Possible score", fontsize=14)
#  plt.xlabel("Week", fontsize=14)
#  plt.suptitle('Possible weekly scoring data', y=0.98, fontsize=18)
#  plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/possible/weekly_all.pdf', bbox_inches='tight', dpi=300)
#  plt.close()
#  texfile.write('\\begin{figure}[htb!]\n')
#  texfile.write('\\centering\n')
#  print("Finished plotting league data for weekly possible scores.\n")
  #--------------------------
  # Individual plot per team.
  #--------------------------
  print("Plotting team data for weekly possible scores...")
  #----------------
  # Create texfile.
  #----------------
  texfile = open(LEAGUE + '/' + args.year + '/score_possible.tex', 'w')
  #------------
  # Make plots.
  #------------
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  for teamID in range(0, len(a_TeamOwnerList)):
    plt.figure() 
    plt.plot(np.linspace(1, 14, 14), a_LeagueData.loc[leagueData["Sheet"] == "Possible", a_TeamOwnerList[teamID]].to_numpy(), 'k.-', label="Possible")
    plt.plot(np.linspace(1, 14, 14), a_LeagueData.loc[leagueData["Sheet"] == "Actual", a_TeamOwnerList[teamID]].to_numpy(), 'r.-', label="Actual")
    plt.legend(bbox_to_anchor=(0.88, 0.084), loc='center',\
               handlelength=1, fontsize=14,\
               edgecolor='k', framealpha=1.0)
    plt.xticks(np.linspace(1,14,14)) 
    plt.xlim([1,14])
    plt.ylim([40,200])
    plt.grid(axis='y')
    plt.ylabel("Score", fontsize=14)
    plt.xlabel("Week", fontsize=14)
    plt.suptitle('Possible vs. actual weekly scoring data for ' + a_TeamOwnerList[teamID], y=0.98, fontsize=18)
    plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/possible/weekly_' + a_TeamOwnerList[teamID] + '.pdf', bbox_inches='tight', dpi=300)
    plt.close()
    #---------------------
    # Put plot in texfile.
    #---------------------
    texfile.write('\\subfigure{\includegraphics[width=0.3\\textwidth]{./figures/possible/weekly_' + a_TeamOwnerList[teamID] + '.pdf}}')
    if (teamID + 1) % 3 == 0 and 0 < teamID < len(a_TeamOwnerList):
      texfile.write('\\\\')
    texfile.write('\n')
  
  texfile.write('\\caption{Possible team scoring week-by-week. Black lines indicate the score given an optimal starting lineup, and red lines indicate the actual score.}\n')
  texfile.write('\\label{fig:Possible_Weekly_Team}\n')
  texfile.write('\\end{figure}\n\n')

  print("Finished plotting team data for weekly possible scores.\n")
  #---------------------------------------------------
  # Compute the mean and variance for possible scores.
  #---------------------------------------------------
  mean_team  = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Possible", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  std_team   = np.std(a_LeagueData.loc[a_LeagueData["Sheet"] == "Possible", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  mean_total = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Possible", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy())
  #-------------------------
  # Make box plots per week.
  #-------------------------
  print("Plotting possible team score variance...")
  plt.figure()
  plt.boxplot(a_LeagueData.loc[a_LeagueData["Sheet"] == "Possible", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), showmeans=True)
  plt.plot(np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)), mean_total*np.ones(len(a_TeamOwnerList)), 'k--', label='League mean')
  plt.ylabel("Possible score",fontsize=16)
  plt.xlabel("Team",fontsize=16)
  plt.xticks(ticks=np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)),labels=a_LeagueData.columns.to_list()[1:-1])
  plt.ylim([40,200])
  plt.suptitle("Variance of possible team performances", y=0.98, fontsize=18) 
  plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/possible/variance_all.pdf', bbox_inches='tight', dpi=300)
  plt.close()
  #---------------------
  # Put plot in texfile.
  #---------------------
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  texfile.write('\\includegraphics[width=0.9\\textwidth]{./figures/possible/variance_all.pdf}\n')
  texfile.write('\\caption{Variance of \textit{possible} team performances over the duration of the season. Dashed black line indicates the league average possible score.}\n')
  texfile.write('\\end{figure}\n\n')

  print("Finished plotting possible team score variance.\n")
  #----------------------------------------------
  # Compute the mean and variance for effiencies.
  #----------------------------------------------
  mean_team  = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy()/a_LeagueData.loc[a_LeagueData["Sheet"] == "Possible", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)*100 
  std_team   = np.std(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy()/a_LeagueData.loc[a_LeagueData["Sheet"] == "Possible", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)*100
  mean_total = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy()/a_LeagueData.loc[a_LeagueData["Sheet"] == "Possible", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy())*100
  #-------------------------
  # Make box plots per week.
  #-------------------------
  print("Plotting team efficiency variance...")
  plt.figure()
  plt.boxplot(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy()/a_LeagueData.loc[a_LeagueData["Sheet"] == "Possible", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy()*100, showmeans=True)
  plt.plot(np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)), mean_total*np.ones(len(a_TeamOwnerList)), 'k--', label='League mean')
  plt.ylabel("Efficiency",fontsize=16)
  plt.xlabel("Team",fontsize=16)
  plt.xticks(ticks=np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)),labels=a_LeagueData.columns.to_list()[1:-1])
  plt.yticks([50,60,70,80,90,100],['50\%', '60\%', '70\%', '80\%', '90\%', '100\%'])
  plt.ylim([40,110])
  plt.suptitle("Variance of team efficiencies", y=0.98, fontsize=18) 
  plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/possible/variance_efficiency_all.pdf', bbox_inches='tight', dpi=300)
  plt.close()
  #---------------------
  # Put plot in texfile.
  #---------------------
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  texfile.write('\\includegraphics[width=0.9\\textwidth]{./figures/possible/variance_efficiency_all.pdf}\n')
  texfile.write('\\caption{Variance of team owner efficiency over the duration of the season, where $\\text{efficiency } = \\frac{\\text{Actual score}}{\\text{Possible score}}$. Dashed black line indicates the league average efficiency.}\n')
  texfile.write('\\end{figure}')
  texfile.close()

  print("Finished plotting efficiency variance.\n")
  
  return
#----------------------------------------------------------------------
# Function to analyze and plot the point differentials between matchups
# between pairs of teams. 
# ----------
# Arguments:
# ----------
# a_LeagueData    (object)  pandas dataframe object for league data
#                           given by .xls sheets
# a_TeamOwnerList (list)    list of team owner names
# args            (object)  command line arguments
#----------------------------------------------------------------------
def pointDifferentialAnalysis(a_LeagueData, a_TeamOwnerList, args):
  #--------------------------
  # Individual plot per team.
  #--------------------------
  print("Plotting team data for weekly point differentials...")
  #----------------
  # Create texfile.
  #----------------
  texfile = open(LEAGUE + '/' + args.year + '/score_differential.tex', 'w')
  #------------
  # Make plots.
  #------------
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  for teamID in range(0, len(a_TeamOwnerList)):
    plt.figure() 
    plt.plot(np.linspace(1, 14, 14), a_LeagueData.loc[leagueData["Sheet"] == "Matchup Differential", a_TeamOwnerList[teamID]].to_numpy(), 'k.-')
    plt.xticks(np.linspace(1,14,14)) 
    plt.xlim([1,14])
    plt.ylim([-80,100])
    plt.grid(axis='y')
    plt.ylabel("Point differential", fontsize=14)
    plt.xlabel("Week", fontsize=14)
    plt.suptitle('Weekly matchup point differentials for ' + a_TeamOwnerList[teamID], y=0.98, fontsize=18)
    plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/differential/weekly_' + a_TeamOwnerList[teamID] + '.pdf', bbox_inches='tight', dpi=300)
    plt.close()
    #---------------------
    # Put plot in texfile.
    #---------------------
    texfile.write('\\subfigure{\includegraphics[width=0.3\\textwidth]{./figures/differential/weekly_' + a_TeamOwnerList[teamID] + '.pdf}}')
    if (teamID + 1) % 3 == 0 and 0 < teamID < len(a_TeamOwnerList):
      texfile.write('\\\\')
    texfile.write('\n')
  
  texfile.write('\\caption{Point differentials in weekly matchups for each team.}\n')
  texfile.write('\\label{fig:Differential_Weekly_Team}\n')
  texfile.write('\\end{figure}\n\n')
    
  print("Finished plotting team data for weekly point differentials.\n")
  #-------------------------------
  # Compute the mean and variance.
  #-------------------------------
  mean_team  = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Matchup Differential", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  std_team   = np.std(a_LeagueData.loc[a_LeagueData["Sheet"] == "Matchup Differential", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  mean_total = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Matchup Differential", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy())
  #-------------------------
  # Make box plots per week.
  #-------------------------
  print("Plotting team matchup differential variance...")
  plt.figure()
  plt.boxplot(a_LeagueData.loc[a_LeagueData["Sheet"] == "Matchup Differential", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), showmeans=True)
  plt.ylabel("Matchup point differential",fontsize=16)
  plt.xlabel("Team",fontsize=16)
  plt.xticks(ticks=np.linspace(1, len(a_TeamOwnerList), len(a_TeamOwnerList)),labels=a_LeagueData.columns.to_list()[1:-1])
  plt.ylim([-80,80])
  plt.suptitle("Variance of team matchup point differentials", y=0.98, fontsize=18) 
  plt.savefig("/".join(args.inputFile.split('/')[0:-1]) + '/figures/differential/variance_all.pdf', bbox_inches='tight', dpi=300)
  plt.close()
  #---------------------
  # Put plot in texfile.
  #---------------------
  texfile.write('\\begin{figure}[htb!]\n')
  texfile.write('\\centering\n')
  texfile.write('\\includegraphics[width=0.9\\textwidth]{./figures/differential/variance_all.pdf}\n')
  texfile.write('\\caption{Variance of point differentials in weekly matchups over the duration of the season.}\n')
  texfile.write('\\end{figure}')
  texfile.close()

  print("Finished plotting team matchup differential variance.\n")

  return
#----------------------------------------------------------------------
# Function to compute correlations between the following:
# - Total PF and record
# - Weekly PF variance and record
# - Total PF and Weekly PF variance, and record
# ----------
# Arguments:
# ----------
# a_LeagueData    (object)  pandas dataframe object for league data
#                           given by .xls sheets
# a_TeamOwnerList (list)    list of team owner names
# args            (object)  command line arguments
#----------------------------------------------------------------------
def regressionAnalysis(a_LeagueData, a_TeamOwnerList, args):
  #--------------------------------------------
  # Determine each team's total number of wins.
  #--------------------------------------------
  if 'Geed' in a_LeagueData.columns.to_list():
    diff            = a_LeagueData.loc[a_LeagueData['Sheet'] == 'Matchup Differential', a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy()
    diff[diff > 0]  = 1
    diff[diff <= 0] = 0
    record          = np.sum(diff, axis=0)
    record_Median   = np.sum(a_LeagueData.loc[a_LeagueData['Sheet'] == 'Record', a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  else:
    record   = np.sum(a_LeagueData.loc[a_LeagueData['Sheet'] == 'Record', a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  #----------------------------------------
  # Determine total PF actual and possible.
  #----------------------------------------
  totalPF   = np.sum(a_LeagueData.loc[leagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  #-------------------------------------------------------
  # Determine coefficient of variance of every team, i.e.,
  # CoV = deviation of team score / average of team score
  #-------------------------------------------------------
  CV   = np.zeros(len(a_TeamOwnerList))
  mean = np.mean(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  std  = np.std(a_LeagueData.loc[a_LeagueData["Sheet"] == "Actual", a_TeamOwnerList[0]:a_TeamOwnerList[-1]].to_numpy(), axis=0)
  for teamID in range(0, len(a_TeamOwnerList)):
    CV[teamID] = std[teamID]/mean[teamID]
  #---------------------------------------------------------------------------
  # Generate new data frame for statistical analysis for measures of interest.
  #---------------------------------------------------------------------------
  recordDF = pd.DataFrame({'Team' : a_TeamOwnerList, 'Record': record, 'PF': totalPF,  'CV' : CV})
  #-------------------------------------------
  # Perform regression of total PF vs. record.
  #-------------------------------------------
  result_PF = ols(formula='Record ~ PF', data=recordDF).fit()
  #-------------------------------
  # Write janky table to tex file.
  #-------------------------------
  texfile = open(LEAGUE + '/' + args.year + '/regression_RPF.tex','w')
  texfile.write(result_PF.summary().as_latex())
  texfile.close()
  #------------
  # Formatting.
  #------------
  texfile = open(LEAGUE + '/' + args.year + '/regression_RPF.tex', 'r')
  lines = texfile.readlines()
  lines.insert(0, '\\begin{table}[htb!]\n')
  lines[29] = '\\caption{Ordinary least-squares regression analysis of correlation between team record and team total points (PF).}\n'
  lines = lines[0:-4]
  lines.insert(-1, '\\end{table}\n')
  texfile.close()
  texfile = open(LEAGUE + '/' + args.year + '/regression_RPF.tex', 'w')
  texfile.writelines(lines)
  texfile.close()
  #-------------------------------------
  # Perform regression of CV vs. record.
  #-------------------------------------
  result_CV = ols(formula='Record ~ CV', data=recordDF).fit()
  #-------------------------------
  # Write janky table to tex file.
  #-------------------------------
  texfile = open(LEAGUE + '/' + args.year + '/regression_RCV.tex','w')
  texfile.write(result_CV.summary().as_latex())
  texfile.close()
  #------------
  # Formatting.
  #------------
  texfile = open(LEAGUE + '/' + args.year + '/regression_RCV.tex', 'r')
  lines = texfile.readlines()
  lines.insert(0, '\\begin{table}[htb!]\n')
  lines[29] = '\\caption{Ordinary least-squares regression analysis of correlation between team record and team points correlation of variation (CV).}\n'
  lines = lines[0:-2]
  lines.insert(-1, '\\end{table}\n')
  texfile.close()
  texfile = open(LEAGUE + '/' + args.year + '/regression_RCV.tex', 'w')
  texfile.writelines(lines)
  texfile.close()
  #------------------------------------------
  # Perform regression of CV + PF vs. record.
  #------------------------------------------
  result_Correlation = ols(formula='Record ~ PF + CV + PF * CV', data=recordDF).fit()
  #-------------------------------
  # Write janky table to tex file.
  #-------------------------------
  texfile = open(LEAGUE + '/' + args.year + '/regression_RPFCV.tex','w')
  texfile.write(result_Correlation.summary().as_latex())
  texfile.close()
  #------------
  # Formatting.
  #------------
  texfile = open(LEAGUE + '/' + args.year + '/regression_RPFCV.tex', 'r')
  lines = texfile.readlines()
  lines.insert(0, '\\begin{table}[htb!]\n')
  lines[31] = '\\caption{Ordinary least-squares regression analysis of correlation between team record and interaction between team total points (PF) and team correlation of variation of points (CV).}\n'
  lines = lines[0:-4]
  lines.insert(-1, '\\end{table}')
  texfile.close()
  texfile = open(LEAGUE + '/' + args.year + '/regression_RPFCV.tex', 'w')
  texfile.writelines(lines)
  texfile.close()
  #---------------------------------
  # Perform regression of CV vs. PF.
  #---------------------------------
  result_CVPF = ols(formula='PF ~ CV', data=recordDF).fit()
  #-------------------------------
  # Write janky table to tex file.
  #-------------------------------
  texfile = open(LEAGUE + '/' + args.year + '/regression_PFCV.tex','w')
  texfile.write(result_CVPF.summary().as_latex())
  texfile.close()
  #------------
  # Formatting.
  #------------
  texfile = open(LEAGUE + '/' + args.year + '/regression_PFCV.tex', 'r')
  lines = texfile.readlines()
  lines.insert(0, '\\begin{table}[htb!]\n')
  lines[29] = '\\caption{Ordinary least-squares regression analysis of correlation between team total points (CF) and team points correlation of variation (CV).}\n'
  lines = lines[0:-2]
  lines.insert(-1, '\\end{table}\n')
  texfile.close()
  texfile = open(LEAGUE + '/' + args.year + '/regression_PFCV.tex', 'w')
  texfile.writelines(lines)
  texfile.close()
  #----------------------------------------------------------
  # Perform regression of CV + PF vs. record for median wins.
  #----------------------------------------------------------
  if 'Geed' in a_LeagueData.columns.to_list() and args.year == '2023':
    recordMedianDF = pd.DataFrame({'Team' : a_TeamOwnerList, 'Record': record_Median, 'PF': totalPF, 'CV' : CV})
    resultMedian = ols(formula='Record ~ PF + CV + PF * CV', data=recordMedianDF).fit()
    #-------------------------------
    # Write janky table to tex file.
    #-------------------------------
    texfile = open(LEAGUE + '/' + args.year + '/regression_MRPFCV.tex','w')
    texfile.write(resultMedian.summary().as_latex())
    texfile.close()
    #------------
    # Formatting.
    #------------
    texfile = open(LEAGUE + '/' + args.year + '/regression_MRPFCV.tex', 'r')
    lines = texfile.readlines()
    lines.insert(0, '\\begin{table}[htb!]')
    lines[31] = '\\caption{Ordinary least-squares regression analysis of correlation between team record \\textbf{using \\textit{median} wins} and interaction between team points and coefficient of variation of team points.}\n'
    lines = lines[0:-4]
    lines.insert(-1, '\\end{table}')
    texfile.close()
    texfile = open(LEAGUE + '/' + args.year + '/regression_MRPFCV.tex', 'w')
    texfile.writelines(lines)
    texfile.close()

  return

#-------------
# Main script.
#------------- 
if __name__ == '__main__':
  #-----------------
  # Set LaTeX fonts.
  #-----------------
  plt.rc('text', usetex=True)
  plt.rc('font', family='serif')
  #---------------------------
  # Read command line options.
  #---------------------------
  parser = argparse.ArgumentParser(description='This file is used to generate plots related\
                                                to the fantasy football league data for the\
                                                "LEAGUE Squad" league. Report generation is optional.')
  parser.add_argument('inputFile', metavar='i', type=str,
                      help='the file path to the data set file')
  parser.add_argument('year', metavar='y', type=str,
                      help='the season to analyze')
  parser.add_argument('--all', action='store_true',
                      help='flag to make all plots')
  parser.add_argument('--a', action='store_true',
                      help='flag to make plots for actual scores')
  parser.add_argument('--pr', action='store_true',
                      help='flag to make plots for projected scores')
  parser.add_argument('--po', action='store_true',
                      help='flag to make plots for possible scores')
  parser.add_argument('--d', action='store_true',
                      help='flag to make plots for matchup differentials')
  parser.add_argument('--r', action='store_true',
                      help='flag to perform regression analysis of league data')
  parser.add_argument('--print', action='store_true',
                      help='flag to execute print statements')
  parser.add_argument('--build', action='store_true',
                      help='flag to build LaTeX report')
  
  args = parser.parse_args()
  #-----------------------------
  # Check environment variables.
  #-----------------------------
  try:
    LEAGUE = os.environ['LEAGUE']
  except KeyError:
    sys.exit("-------------------\nCOMMAND LINE ERROR:\n-------------------\nSet the LEAUGE environment variable.")
  #-------------------
  # Build directories.
  #-------------------
  if not os.path.exists(LEAGUE + '/' + args.year + '/figures/actual/'):
    os.makedirs(LEAGUE + '/' + args.year + '/figures/actual/')
  if not os.path.exists(LEAGUE + '/' + args.year + '/figures/projected/'):
    os.makedirs(LEAGUE + '/' + args.year + '/figures/projected/')
  if not os.path.exists(LEAGUE + '/' + args.year + '/figures/possible/'):
    os.makedirs(LEAGUE + '/' + args.year + '/figures/possible/')
  if not os.path.exists(LEAGUE + '/' + args.year + '/figures/differential/'):
    os.makedirs(LEAGUE +  args.year + '/figures/differential/')
  #-----------------------
  # Make example box plot.
  #-----------------------
  df = pd.DataFrame({'Column 1': np.random.normal(size=100),
                     'Column 2': np.random.normal(scale=2, size=100)})

  bpdict = df.boxplot(whis=[5, 95], return_type='dict', showmeans=True)
  annotate_boxplot(bpdict, args, x_loc=1)
  #------------------------
  # Read in the .xlsx data.
  #------------------------ 
  leagueData = readData(args)
  #-------------------------
  # Get list of team owners.
  #-------------------------
  teamOwnerList = list(leagueData.columns.values)[1:-1]
  #------------------
  # Scoring analysis.
  #------------------
  if args.all or args.a:
    actualScoreAnalysis(leagueData, teamOwnerList, args)
  #----------------------------
  # Projected scoring analysis.
  #----------------------------
  if args.all or args.pr:
    projectedScoreAnalysis(leagueData, teamOwnerList, args)
  #---------------------------
  # Possible scoring analysis.
  #---------------------------
  if args.all or args.po:
    possibleScoreAnalysis(leagueData, teamOwnerList, args)
  #-----------------------------
  # Point differential analysis.
  #-----------------------------
  if args.all or args.d:
    pointDifferentialAnalysis(leagueData, teamOwnerList, args)
  #---------------------
  # Regression analysis.
  #---------------------
  if args.all or args.r:
    regressionAnalysis(leagueData, teamOwnerList, args)
  #---------------------
  # Build LaTeX report.
  #--------------------
  if args.build:
    print()
    print("Building the report...")
    os.chdir(LEAGUE + '/' + args.year + '/')
    try:
      latex_cmd = ['pdflatex', 'report.tex']
      subprocess.run(latex_cmd, check=True, capture_output=True)
      subprocess.run(latex_cmd, check=True, capture_output=True) # fix refs in .pdf
    except subprocess.CalledProcessError:
      sys.exit("\nERROR. Could not generate report.")
    print("Finished building the report.")

