from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import re


def usage():
    print(f'{sys.argv[0]} [options] probplot INPUT [kwargs]')
    # TODO: Add options
    print('''
    x=str               Name of statistic series (default: first column
    linecolor=str       Color for the linear regression (default: Orange
    figsize=tuple       Figure size (default: 4,4)
    xlabel=str          Label for the x axis (default 'Theoretical Quantiles')
    ylabel=str          Label for the y axis (default 'Sample Quantiles')
    scale=float         Rescale the statistic series by this amount (default 0)
    filetype=str        Output file type (default svg)''')


def plot(df, kwargs):
    sns.set_context('notebook')
    sns.set_style('darkgrid', {'axes.facecolor': '#ebebeb'})

    param = {
        'x': df.columns[0],
        'linecolor': 'Orange',
        'figsize': '4,4',
        'xlabel': 'Theoretical Quantiles',
        'ylabel': 'Sample Quantiles',
        'scale': 1,
        'filename': None,
        'filetype': 'svg'
    }

    # Parse kwargs
    for arg in kwargs:
        key, value = arg.split('=')
        param[key] = value

    # Augment parameters
    param['figsize'] = tuple(
        map(float, param['figsize'].strip('{[()]}').split(',')))
    param['scale'] = float(param['scale'])

    # Scale data
    df[param['x']] = df[param['x']] * param['scale']

    # Compute probplot
    arr, stat = stats.probplot(df[param['x']], rvalue=True)

    osm, osr = arr
    slope, intercept, r = stat

    print(f'r: {r}')

    plt.figure(figsize=param['figsize'])

    ax = sns.scatterplot(x=osm,
                         y=osr,
                         alpha=0.7,
                         linewidth=0,
                         s=20)

    ax.axline((0, intercept), slope=slope, color=param['linecolor'])

    plt.xlabel(param['xlabel'])
    plt.ylabel(param['ylabel'])

    plt.tight_layout()

    if param['filename']:
        filename = param['filename'] + '.' + param['filetype']
    else:
        y = re.sub('/', '-', '+'.join(param['x']))
        filename = f'./plots/{y}_' + f"{param['time']}.{param['filetype']}"

    plt.savefig(filename)

    plt.close()
