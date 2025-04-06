from agents.extensions.visualization import draw_graph


def vis_agent(agent, visual_name="vis1") -> str:
    filename = f"viz/{visual_name}.gv"
    try:
        draw_graph(agent, filename=filename)
    except Exception as e:
        print(f"An error occurred: {e}")

    return filename
