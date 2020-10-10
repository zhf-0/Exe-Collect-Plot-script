#!/usr/bin/env python3
import numpy as np
from matplotlib import pyplot as plt
import operator
import os

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def plot_grid(f_name,x,output_path,output_name):
    with open(f_name,'r') as f:
        contents = f.readlines()

    # x = np.linspace(0.1,0.9,81)
    length = len(x)
    line_num_opt = length + 2
    num_iter = []
    elapse_time = []

    for i in range(len(x)):
        line_list = contents[i].split(';')
        num_iter.append( eval(line_list[1].split('=')[1]) )
        elapse_time.append( eval(line_list[2].split('=')[1]) )

    y1 = np.array(num_iter,dtype=float)
    y2 = np.array(elapse_time,dtype=float)

    fig_title = contents[line_num_opt].split(';')[0].split('=')[1] 
    if output_path == 0:
        path = os.path.dirname(f_name)
        fig_path = os.path.join(path,output_name+'_grid.png')
    else:
        fig_path = os.path.join(output_path,output_name+'_grid.png')


    opt_index, opt_iter = min(enumerate(num_iter), key=operator.itemgetter(1))
    opt_x = x[opt_index]
    opt_time = elapse_time[opt_index]

    plt.figure()
    plt.title(fig_title)
    plt.xlabel("x")
    plt.ylabel("iterations")
    plt.bar(x,y1,width=0.005, color='blue')
    plt.bar(opt_x,opt_iter,width=0.005,color='red')
    # plt.bar(gp_w,10,width=0.005,color='yellow')
    plt.savefig(fig_path)
    # plt.show()
    plt.close()


def plot_gp(f_name,x,gp_x,gp_y,output_path,output_name):
    with open(f_name,'r') as f:
        contents = f.readlines()

    # x = np.linspace(0.1,0.9,81)
    length = len(x)
    line_num_opt = length + 2
    num_iter = []
    elapse_time = []

    for i in range(len(x)):
        line_list = contents[i].split(';')
        num_iter.append( eval(line_list[1].split('=')[1]) )
        elapse_time.append( eval(line_list[2].split('=')[1]) )

    y1 = np.array(num_iter,dtype=float)
    y2 = np.array(elapse_time,dtype=float)

    fig_title = contents[line_num_opt].split(';')[0].split('=')[1] 
    if output_path == 0:
        path = os.path.dirname(f_name)
        fig_path = os.path.join(path,output_name+'_gp.png')
    else:
        fig_path = os.path.join(output_path,output_name+'_gp.png')


    opt_index, opt_iter = min(enumerate(num_iter), key=operator.itemgetter(1))
    opt_x = x[opt_index]
    opt_time = elapse_time[opt_index]

    plt.figure()
    plt.title(fig_title)
    plt.xlabel("x")
    plt.ylabel("iterations")
    plt.bar(x,y1,width=0.005, color='blue')
    plt.bar(opt_x,opt_iter,width=0.005,color='red')
    plt.bar(gp_x,gp_y,width=0.005,color='yellow')
    plt.savefig(fig_path)
    # plt.show()
    plt.close()

def threshold_grid():
    # AMG_strong_threshold 
    f_name = ['./1/threshold_grid.txt','./2/threshold_grid.txt','./3/threshold_grid.txt','./4/threshold_grid.txt','./5/threshold_grid.txt','./6/threshold_grid.txt','./7/threshold_grid.txt','./8/threshold_grid.txt','./9/threshold_grid.txt','./10/threshold_grid.txt','./11/threshold_grid.txt','./12/threshold_grid.txt','./13/threshold_grid.txt','./14/threshold_grid.txt','./15/threshold_grid.txt','./16/threshold_grid.txt']
    threshold = np.linspace(0.1,0.9,81)
    name = 'threshold'
    for i in range(len(f_name)):
        plot_grid(f_name[i],threshold,'./pic/',str(i+1)+name)

def relax_grid():
    # jacobi relax
    f_name = ['./1/relax_grid.txt','./2/relax_grid.txt','./3/relax_grid.txt','./4/relax_grid.txt','./5/relax_grid.txt','./6/relax_grid.txt','./7/relax_grid.txt','./8/relax_grid.txt','./9/relax_grid.txt','./10/relax_grid.txt','./11/relax_grid.txt','./12/relax_grid.txt','./13/relax_grid.txt','./14/relax_grid.txt','./15/relax_grid.txt','./16/relax_grid.txt']
    relax = np.linspace(0.5,0.98,49)
    name = 'relax'
    for i in range(len(f_name)):
        plot_grid(f_name[i],relax,'./pic/relax/',str(i+1)+name)

def threshold_gp(num,gp_x,gp_y):
    f_name = './{}/threshold_grid.txt'.format(num)
    threshold = np.linspace(0.1,0.9,81)
    name = '{}_threshold'.format(num)
    plot_gp(f_name,threshold,gp_x,gp_y,'./pic/',name)


def relax_gp(num,gp_x,gp_y):
    f_name = './{}/relax_grid.txt'.format(num)
    relax = np.linspace(0.5,0.98,49)
    name = '{}_relax'.format(num)
    plot_gp(f_name,relax,gp_x,gp_y,'./pic/',name)


if __name__ == "__main__":
    threshold_grid()
    relax_grid()
    threshold_gp(5,0.19994636046141404,35)
    threshold_gp(16,0.3798306752101793,4)
    relax_gp(16,0.594366672164779,17)







