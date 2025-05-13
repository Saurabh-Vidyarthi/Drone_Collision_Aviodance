import plotly.graph_objects as go

TEXT_Z_OFFSET = 0.5
PALETTE = {1: "red", 2: "green", 3: "blue", 4: "orange", 5: "black"}

def create_interactive_figure(positions, velocities, collisions, pause_log, dt):
    """
    positions: dict of drone_id -> [ [x,y,z], ... ]
    velocities: dict of drone_id -> [v, ...]
    collisions: dict of frame_idx -> list of (x,y,z) collision points
    pause_log: list of (sim_time, other_id, frame_idx)
    dt: timestep (s)
    """
    drone_ids = sorted(positions.keys())
    n_frames = len(positions[drone_ids[0]])

    # map each frame to pause annotations
    pause_map = {}
    for sim_t, other_id, frame_idx in pause_log:
        txt = f"[t={sim_t:.2f}s] PAUSE primary due to Drone {other_id}"
        pause_map.setdefault(frame_idx, []).append(txt)

    frames = []
    for i in range(n_frames):
        data = []
        for did in drone_ids:
            xs = [p[0] for p in positions[did][:i+1]]
            ys = [p[1] for p in positions[did][:i+1]]
            zs = [p[2] for p in positions[did][:i+1]]
            v = velocities[did][i]
            color = PALETTE[did]

            # path line
            data.append(go.Scatter3d(
                x=xs, y=ys, z=zs,
                mode="lines", line=dict(color=color),
                showlegend=False
            ))
            #circle marker for drone rep
            data.append(go.Scatter3d(
                x=[xs[-1]], y=[ys[-1]], z=[zs[-1]],
                mode="markers",
                marker=dict(size=4, color=color, symbol="circle"),
                showlegend=False
            ))
            # velocity label
            data.append(go.Scatter3d(
                x=[xs[-1]], y=[ys[-1]], z=[zs[-1] + TEXT_Z_OFFSET],
                mode="text", text=[f"{v:.2f} m/s"], textfont=dict(size=10),
                showlegend=False
            ))

        # frame-specific annotations for pauses
        annots = []
        for idx, txt in enumerate(pause_map.get(i, [])):
            annots.append(dict(
                text=txt,
                xref="paper", yref="paper",
                x=0.01, y=0.98 - 0.05 * idx,
                showarrow=False, font=dict(size=12, color="black")
            ))

        frames.append(go.Frame(data=data, name=str(i), layout=go.Layout(annotations=annots)))

    # static summary of all pauses
    summary_items = []
    for sim_t, other_id, _ in pause_log:
        summary_items.append(f"[t={sim_t:.2f}s] → Drone {other_id}")
    summary_text = "All pauses:<br>" + "<br>".join(summary_items)

    summary_annot = dict(
        text=summary_text,
        xref="paper", yref="paper",
        x=1.02, y=0.5, xanchor="left", yanchor="middle",
        showarrow=False, font=dict(size=12)
    )

    # build figure
    fig = go.Figure(
        data=frames[0].data,
        frames=frames,
        layout=go.Layout(
            annotations=[summary_annot],
            scene=dict(
                xaxis=dict(range=[-10, 15], autorange=False),
                yaxis=dict(range=[-10, 15], autorange=False),
                zaxis=dict(range=[-10, 15], autorange=False),
                aspectmode="cube"
            ),
            updatemenus=[dict(
                type="buttons", showactive=False,
                x=0, y=0, xanchor="left", yanchor="top",
                buttons=[dict(
                    label="▶️", method="animate",
                    args=[None, {"frame": {"duration": dt * 1000, "redraw": True},
                                 "fromcurrent": True}]
                )]
            )],
            sliders=[dict(
                active=0, pad={"t": 50},
                steps=[dict(
                    method="animate",
                    args=[[str(k)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    label=f"{k*dt:.1f}s"
                ) for k in range(n_frames)],
                currentvalue={"prefix": "Time: "}
            )]
        )
    )
    return fig
