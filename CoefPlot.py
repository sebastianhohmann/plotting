import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class CoefPlot(object):
    
    '''
    python wrapper for creating coefficient plots, similar to Stata's coefplot
    http://repec.sowi.unibe.ch/stata/coefplot/
    requires numpy, pandas, matplotlib
    
    Sebastian Hohmann, 2020
    '''
    
    def __init__(self, df):
        self.df = df
        
    def simple_dotplot(self, b, varname, err=None, figsize=(10,6),
                       sort_varname = False, sort_coefval = False,
                       zero_line=False):
        if sort_varname:
            df = self.df.sort_values(varname, inplace=False, ascending=False)
        elif sort_coefval:
            df = self.df.sort_values(b, inplace=False, ascending=True)
        elif sort_varname and sort_coefval:
            print('Error: sort by EITHER variable name OR coefficient value')
            df = self.df
        else:
            df = self.df
        
        f, ax = plt.subplots(1, 1, figsize=figsize)
        if err:
            ax.barh(y = df[varname], width = df[b],   
                    color='none', xerr=df[err])
        ax.scatter(x=df[b], y = df[varname])
        if zero_line:
            ax.axvline(x=0, linestyle='--', color='black', linewidth=1)
        
        plt.show();
        
        
    def grouped_dotplot(self, b, varname, groupname, err=None, figsize=(10,6),
                        sort_groupname = False, zero_line=False):

        if sort_groupname:
            df = self.df.sort_values(groupname, inplace=False, ascending=False)
        else:
            df = self.df
            
        varlist = list(set(df[varname]))
        groups = list(set(df[groupname]))
        offsets = self.make_offset_grid(len(varlist))
        markseq = 'sox^vD+' # can extend this https://matplotlib.org/3.1.1/api/markers_api.html
        colseq = 'bgrcmyk' # can extend this https://matplotlib.org/3.1.0/api/colors_api.html
        
        f, ax = plt.subplots(1, 1, figsize=figsize)
        
        for ivar, var in enumerate(varlist):

            X = np.arange(0, len(groups)*2, 2) + offsets[ivar]
            mod_df = df[df[varname] == var]
            if err:
                ax.barh(y = X, width = mod_df[b],   
                            color='none', xerr=mod_df[err])
            ax.scatter(x=mod_df[b], y = X,
                       marker=markseq[ivar], 
                       color=colseq[ivar], label=var)
            
        ax.set_yticks(np.arange(0, len(groups)*2, 2))
        ax.set_yticklabels(mod_df[groupname], rotation=0)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(reversed(handles), reversed(labels))
       
        
    def make_offset_grid(self, npoints):
        grid = np.arange(0.25, 0.25*(npoints//2 + 1), 0.25)
        if npoints % 2 == 0:
            grid = np.concatenate([grid, -grid])
            return(sorted(grid))
        else:
            grid = np.concatenate([grid, [0], -grid])
            return(sorted(grid))     