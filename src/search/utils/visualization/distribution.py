
__all__ = ['hex_distribution']


import matplotlib.pyplot as plt
import seaborn as sns


def hex_distribution(input_string):
    """Plots the distribution of binary input in hex style.

    Args:
        input_string: string of binary info in form val1:val2, comma
            separated
    """
    processed_input = [x.split(':') for x in input_string.split(',')[:-1]]
    print(processed_input)
    x = [int(pair[0]) for pair in processed_input]
    y = [int(pair[1]) for pair in processed_input]
    with sns.axes_style('white'):
        sns.jointplot(x=x, y=y, kind='hex', color='k')
        plt.show()
