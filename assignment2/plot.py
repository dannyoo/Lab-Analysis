# %%
from matplotlib import pyplot as plt
from process_data import *
from import_cells import *


# %%
#Function to average LD ratios to plot all wells as one point
def Average(lst):
    return sum(lst) / len(lst)

# %%
# creates 3 columns dead_count, alive_count, & ld_ratio = dead_count / alive count 
ld_c1 = continuous1.ld_ratio()
ld_c2 = continuous2.ld_ratio()
ld_b3 = blast3.ld_ratio()

#Groups columns of live/death ratio by dilution
ld_c1["dilution_no"] = ld_c1["dilution"].map(dilution_map)
ld_c2["dilution_no"] = ld_c2["dilution"].map(dilution_map)
ld_b3["dilution_no"] = ld_b3["dilution"].map(dilution_map)


# %%
#This is setting each live/dead ratio of a cell type based
#on dilution column to a more managable variable
highest_w3 = ld_w3[ld_w3.dilution_no == 1.0].ld_ratio
seventh_w3 = ld_w3[ld_w3.dilution_no == 2.0].ld_ratio
sixth_w3 = ld_w3[ld_w3.dilution_no == 3.0].ld_ratio
fifth_w3 = ld_w3[ld_w3.dilution_no == 4.0].ld_ratio
fourth_w3 = ld_w3[ld_w3.dilution_no == 5.0].ld_ratio
third_w3 = ld_w3[ld_w3.dilution_no == 6.0].ld_ratio
second_w3 = ld_w3[ld_w3.dilution_no == 7.0].ld_ratio
lowest_w3 = ld_w3[ld_w3.dilution_no == 8.0].ld_ratio

# %%
#Storing average of the list (live/dead ratio of cell type
# based on dilution) in a new variable
highest_w3_avg = Average(highest_w3)
seventh_w3_avg = Average(seventh_w3)
sixth_w3_avg = Average(sixth_w3)
fifth_w3_avg = Average(fifth_w3)
fourth_w3_avg = Average(fourth_w3)
third_w3_avg = Average(third_w3)
second_w3_avg = Average(second_w3)
lowest_w3_avg = Average(lowest_w3)

# %%
#Sets y axis to highest dilution - lowest dilution ld ratio
#and x axis to dilutions
ld_w3_y = [highest_w3_avg, seventh_w3_avg, sixth_w3_avg, fifth_w3_avg, fourth_w3_avg, third_w3_avg, second_w3_avg, lowest_w3_avg]
print('The LD ratios are ', ld_w3_y)
dilution_x = [0.22, 0.044, 0.0088, 0.00176, 0.000352, 0.0000704, 0.0000141, 0.00000282]

# %%
#Plot the graph
plt.plot(dilution_x, ld_w3_y)

plt.title('LD50 Curve for Wildtype')
plt.xlabel('Dilution (mg/mL)')
plt.ylabel('Cell Death (%)')
plt.tight_layout()
plt.show()


# %%
'''The error is that the list is nil like it's not accessing the data somewhere?
I left a few print statements in to see if when changes are made the data shows up.'''
#CONTINUOUS 1
#This is setting each live/dead ratio of a cell type based
#on dilution column to a more managable variable
highest_c1 = ld_c1[ld_c1.dilution_no == 1.0].ld_ratio
seventh_c1 = ld_c1[ld_c1.dilution_no == 2.0].ld_ratio
sixth_c1 = ld_c1[ld_c1.dilution_no == 3.0].ld_ratio
fifth_c1 = ld_c1[ld_c1.dilution_no == 4.0].ld_ratio
fourth_c1 = ld_c1[ld_c1.dilution_no == 5.0].ld_ratio
third_c1 = ld_c1[ld_c1.dilution_no == 6.0].ld_ratio
second_c1 = ld_c1[ld_c1.dilution_no == 7.0].ld_ratio
lowest_c1 = ld_c1[ld_c1.dilution_no == 8.0].ld_ratio
print(highest_c1)

# %%
#Storing average of the lists in a new variable
highest_c1_avg = Average(highest_c1)
seventh_c1_avg = Average(seventh_c1)
sixth_c1_avg = Average(sixth_c1)
fifth_c1_avg = Average(fifth_c1)
fourth_c1_avg = Average(fourth_c1)
third_c1_avg = Average(third_c1)
second_c1_avg = Average(second_c1)
lowest_c1_avg = Average(lowest_c1)

# %%
#Sets y axis to highest dilution - lowest dilution ld ratio
#and x axis to dilutions
ld_c1_y = [highest_c1_avg, seventh_c1_avg, sixth_c1_avg, fifth_c1_avg, fourth_c1_avg, third_c1_avg, second_c1_avg, lowest_c1_avg]
print(ld_c1_y)

# %%
#Plot the graph
plt.plot(dilution_x, ld_c1_y)

plt.title('LD50 Curve for Continuous 1')
plt.xlabel('Dilution (mg/mL)')
plt.ylabel('Cell Death (%)')
plt.tight_layout()
plt.show()


# %%
#CONTINUOUS 2
#This is setting each live/dead ratio of a cell type based
#on dilution column to a more managable variable
highest_c2 = ld_c2[ld_c2.dilution_no == 1.0].ld_ratio
seventh_c2 = ld_c2[ld_c2.dilution_no == 2.0].ld_ratio
sixth_c2 = ld_c2[ld_c2.dilution_no == 3.0].ld_ratio
fifth_c2 = ld_c2[ld_c2.dilution_no == 4.0].ld_ratio
fourth_c2 = ld_c2[ld_c2.dilution_no == 5.0].ld_ratio
third_c2 = ld_c2[ld_c2.dilution_no == 6.0].ld_ratio
second_c2 = ld_c2[ld_c2.dilution_no == 7.0].ld_ratio
#ERRORing lowest_c2 = ld_c2[ld_c2.dilution_no == 8.0].ld_ratio
print(highest_c2)

# %%
#Storing average of the lists in a new variable
highest_c2_avg = Average(highest_c2)
seventh_c2_avg = Average(seventh_c2)
sixth_c2_avg = Average(sixth_c2)
fifth_c2_avg = Average(fifth_c2)
fourth_c2_avg = Average(fourth_c2)
third_c2_avg = Average(third_c2)
second_c2_avg = Average(second_c2)
#ERRORing lowest_c2_avg = Average(lowest_c2)

# %%
#Sets y axis to highest dilution - lowest dilution ld ratio
#and x axis to dilutions
ld_c2_y = [highest_c2_avg, seventh_c2_avg, sixth_c2_avg, fifth_c2_avg, 
fourth_c2_avg, third_c2_avg, second_c2_avg]
#ERRORing lowest_c2_avg so took out of plot
print(ld_c2_y)

# %%
#Plot the graph
dilution_x_nolow = [0.22, 0.044, 0.0088, 0.00176, 0.000352, 0.0000704, 0.0000141]
plt.plot(dilution_x_nolow, ld_c2_y)

plt.title('LD50 Curve for Continuous 2')
plt.xlabel('Dilution (mg/mL)')
plt.ylabel('Cell Death (%)')
plt.tight_layout()
plt.show()


# %%
#BLAST3
#This is setting each live/dead ratio of a cell type based
#on dilution column to a more managable variable
highest_b3 = ld_b3[ld_b3.dilution_no == 1.0].ld_ratio
seventh_b3 = ld_b3[ld_b3.dilution_no == 2.0].ld_ratio
sixth_b3 = ld_b3[ld_b3.dilution_no == 3.0].ld_ratio
fifth_b3 = ld_b3[ld_b3.dilution_no == 4.0].ld_ratio
fourth_b3 = ld_b3[ld_b3.dilution_no == 5.0].ld_ratio
third_b3 = ld_b3[ld_b3.dilution_no == 6.0].ld_ratio
second_b3 = ld_b3[ld_b3.dilution_no == 7.0].ld_ratio
lowest_b3 = ld_b3[ld_b3.dilution_no == 8.0].ld_ratio

# %%
#Storing average of the lists in a new variable
highest_b3_avg = Average(highest_b3)
seventh_b3_avg = Average(seventh_b3)
sixth_b3_avg = Average(sixth_b3)
fifth_b3_avg = Average(fifth_b3)
fourth_b3_avg = Average(fourth_b3)
third_b3_avg = Average(third_b3)
second_b3_avg = Average(second_b3)
lowest_b3_avg = Average(lowest_b3)

# %%
#Sets y axis to highest dilution - lowest dilution ld ratio
#and x axis to dilutions
ld_b3_y = [highest_b3_avg, seventh_b3_avg, sixth_b3_avg, 
fifth_b3_avg, fourth_b3_avg, third_b3_avg, second_b3_avg, lowest_b3_avg]
print('The LD ratios are ', ld_b3_y)

# %%
#Plot the graph
plt.plot(dilution_x, ld_b3_y)

plt.title('LD50 Curve for Blast 3')
plt.xlabel('Dilution (mg/mL)')
plt.ylabel('Cell Death (%)')
plt.tight_layout()
plt.show()


'''May need to zoom in on the bottom left corner'''