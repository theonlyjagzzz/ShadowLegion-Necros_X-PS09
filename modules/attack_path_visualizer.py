"""
NECROS X - Attack Path Visualizer Module
Generates interactive vis.js network graphs of attack paths.
Preserved from original + enhanced with clickable node callbacks and API intelligence popups.
"""
try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False
    Network = None  # type: ignore

import tempfile
import json


SEVERITY_COLORS = {
    "Critical": {"background": "#ff4b4b", "border": "#cc0000"},
    "High":     {"background": "#ff9f43", "border": "#e68a00"},
    "Medium":   {"background": "#f9ca24", "border": "#d4a800"},
    "Low":      {"background": "#6ab04c", "border": "#4a8034"},
}

HONEYPOT_APIS = [
    "legacy_transfer_api",
    "old_payment_gateway",
    "internal_audit_api",
    "debug_api",
    "test_admin_api",
]


def generate_attack_path_graph(attack_logs):
    if not PYVIS_AVAILABLE:
        return "<html><body style='background:#060b18;color:#e2e8f0;font-family:monospace;padding:40px;'><h2>⚠ pyvis not installed</h2><p>Run: <code>pip install pyvis</code></p></body></html>"
    net = Network(
        height="780px",
        width="100%",
        bgcolor="#060b18",
        font_color="white",
        directed=True,
    )

    net.barnes_hut(
        gravity=-4200,
        central_gravity=0.12,
        spring_length=280,
        spring_strength=0.03,
        damping=0.18,
    )

    # Build unique API nodes with aggregated metadata
    api_meta = {}
    for attack in attack_logs:
        api = attack["api_target"]
        sev = attack.get("severity", "Low")
        if api not in api_meta:
            api_meta[api] = {"severity": sev, "count": 1, "attacks": [attack]}
        else:
            api_meta[api]["count"] += 1
            api_meta[api]["attacks"].append(attack)
            # Escalate severity
            order = ["Low", "Medium", "High", "Critical"]
            if order.index(sev) > order.index(api_meta[api]["severity"]):
                api_meta[api]["severity"] = sev

    # Add nodes
    for api, meta in api_meta.items():
        sev = meta["severity"]
        colors = SEVERITY_COLORS.get(sev, SEVERITY_COLORS["Low"])
        is_honeypot = api in HONEYPOT_APIS
        honeypot_label = " 🍯" if is_honeypot else ""
        border_width = 4 if is_honeypot else 2

        title_html = f"""
        <div style='font-family:monospace;padding:8px;background:#131a2b;border-radius:8px;'>
          <b style='color:{colors["background"]};font-size:14px;'>{api}{honeypot_label}</b><br/>
          <hr style='border-color:rgba(255,255,255,0.1);margin:4px 0'/>
          <span style='color:#9aa4bf;'>Severity:</span> <b style='color:{colors["background"]};'>{sev}</b><br/>
          <span style='color:#9aa4bf;'>Attack Count:</span> <b style='color:white;'>{meta["count"]}</b><br/>
          <span style='color:#9aa4bf;'>Latest Attack:</span> <b style='color:white;'>{meta["attacks"][-1].get("attack_type","?")}</b><br/>
          <span style='color:#9aa4bf;'>Source IP:</span> <b style='color:white;'>{meta["attacks"][-1].get("source_ip","?")}</b><br/>
          {'<span style="color:#f9ca24;">⚠ HONEYPOT ACTIVE</span>' if is_honeypot else ''}
        </div>
        """

        net.add_node(
            api,
            label=f"{api}{honeypot_label}",
            title=title_html,
            shape="box",
            color={
                "background": colors["background"],
                "border": colors["border"],
                "highlight": {"background": colors["background"], "border": "#ffffff"},
            },
            borderWidth=border_width,
            borderWidthSelected=4,
            font={"size": 14, "face": "monospace", "color": "#0d0d0d"},
            margin=14,
            shadow={"enabled": True, "color": "rgba(0,0,0,0.5)", "size": 8, "x": 2, "y": 2},
        )

    # Build edges from sequential attack path
    previous_api = None
    for attack in attack_logs:
        api = attack["api_target"]
        if previous_api and previous_api != api:
            net.add_edge(
                previous_api,
                api,
                color={
                    "color": "rgba(255,75,75,0.4)",
                    "highlight": "rgba(255,75,75,0.9)",
                    "hover": "rgba(255,75,75,0.7)",
                },
                width=2,
                arrows={"to": {"enabled": True, "scaleFactor": 1.2}},
                smooth={"enabled": True, "type": "curvedCW", "roundness": 0.2},
            )
        previous_api = api

    net.set_options("""
    var options = {
      "nodes": {
        "shape": "box",
        "borderWidth": 2,
        "font": { "size": 14, "face": "monospace", "color": "#0d0d0d" }
      },
      "edges": {
        "smooth": { "enabled": true, "type": "curvedCW", "roundness": 0.2 },
        "color": { "inherit": false }
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -4200,
          "centralGravity": 0.12,
          "springLength": 280,
          "springConstant": 0.03,
          "damping": 0.18
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "navigationButtons": true,
        "selectConnectedEdges": true
      }
    }
    """)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(temp_file.name)

    with open(temp_file.name, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Inject click callback for Streamlit communication
    click_script = """
    <script>
    network.on("click", function(params) {
      if (params.nodes.length > 0) {
        var nodeId = params.nodes[0];
        // Post message to parent Streamlit frame
        window.parent.postMessage({type: "necros_node_click", api: nodeId}, "*");
      }
    });
    </script>
    """
    html_content = html_content.replace("</body>", click_script + "</body>")
    return html_content
