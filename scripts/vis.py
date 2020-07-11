from IPython.display import IFrame
import json
import uuid

def vis_network(nodes, edges, physics=False):
    html = """
    <html>
    <head>
      <script type="text/javascript" src="../lib/vis/dist/vis.js"></script>
      <link href="../lib/vis/dist/vis.css" rel="stylesheet" type="text/css">
    </head>
    <body>

    <div id="{id}"></div>

    <script type="text/javascript">
      var nodes = {nodes};
      var edges = {edges};

      var container = document.getElementById("{id}");

      var data = {{
        nodes: nodes,
        edges: edges
      }};

      var options = {{
          nodes: {{
            shape: 'dot',
            scaling: {{
                min:20,
                max:40
            }},            
            fontSize: 15,
            fontFace: "Tahoma",
            borderWidth: 0.5
          }},
          edges: {{
              font: {{
                  size: 10,
                  align: 'middle'
              }},
              color: 'grey',
              arrows: {{
                  to: {{enabled: true, scaleFactor: 0.5}}
              }},
              "smooth": {{
                  "type": "continuous",
                  "roundness": 0.35,
                  "hideEdgesOnDrag": true
              }}             
          }},
          physics: {{
              enabled: {physics}
          }}
      }};

      var network = new vis.Network(container, data, options);

    </script>
    </body>
    </html>
    """

    unique_id = str(uuid.uuid4())
    html = html.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))

    filename = "figure/graph-{}.html".format(unique_id)

    file = open(filename, "w")
    file.write(html)
    file.close()

    return IFrame(filename, width="100%", height="400")

def draw(graph, options, physics=False, limit=100, query="Mining"):
    # The options argument should be a dictionary of node labels and property keys; it determines which property
    # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    # Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    # Setting physics = True makes the nodes bounce around when you touch them!
    query = """
    MATCH (a)-[r]->(m)
    WITH  a, r, m , rand() AS random
    ORDER BY random
    RETURN a AS source_node,
           id(a) AS source_id,
           r,
           m AS target_node,
           id(m) AS target_id
    LIMIT {limit}
    """

    data = graph.run(query, limit=limit)

    nodes = []
    edges = []

    def get_vis_info(node, id):
        node_label = list(node.labels())[0]
        prop_key = options.get(node_label)
        value_label = node.properties.get("value", "")
        vis_label = node.properties.get(prop_key, "")
        
        if value_label == "":
            return {"id": id, "label": vis_label, "group": node_label, "title": repr(node.properties)}
        else:
            return {"id": id, "label": vis_label, "group": node_label, "value": value_label, "title": repr(node.properties)}

    for row in data:
        source_node = row[0]
        source_id = row[1]
        rel = row[2]
        target_node = row[3]
        target_id = row[4]

        source_info = get_vis_info(source_node, source_id)

        if source_info not in nodes:
            nodes.append(source_info)

        if rel is not None:
            target_info = get_vis_info(target_node, target_id)

            if target_info not in nodes:
                nodes.append(target_info)
            
            edge_wt = rel.properties.get("value", "")
            if edge_wt == "":
                edges.append({"from": source_info["id"], "to": target_info["id"], "label": rel.type()})
            else:
                edges.append({"from": source_info["id"], "to": target_info["id"], "label": rel.type(), "value": edge_wt})

    return vis_network(nodes, edges, physics=physics)
