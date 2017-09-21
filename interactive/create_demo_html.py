#!/users/anil/anaconda3/bin/python

html_file_string = '''<!DOCTYPE html>
<html>
<body>

<script>
function load_character_plot() {{
    var selected_value = document.getElementById('drop_down_menu').value;

    document.getElementById("graph_div").style.display='block';

    if (selected_value == "annie_hall") {{
        document.getElementById("graph").setAttribute("src", "https://plot.ly/~anilkram/1272.embed?show_link=false");
    }}
{0}
}}
</script>

<div align='center'>
<p id='demo' align='center'>Choose a movie from the list below and click submit to load its character network graph</p>

<select id='drop_down_menu'>
    <option value="annie_hall">Annie Hall</option>
{1}
</select>
<br />
<button onclick='load_character_plot()'>Submit</button>
<br />
</div>
<div id='graph_div' style='display:none;'>
<br />
<iframe id='graph' scrolling='no' style='border:none;' seamless='seamless' src='' height='550' width='100%%'></iframe>
</div>
<div>
<br />
<h3 align="center">Usage</h3>
<ul>
<li>The graph is interactive. Zoom in and rotate the graph to reveal interesting patterns</li>
<li>Each node in the graph represents a character in the movie; hover on it to reveal its name</li>
<li>Size of the node represents number of utterances by that character</li>
<li>Male characters are blue colored, female characters are green colored</li>
<li>The graph title indicates if a movie passes the <u><b>Bechdel test</b></u></li>
<li>Red nodes represent female characters that pass the Bechdel test</li>
</ul>
<br />
<h4>Please share your thoughts/feedback in comments below.</h4>
</div>
</body>
</html>'''

links_file='../Results/demo_html/character_network_plot_links.txt'

js_string=''
select_string=''

with open('../Results/incorrect_predictions.txt') as inPtr:
    incorrect_predictions=[x.strip() for x in inPtr.readlines()]

accurate_predictions = []
with open('../Results/predicted_both.txt') as inPtr:
    _ = inPtr.readline()

    for line in inPtr.readlines():
        line=line.strip()
        cur_movie_name=line.split('\t')[0]

        if cur_movie_name not in incorrect_predictions:
            accurate_predictions.append(cur_movie_name)

first_entry=False
with open(links_file) as inPtr:
    for line in inPtr.readlines():
        line = line.strip()

        tmplist = line.split(': ')
        
        movie_id=tmplist[0][:-5]
        movie_url=tmplist[1]

#        if movie_id not in accurate_predictions:
#            continue

        if first_entry:
            js_string='''
    if (selected_value == "{0}") {{
        document.getElementById("graph").setAttribute("src", "{1}.embed?show_link=false");
    }}
'''.format(movie_id, movie_url)
            first_entry=False
        else:
            js_string=js_string+'''
    else if (selected_value == "{0}") {{
        document.getElementById("graph").setAttribute("src", "{1}.embed?show_link=false");
    }}   
'''.format(movie_id, movie_url)     
          
        select_string=select_string+'''    <option value="{0}">{1}</option>
'''.format(movie_id, ' '.join([x.capitalize() for x in movie_id.split('_')]))

html_file_string = html_file_string.format(js_string, select_string)

print(html_file_string)
