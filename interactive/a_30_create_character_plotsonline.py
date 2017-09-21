#!/users/anil/anaconda3/bin/python

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
        node_gender = [1 if node['gender'] == 'male' else 0 for node in file_data['nodes']]
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
    
        malenodes_x=[positions[i][0] for i in range(num_nodes) if node_gender[i]==1]
        malenodes_y=[positions[i][1] for i in range(num_nodes) if node_gender[i]==1]
        malenodes_z=[positions[i][2] for i in range(num_nodes) if node_gender[i]==1]
        malenodes_size=[node_size[i] for i in range(num_nodes) if node_gender[i]==1]
        malenode_labels=[node_labels[i] for i in range(num_nodes) if node_gender[i]==1]
        femalenodes_x=[positions[i][0] for i in range(num_nodes) if node_gender[i]==0]
        femalenodes_y=[positions[i][1] for i in range(num_nodes) if node_gender[i]==0]
        femalenodes_z=[positions[i][2] for i in range(num_nodes) if node_gender[i]==0]
        femalenodes_size=[node_size[i] for i in range(num_nodes) if node_gender[i]==0]
        femalenode_labels=[node_labels[i] for i in range(num_nodes) if node_gender[i]==0]
    
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
        
        trace2=Scatter3d(x=malenodes_x,y=malenodes_y,z=malenodes_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=malenodes_size,color='blue',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=malenode_labels,
            hoverinfo='text',
            name='Male characters'
        )
    
        trace3=Scatter3d(x=femalenodes_x,y=femalenodes_y,z=femalenodes_z,
            mode='markers',
            marker=Marker(symbol='dot',opacity=1,size=femalenodes_size,color='green',line=Line(color='rgb(50,50,50)', width=0.5)),
            text=femalenode_labels,
            hoverinfo='text',
            name='Female characters'
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
    
            trace4=Scatter3d(x=passed_node_x,y=passed_node_y,z=passed_node_z,
                mode='markers',
                marker=Marker(symbol='dot',opacity=1,size=passed_node_sizes,color='red',line=Line(color='rgb(50,50,50)', width=0.5)),
                text=passed_node_labels,
                hoverinfo='text',
                name='Female chars that pass test'
            )
    
            trace5=Scatter3d(x=passed_edge_x,y=passed_edge_y,z=passed_edge_z,
                mode='lines',
                line=Line(color='red', width=3.25),
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
            width=1000,
            height=1000,
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
            data=Data([trace1, trace2, trace3, trace4, trace5])
        else: 
            data=Data([trace1, trace2, trace3])
    
        fig=Figure(data=data, layout=layout)
        
        current_url=py.plot(fig, filename=file.replace('.json', ''), auto_open=False)
    
        print("%s: %s" % (file, current_url))

    except Exception:
        continue
