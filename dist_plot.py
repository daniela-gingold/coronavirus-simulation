import matplotlib.pyplot as plt
import numpy as  np
import warnings
warnings.filterwarnings("ignore")
import pandas as pd


def dist_plot(figure, progress, n, data):
    # need change these static numbers (total time steps and total people)
    len_progress = len(progress[0])
    t_total = 50

    # list_immuned = progress[0][max(0,len_progress-t_total):]
    # list_healthy = progress[1][max(0,len_progress-t_total):]
    # list_unhealthy = progress[2][max(0,len_progress-t_total):]
    # list_sick =  progress[3][max(0,len_progress-t_total):]
    # list_dead = progress[4][max(0,len_progress-t_total):]
    list_immuned = progress[0]
    list_healthy = progress[1]
    list_unhealthy = progress[2]
    list_sick =  progress[3]
    list_dead = progress[4]

    count_immuned = list_immuned[-1]
    count_healthy = list_healthy[-1]
    count_unhealthy = list_unhealthy[-1]
    count_sick = list_sick[-1]
    count_dead = list_dead[-1]

    # print(count_sick, count_immuned, count_healthy, count_dead, count_unhealthy)

    t = np.linspace(1, len_progress, len_progress)
    fig = plt.figure(figsize=(7, 5.5))
    plt.style.use("dark_background")

    if figure == 'lines':
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
        ax.plot(t, list_sick, 'r', linewidth=5, label='Sick')
        ax.plot(t, list_healthy, 'lime', linewidth=5, label='Healthy')
        ax.plot(t, list_immuned, 'b', linewidth=5, label='Recovered')
        ax.plot(t, list_dead, 'grey', linewidth=5, label='Deceased')
        ax.plot(t, list_unhealthy, 'yellow', linewidth=5, label='Infected')
        ax.set_xlabel('time / update')

    if figure == 'pie':
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')

        labels = ['Sick', 'Healthy', 'Recovered', 'Deceased', 'Infected']
        colors = ['r', 'lime', 'b', 'grey', 'yellow']
        counter = [count_sick, count_healthy, count_immuned, count_dead, count_unhealthy]

        # do not plot if the value is 0%
        for i in range(len(counter)-1, -1, -1):
            if counter[i] == 0:
                labels.pop(i)
                counter.pop(i)
                colors.pop(i)

        ax.pie(counter, labels=labels, colors=colors, autopct='%1.2f%%')

    if figure == 'fill_lines':
        fig = plt.figure(figsize=(7, 5.5))
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
        ax.fill_between(t, np.zeros(len_progress), list_sick, color='r', linewidth=5, alpha=0.5, label='Sick')
        ax.fill_between(t, np.zeros(len_progress), list_healthy, color='lime', linewidth=5, alpha=0.5, label='Healthy')
        ax.fill_between(t, np.zeros(len_progress), list_immuned, color='b', linewidth=5, alpha=0.5, label='Recovered')
        ax.fill_between(t, np.zeros(len_progress), list_dead, color='grey', linewidth=5, alpha=0.7, label='Deceased')
        ax.fill_between(t, np.zeros(len_progress), list_unhealthy, color='yellow', linewidth=5, alpha=0.5, label='Infected')

        # ax.set_xlim([0, t_total])
        ax.set_xlim([max(0, len_progress - t_total), max(t_total, len_progress)])
        ax.set_ylim([0, n])
        ax.set_xlabel('time / update')

    if figure == 'stackplot':
        fig = plt.figure(figsize=(7,5.5))
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
        # labels = ['Sick','Healthy', 'Recovered', 'Deceased', 'Infected']
        # colors = ['r', 'lime', 'b','grey', 'yellow']
        # ax.stackplot(t, list_sick, list_healthy, list_immuned, list_dead, list_unhealthy, labels = labels, colors=colors)
        labels = ['Sick', 'Infected', 'Healthy', 'Recovered', 'Deceased']
        colors = ['r',  'yellow', 'lime', 'b','grey']
        ax.stackplot(t, list_sick, list_unhealthy, list_healthy, list_immuned, list_dead,  labels = labels, colors=colors)
        # ax.set_xlim([0, t_total])
        ax.set_xlim([max(0, len_progress-t_total), max(t_total, len_progress)])
        ax.set_ylim([0, n/2])
        ax.set_xlabel('time / update')

    if figure =='glow_lines':
        # df = pd.read_csv('out.csv')
        df = data.iloc[:, 1:]
        fig, ax = plt.subplots()
        plt.suptitle('Day: {}'.format(len_progress))
        colors = ['b', 'lime', 'yellow', 'r', 'grey']
        df.plot(marker='o', color=colors, ax=ax, legend=False)

        n_shades = 10
        diff_linewidth = 1.05
        alpha_value = 0.3 / n_shades
        for n in range(1, n_shades + 1):
            df.plot(marker='o',
                    linewidth=2 + (diff_linewidth * n),
                    alpha=alpha_value,
                    legend=False,
                    ax=ax,
                    color=colors)

        for column, color in zip(df, colors):
            ax.fill_between(x=df.index,
                            y1=df[column].values,
                            y2=[0] * len(df),
                            color=color,
                            alpha=0.1)

            # ax.fill_between(x=t, y1=list_sick, y2=[0] * len_progress, color='r', alpha=0.1)
            # ax.fill_between(x=t, y1=list_healthy, y2=[0] * len_progress, color='lime', alpha=0.1)
            # ax.fill_between(x=t, y1=list_immuned, y2=[0] * len_progress, color='b', alpha=0.1)
            # ax.fill_between(x=t, y1=list_dead, y2=[0] * len_progress, color='grey', alpha=0.1)
            # ax.fill_between(x=t, y1=list_unhealthy, y2=[0] * len_progress, color='yellow', alpha=0.1)


        ax.set_xlim([max(0, len_progress-t_total), max(t_total, len_progress)])
        ax.set_ylim([0, n])
        ax.set_xlabel('day')



    # ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    ax.grid(color='#2A3459')
    legend = ax.legend(loc='upper left')
    # legend.set_alpha(0.8)
    plt.savefig("fig.png")
    plt.close('all')

def dist_all_plots(progress, n):
    # need change these static numbers (total time steps and total people)
    len_progress = len(progress[0])
    t_total = 30

    list_immuned = progress[0]
    list_healthy = progress[1]
    list_unhealthy = progress[2]
    list_sick =  progress[3]
    list_dead = progress[4]

    count_immuned = list_immuned[-1]
    count_healthy = list_healthy[-1]
    count_unhealthy = list_unhealthy[-1]
    count_sick = list_sick[-1]
    count_dead = list_dead[-1]

    # print(count_sick, count_immuned, count_healthy, count_dead, count_unhealthy)

    t = np.linspace(1, len_progress, len_progress)
    fig, axs = plt.subplots(2,2, figsize=(8,8))
    plt.suptitle('Day: {}'.format(len_progress))
    plt.style.use("dark_background")

    # LINES
    ############################
    axs[0,0].plot(t, list_sick, 'r', linewidth=5, label='Sick')
    axs[0,0].plot(t, list_healthy, 'lime', linewidth=5, label='Healthy')
    axs[0,0].plot(t, list_immuned, 'b', linewidth=5, label='Recovered')
    axs[0,0].plot(t, list_dead, 'grey', linewidth=5, label='Deceased')
    axs[0,0].plot(t, list_unhealthy, 'yellow', linewidth=5, label='Infected')
    axs[0,0].set_xlim([max(0, len_progress - t_total), max(t_total, len_progress)])
    axs[0,0].set_ylim([0, n])
    axs[0,0].set_xlabel('day')

    # PIE
    #############################
    axs[0,1].axis([0, 0, 1, 1])
    axs[0,1].axis('equal')
    labels = ['Sick', 'Healthy', 'Recovered', 'Deceased', 'Infected']
    colors = ['r', 'lime', 'b', 'grey', 'yellow']
    counter = [count_sick, count_healthy, count_immuned, count_dead, count_unhealthy]
    # do not plot if the value is 0%
    for i in range(len(counter)-1, -1, -1):
        if counter[i] == 0:
            labels.pop(i)
            counter.pop(i)
            colors.pop(i)
    axs[0,1].pie(counter, labels=labels, colors=colors, autopct='%1.2f%%')

    # FILL LINES
    #############################
    axs[1,0].fill_between(t, np.zeros(len_progress), list_sick, color='r', linewidth=5, alpha=0.5, label='Sick')
    axs[1,0].fill_between(t, np.zeros(len_progress), list_healthy, color='lime', linewidth=5, alpha=0.5, label='Healthy')
    axs[1,0].fill_between(t, np.zeros(len_progress), list_immuned, color='b', linewidth=5, alpha=0.5, label='Recovered')
    axs[1,0].fill_between(t, np.zeros(len_progress), list_dead, color='grey', linewidth=5, alpha=0.7, label='Deceased')
    axs[1,0].fill_between(t, np.zeros(len_progress), list_unhealthy, color='yellow', linewidth=5, alpha=0.5, label='Infected')

    axs[1,0].set_xlim([max(0, len_progress - t_total), max(t_total, len_progress)])
    axs[1,0].set_ylim([0, n])
    axs[1,0].set_xlabel('day')

    # STACKPLOT
    #############################
    labels = ['Sick', 'Healthy', 'Recovered', 'Deceased','Infected']
    colors = ['r', 'lime', 'b','grey',  'yellow']
    axs[1,1].stackplot(t, list_sick, list_healthy, list_immuned, list_dead, list_unhealthy, labels = labels, colors=colors)
    axs[1,1].set_xlim([max(0, len_progress-t_total), max(t_total, len_progress)])
    axs[1,1].set_ylim([0, n])
    axs[1,1].set_xlabel('day')


    # define grid
    axs[0,0].grid(b=True, which='major', c='w', lw=1, ls='-')
    axs[0,1].grid(b=True, which='major', c='w', lw=1, ls='-')
    axs[1,0].grid(b=True, which='major', c='w', lw=1, ls='-')
    axs[1,1].grid(b=True, which='major', c='w', lw=1, ls='-')


    plt.figlegend(axs[1,1], labels = labels, loc = 'upper right')
    plt.savefig("fig.png")
    plt.close('all')


##################################################












# if __name__ == "__main__":
#     # plot the distributions
#     # dist_plot('lines')
#     # dist_plot('pie')
#     # dist_plot('fill_lines')
#     # dist_plot('stackplot')



