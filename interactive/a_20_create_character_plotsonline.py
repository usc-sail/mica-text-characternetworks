#!/usr/bin/env python

import pdb
import os
import igraph as ig
import json
import plotly.plotly as py
from plotly.graph_objs import *

json_files_dir='../Results/character_network_jsonfiles/'

fileslist = os.listdir(json_files_dir)
#fileslist = fileslist[fileslist.index('sleepless_in_seattle.json')+1:]

for file in fileslist:
    if not file.endswith('.json'):
        continue

    try:
        file_data = json.loads(open(json_files_dir+file).read())
    
        num_nodes = len(file_data['nodes'])
        node_labels = [node['name'] for node in file_data['nodes']]
        node_size = [node['count'] if type(node['count'])==int else 0 for node in file_data['nodes']]
        max_count = max(node_size);min_count = min(node_size)
        upper=80;lower=10
        node_size = [(x-min_count)/(max_count-min_count)*(upper-lower)+lower for x in node_size]
        node_gender = [node['gender'] for node in file_data['nodes']]
        node_race = [node['race'] for node in file_data['nodes']]
        bechdel_nodes = [node['sno']-1 for node in file_data['nodes'] if node['bechdel']==1]
    
        if bechdel_nodes != []:
            bechdel_test_passed=True
            bechdel_status_message='; Passes Bechdel test'
        else:
            bechdel_test_passed=False
            bechdel_status_message=''
    
        edges = [(edge['source'], edge['target']) for edge in file_data['edges']]
        edge_strengths = [edge['strength'] for edge in file_data['edges']]
    
        graph = ig.Graph(edges, directed=False)
        positions = graph.layout('kk', dim=3)
   
        male_1_x,male_1_y,male_1_z,male_1_size,male_1_labels=[],[],[],[],[]
        male_2_x,male_2_y,male_2_z,male_2_size,male_2_labels=[],[],[],[],[]
        male_3_x,male_3_y,male_3_z,male_3_size,male_3_labels=[],[],[],[],[]
        male_4_x,male_4_y,male_4_z,male_4_size,male_4_labels=[],[],[],[],[]
        male_5_x,male_5_y,male_5_z,male_5_size,male_5_labels=[],[],[],[],[]
        male_6_x,male_6_y,male_6_z,male_6_size,male_6_labels=[],[],[],[],[]
        male_7_x,male_7_y,male_7_z,male_7_size,male_7_labels=[],[],[],[],[]
        male_8_x,male_8_y,male_8_z,male_8_size,male_8_labels=[],[],[],[],[]
        male_9_x,male_9_y,male_9_z,male_9_size,male_9_labels=[],[],[],[],[]
        female_1_x,female_1_y,female_1_z,female_1_size,female_1_labels=[],[],[],[],[]
        female_2_x,female_2_y,female_2_z,female_2_size,female_2_labels=[],[],[],[],[]
        female_3_x,female_3_y,female_3_z,female_3_size,female_3_labels=[],[],[],[],[]
        female_4_x,female_4_y,female_4_z,female_4_size,female_4_labels=[],[],[],[],[]
        female_5_x,female_5_y,female_5_z,female_5_size,female_5_labels=[],[],[],[],[]
        female_6_x,female_6_y,female_6_z,female_6_size,female_6_labels=[],[],[],[],[]
        female_7_x,female_7_y,female_7_z,female_7_size,female_7_labels=[],[],[],[],[]
        female_8_x,female_8_y,female_8_z,female_8_size,female_8_labels=[],[],[],[],[]
        female_9_x,female_9_y,female_9_z,female_9_size,female_9_labels=[],[],[],[],[]

        for i in range(num_nodes):
            if node_gender[i] == 'male':
                if node_race[i] == 'caucasian':
                    male_1_x.append(positions[i][0])
                    male_1_y.append(positions[i][1])
                    male_1_z.append(positions[i][2])
                    male_1_size.append(node_size[i])
                    male_1_labels.append(node_labels[i])
                elif node_race[i] == 'eastasian':
                    male_2_x.append(positions[i][0])
                    male_2_y.append(positions[i][1])
                    male_2_z.append(positions[i][2])
                    male_2_size.append(node_size[i])
                    male_2_labels.append(node_labels[i])
                elif node_race[i] == 'mixed':
                    male_3_x.append(positions[i][0])
                    male_3_y.append(positions[i][1])
                    male_3_z.append(positions[i][2])
                    male_3_size.append(node_size[i])
                    male_3_labels.append(node_labels[i])
                elif node_race[i] == 'nativeamerican':
                    male_4_x.append(positions[i][0])
                    male_4_y.append(positions[i][1])
                    male_4_z.append(positions[i][2])
                    male_4_size.append(node_size[i])
                    male_4_labels.append(node_labels[i])
                elif node_race[i] == 'african':
                    male_5_x.append(positions[i][0])
                    male_5_y.append(positions[i][1])
                    male_5_z.append(positions[i][2])
                    male_5_size.append(node_size[i])
                    male_5_labels.append(node_labels[i])
                elif node_race[i] == 'asianindian':
                    male_6_x.append(positions[i][0])
                    male_6_y.append(positions[i][1])
                    male_6_z.append(positions[i][2])
                    male_6_size.append(node_size[i])
                    male_6_labels.append(node_labels[i])
                elif node_race[i] == 'latino':
                    male_7_x.append(positions[i][0])
                    male_7_y.append(positions[i][1])
                    male_7_z.append(positions[i][2])
                    male_7_size.append(node_size[i])
                    male_7_labels.append(node_labels[i])
                elif node_race[i] == 'pacificislander':
                    male_8_x.append(positions[i][0])
                    male_8_y.append(positions[i][1])
                    male_8_z.append(positions[i][2])
                    male_8_size.append(node_size[i])
                    male_8_labels.append(node_labels[i])
                else:
                    male_9_x.append(positions[i][0])
                    male_9_y.append(positions[i][1])
                    male_9_z.append(positions[i][2])
                    male_9_size.append(node_size[i])
                    male_9_labels.append(node_labels[i])

            if node_gender[i] == 'female':
                if node_race[i] == 'caucasian':
                    female_1_x.append(positions[i][0])
                    female_1_y.append(positions[i][1])
                    female_1_z.append(positions[i][2])
                    female_1_size.append(node_size[i])
                    female_1_labels.append(node_labels[i])
                elif node_race[i] == 'eastasian':
                    female_2_x.append(positions[i][0])
                    female_2_y.append(positions[i][1])
                    female_2_z.append(positions[i][2])
                    female_2_size.append(node_size[i])
                    female_2_labels.append(node_labels[i])
                elif node_race[i] == 'mixed':
                    female_3_x.append(positions[i][0])
                    female_3_y.append(positions[i][1])
                    female_3_z.append(positions[i][2])
                    female_3_size.append(node_size[i])
                    female_3_labels.append(node_labels[i])
                elif node_race[i] == 'nativeamerican':
                    female_4_x.append(positions[i][0])
                    female_4_y.append(positions[i][1])
                    female_4_z.append(positions[i][2])
                    female_4_size.append(node_size[i])
                    female_4_labels.append(node_labels[i])
                elif node_race[i] == 'african':
                    female_5_x.append(positions[i][0])
                    female_5_y.append(positions[i][1])
                    female_5_z.append(positions[i][2])
                    female_5_size.append(node_size[i])
                    female_5_labels.append(node_labels[i])
                elif node_race[i] == 'asianindian':
                    female_6_x.append(positions[i][0])
                    female_6_y.append(positions[i][1])
                    female_6_z.append(positions[i][2])
                    female_6_size.append(node_size[i])
                    female_6_labels.append(node_labels[i])
                elif node_race[i] == 'latino':
                    female_7_x.append(positions[i][0])
                    female_7_y.append(positions[i][1])
                    female_7_z.append(positions[i][2])
                    female_7_size.append(node_size[i])
                    female_7_labels.append(node_labels[i])
                elif node_race[i] == 'pacificislander':
                    female_8_x.append(positions[i][0])
                    female_8_y.append(positions[i][1])
                    female_8_z.append(positions[i][2])
                    female_8_size.append(node_size[i])
                    female_8_labels.append(node_labels[i])
                else:
                    female_9_x.append(positions[i][0])
                    female_9_y.append(positions[i][1])
                    female_9_z.append(positions[i][2])
                    female_9_size.append(node_size[i])
                    female_9_labels.append(node_labels[i])

        edge_x=[]
        edge_y=[]
        edge_z=[]
        for edge in edges:
            edge_x+=[positions[edge[0]][0],positions[edge[1]][0], None]
            edge_y+=[positions[edge[0]][1],positions[edge[1]][1], None]
            edge_z+=[positions[edge[0]][2],positions[edge[1]][2], None]
    
        #Plot lines
        trace1=Scatter3d(x=edge_x,y=edge_y,z=edge_z,
            mode='lines',
            line=Line(color='rgb(125,125,125)', width=2),
            hoverinfo='none',
            name='Dialogues'
        )
        
        trace2=Scatter3d(x=male_1_x,y=male_1_y,z=male_1_z,
            mode='markers',
            marker=Marker(symbol='square',opacity=1,size=male_1_size,color='rgb(0,0,255)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=male_1_labels,
            hoverinfo='text',
            name='gender: male; race: caucasian'
        )

        trace3=Scatter3d(x=male_2_x,y=male_2_y,z=male_2_z,
            mode='markers',
            marker=Marker(symbol='square',opacity=1,size=male_2_size,color='rgb(0,255,255)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=male_2_labels,
            hoverinfo='text',
            name='gender: male; race: eastasian'
        )

        trace4=Scatter3d(x=male_3_x,y=male_3_y,z=male_3_z,
            mode='markers',
            marker=Marker(symbol='square',opacity=1,size=male_3_size,color='rgb(0,255,0)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=male_3_labels,
            hoverinfo='text',
            name='gender: male; race: mixed'
        )

        trace5=Scatter3d(x=male_4_x,y=male_4_y,z=male_4_z,
            mode='markers',
            marker=Marker(symbol='square',opacity=1,size=male_4_size,color='rgb(0,0,128)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=male_4_labels,
            hoverinfo='text',
            name='gender: male; race: nativeamerican'
        )

        trace6=Scatter3d(x=male_5_x,y=male_5_y,z=male_5_z,
            mode='markers',
            marker=Marker(symbol='square',opacity=1,size=male_5_size,color='rgb(255,0,255)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=male_5_labels,
            hoverinfo='text',
            name='gender: male; race: african'
        )

        trace7=Scatter3d(x=male_6_x,y=male_6_y,z=male_6_z,
            mode='markers',
            marker=Marker(symbol='square',opacity=1,size=male_6_size,color='rgb(255,0,0)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=male_6_labels,
            hoverinfo='text',
            name='gender: male; race: southasian'
        )

        trace8=Scatter3d(x=male_7_x,y=male_7_y,z=male_7_z,
            mode='markers',
            marker=Marker(symbol='square',opacity=1,size=male_7_size,color='rgb(0,128,128)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=male_7_labels,
            hoverinfo='text',
            name='gender: male; race: latino'
        )

        trace9=Scatter3d(x=male_8_x,y=male_8_y,z=male_8_z,
            mode='markers',
            marker=Marker(symbol='square',opacity=1,size=male_8_size,color='rgb(255,215,0)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=male_8_labels,
            hoverinfo='text',
            name='gender: male; race: pacificislander'
        )
 
        trace10=Scatter3d(x=female_1_x,y=female_1_y,z=female_1_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=female_1_size,color='rgb(0,0,255)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=female_1_labels,
            hoverinfo='text',
            name='gender: female; race: caucasian'
        )
    
        trace11=Scatter3d(x=female_2_x,y=female_2_y,z=female_2_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=female_2_size,color='rgb(0,255,255)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=female_2_labels,
            hoverinfo='text',
            name='gender: female; race: eastasian'
        )

        trace12=Scatter3d(x=female_3_x,y=female_3_y,z=female_3_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=female_3_size,color='rgb(0,255,0)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=female_3_labels,
            hoverinfo='text',
            name='gender: female; race: mixed'
        )

        trace13=Scatter3d(x=female_4_x,y=female_4_y,z=female_4_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=female_4_size,color='rgb(0,0,128)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=female_4_labels,
            hoverinfo='text',
            name='gender: female; race: nativeamerican'
        )

        trace14=Scatter3d(x=female_5_x,y=female_5_y,z=female_5_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=female_5_size,color='rgb(255,0,255)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=female_5_labels,
            hoverinfo='text',
            name='gender: female; race: african'
        )

        trace15=Scatter3d(x=female_6_x,y=female_6_y,z=female_6_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=female_6_size,color='rgb(255,0,0)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=female_6_labels,
            hoverinfo='text',
            name='gender: female; race: southasian'
        )

        trace16=Scatter3d(x=female_7_x,y=female_7_y,z=female_7_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=female_7_size,color='rgb(0,128,128)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=female_7_labels,
            hoverinfo='text',
            name='gender: female; race: latino'
        )

        trace17=Scatter3d(x=female_8_x,y=female_8_y,z=female_8_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=female_8_size,color='rgb(255,215,0)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=female_8_labels,
            hoverinfo='text',
            name='gender: female; race: pacificislander'
        )

        trace18=Scatter3d(x=male_9_x,y=male_9_y,z=male_9_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=male_9_size,color='rgb(255,255,255)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=male_9_labels,
            hoverinfo='text',
            name='gender: male; race: unknown'
        )

        trace19=Scatter3d(x=female_9_x,y=female_9_y,z=female_9_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=female_9_size,color='rgb(255,255,255)',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=female_9_labels,
            hoverinfo='text',
            name='gender: female; race: unknown'
        )
        if bechdel_test_passed:
            passed_node_x=[positions[bechdel_nodes[0]][0], positions[bechdel_nodes[1]][0]]
            passed_node_y=[positions[bechdel_nodes[0]][1], positions[bechdel_nodes[1]][1]]
            passed_node_z=[positions[bechdel_nodes[0]][2], positions[bechdel_nodes[1]][2]]
            passed_edge_x=[positions[bechdel_nodes[0]][0], positions[bechdel_nodes[1]][0]]
            passed_edge_y=[positions[bechdel_nodes[0]][1], positions[bechdel_nodes[1]][1]]
            passed_edge_z=[positions[bechdel_nodes[0]][2], positions[bechdel_nodes[1]][2]]
            passed_node_labels=[node_labels[x] for x in bechdel_nodes]
            passed_node_sizes=[node_size[x] for x in bechdel_nodes]
    
            trace20=Scatter3d(x=passed_node_x,y=passed_node_y,z=passed_node_z,
                mode='markers',
                marker=Marker(symbol='dot',opacity=1,size=passed_node_sizes,color='rgb(255,0,0)',line=Line(color='rgb(50,50,50)', width=0.5)),
                text=passed_node_labels,
                hoverinfo='text',
                name='Female chars that pass Bechdel test'
            )
    
            trace21=Scatter3d(x=passed_edge_x,y=passed_edge_y,z=passed_edge_z,
                mode='lines',
                line=Line(color='rgb(255,0,0)', width=3.25),
                hoverinfo='none',
                showlegend=False,
            )
    
        axis=dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
        )
        
        layout = Layout(title=file.replace('.json', '').capitalize()+bechdel_status_message,
            width=900,
            height=900,
            showlegend=True,
            scene=Scene(
                xaxis=XAxis(axis),
                yaxis=YAxis(axis),
                zaxis=ZAxis(axis),
            ),
            margin=Margin(t=100),
            hovermode='none',
    #        hovermode='closest',
        )
       
        if bechdel_test_passed:
            data=Data([trace1, trace2, trace3, trace4, trace5, \
                trace6, trace7, trace8, trace9, trace10, \
                trace11, trace12, trace13, trace14, trace15, \
                trace16, trace17, trace18, trace19, \
                trace20, trace21])
        else: 
            data=Data([trace1, trace2, trace3, trace4, trace5, \
                trace6, trace7, trace8, trace9, trace10, \
                trace11, trace12, trace13, trace14, trace15, \
                trace16, trace17, trace18, trace19])
    
        fig=Figure(data=data, layout=layout)
        
        current_url=py.plot(fig, filename=file.replace('.json', ''), auto_open=False)
    
        print("%s: %s" % (file, current_url))

    except Exception as e:
        pdb.set_trace()
        continue

#    break
