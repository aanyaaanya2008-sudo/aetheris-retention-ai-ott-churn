import os
import json
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Load production artifacts from deploy_artifacts folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "deploy_artifacts")

preprocessor = joblib.load(os.path.join(ARTIFACTS_DIR, "preprocessor.joblib"))
model = joblib.load(os.path.join(ARTIFACTS_DIR, "model.joblib"))

with open(os.path.join(ARTIFACTS_DIR, "config.json"), "r") as f:
    config = json.load(f)

LOCKED_THRESHOLD = float(config["optimal_threshold"])
CHAMPION_NAME = str(config.get("champion_model", "XGBoost"))

print(f"✓ Production Assets Loaded: Model={CHAMPION_NAME} | Threshold={LOCKED_THRESHOLD:.4f}")

# Luxury Parchment & Oxblood Dashboard Template
HTML_TEMPLATE = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RETENTION-AI // SVOD Retention Intelligence Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800;900&family=JetBrains+Mono:wght@400;600&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        obsidian: '#0A0807',
                        obsidianCard: '#120F0D',
                        obsidianBorder: '#231E1A',
                        parchment: '#F5EBE1',
                        parchmentMuted: '#C4B5A5',
                        oxblood: '#7A0C18',
                        oxbloodBright: '#9E1524',
                        brass: '#C5A059'
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #070605;
            color: #F5EBE1;
            background-image: 
                radial-gradient(circle at 15% 20%, rgba(122, 12, 24, 0.18) 0%, transparent 45%),
                radial-gradient(circle at 85% 80%, rgba(197, 160, 89, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(10, 8, 7, 0.95) 0%, #050403 100%);
            background-attachment: fixed;
            font-family: 'Plus Jakarta Sans', sans-serif;
            min-height: 100vh;
        }
        .parchment-border { border: 1px solid rgba(197, 160, 89, 0.22); }
        input[type=range] { accent-color: #C5A059; }
    </style>
</head>
<body class="p-6">
    <div class="max-w-7xl mx-auto space-y-6">
        
        <!-- Header -->
        <header class="p-4 rounded-xl bg-obsidianCard parchment-border flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded bg-gradient-to-br from-oxblood to-black border border-brass/40 flex items-center justify-center font-['Cinzel'] text-brass font-bold text-xl">
                    Æ
                </div>
                <div>
                    <h1 class="text-xl font-bold font-['Cinzel'] tracking-wider text-brass">RETENTION-AI // SVOD COMMAND CENTER</h1>
                    <p class="text-xs font-mono text-parchmentMuted">SERVING MODEL: {{ model_name }} • OPTIMAL THRESHOLD: τ* = {{ "%.4f"|format(threshold) }}</p>
                </div>
            </div>
            <div class="flex items-center gap-2 px-3 py-1 bg-emerald-950/60 border border-emerald-500 rounded text-emerald-300 font-mono text-xs font-bold">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <span>REAL BACKEND CONNECTED</span>
            </div>
        </header>

        <!-- Presets Bar -->
        <div class="p-3.5 rounded-lg bg-obsidianCard parchment-border flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
            <span class="text-brass font-bold font-['Cinzel'] tracking-wider">EXECUTIVE PRESETS:</span>
            <div class="flex flex-wrap gap-2">
                <button onclick="setPreset(12, 4.0, 0.25, 6, 2, 2, 'Basic_Ad_Supported', 0)" class="px-3 py-1 bg-black border border-oxblood/40 hover:border-brass text-parchmentMuted rounded transition">🔴 7-Day Inactivity Ghosting</button>
                <button onclick="setPreset(8, 7.5, 0.40, 5, 4, 3, 'Standard_HD', 0)" class="px-3 py-1 bg-black border border-oxblood/40 hover:border-brass text-parchmentMuted rounded transition">⚠️ QoS Buffer + Support Friction</button>
                <button onclick="setPreset(1, 24.0, 0.85, 1, 0, 0, 'Premium_4K', 1)" class="px-3 py-1 bg-black border border-emerald-700/40 hover:border-emerald-400 text-parchmentMuted rounded transition">🟢 Loyal Premium User</button>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Controls (Left 5 cols) -->
            <div class="lg:col-span-5 p-6 rounded-xl bg-obsidianCard parchment-border space-y-4 text-xs font-mono">
                <h2 class="text-sm font-bold text-parchment pb-2 border-b border-obsidianBorder font-['Cinzel'] tracking-wider">Subscriber Telemetry HUD</h2>
                
                <div>
                    <label class="block text-parchmentMuted mb-1">SUBSCRIPTION PLAN</label>
                    <select id="plan_type" onchange="runInference()" class="w-full p-2.5 rounded bg-black border border-obsidianBorder text-parchment focus:border-brass outline-none">
                        <option value="Basic_Ad_Supported">Basic Ad Supported ($6.99)</option>
                        <option value="Standard_HD">Standard HD ($12.99)</option>
                        <option value="Premium_4K">Premium 4K ($19.99)</option>
                        <option value="Family_Annual">Family Annual ($24.99)</option>
                    </select>
                </div>

                <div>
                    <label class="block text-parchmentMuted mb-1">BILLING RENEWAL MECHANISM</label>
                    <select id="auto_renew" onchange="runInference()" class="w-full p-2.5 rounded bg-black border border-obsidianBorder text-parchment focus:border-brass outline-none">
                        <option value="0">Manual Renewal (High Friction)</option>
                        <option value="1">Auto-Renew (Active Automation)</option>
                    </select>
                </div>

                <div class="p-3 bg-black/60 rounded-lg border border-oxblood/40">
                    <div class="flex justify-between mb-1">
                        <span class="text-oxbloodBright font-bold">INACTIVITY RECENCY (DAYS)</span>
                        <span id="txt_inactivity" class="text-oxbloodBright font-bold">9 Days</span>
                    </div>
                    <input type="range" id="days_since_last_stream" min="0" max="30" value="9" oninput="runInference()" class="w-full">
                    <div class="flex justify-between text-[10px] text-parchmentMuted mt-1">
                        <span>Active Today</span>
                        <span class="text-brass">7-Day Habit Cliff</span>
                        <span>Dormant (30d)</span>
                    </div>
                </div>

                <div>
                    <div class="flex justify-between mb-1">
                        <span>WEEKLY WATCH TIME</span>
                        <span id="txt_watch" class="text-brass font-bold">6.0 hrs / wk</span>
                    </div>
                    <input type="range" id="weekly_watch_hours" min="0" max="45" value="6.0" step="0.5" oninput="runInference()" class="w-full">
                </div>

                <div>
                    <div class="flex justify-between mb-1">
                        <span>COMPLETION RATE</span>
                        <span id="txt_comp" class="text-brass font-bold">35%</span>
                    </div>
                    <input type="range" id="avg_completion_rate" min="0.05" max="1.0" value="0.35" step="0.05" oninput="runInference()" class="w-full">
                </div>

                <div>
                    <div class="flex justify-between mb-1">
                        <span>SUPPORT TICKETS RAISED</span>
                        <span id="txt_tickets" class="text-oxbloodBright font-bold">2 Tickets</span>
                    </div>
                    <input type="range" id="support_tickets_raised" min="0" max="6" value="2" oninput="runInference()" class="w-full">
                </div>

                <div>
                    <div class="flex justify-between mb-1">
                        <span>BUFFER EVENTS / MONTH</span>
                        <span id="txt_buffers" class="text-parchment font-bold">2 Freezes</span>
                    </div>
                    <input type="range" id="buffer_events_monthly" min="0" max="8" value="2" oninput="runInference()" class="w-full">
                </div>

                <div>
                    <div class="flex justify-between mb-1">
                        <span>SKIPS PER SESSION</span>
                        <span id="txt_skips" class="text-parchment font-bold">5 Skips</span>
                    </div>
                    <input type="range" id="skips_per_session" min="0" max="15" value="5" oninput="runInference()" class="w-full">
                </div>
            </div>

            <!-- Output Display (Right 7 cols) -->
            <div class="lg:col-span-7 space-y-6">
                
                <!-- Probability Dial & Status -->
                <div class="p-6 rounded-xl bg-obsidianCard parchment-border flex flex-col sm:flex-row items-center justify-between gap-6">
                    <div class="relative w-40 h-40 flex items-center justify-center">
                        <svg class="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
                            <circle cx="60" cy="60" r="50" stroke="#1A1512" stroke-width="10" fill="transparent"/>
                            <circle id="gauge_circle" cx="60" cy="60" r="50" stroke="url(#oxbloodGrad)" stroke-width="10" stroke-linecap="round" fill="transparent" stroke-dasharray="314.159" stroke-dashoffset="65" class="transition-all duration-500"/>
                            <defs>
                                <linearGradient id="oxbloodGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#C5A059" />
                                    <stop offset="60%" stop-color="#9E1524" />
                                    <stop offset="100%" stop-color="#7A0C18" />
                                </linearGradient>
                            </defs>
                        </svg>
                        <div class="absolute inset-0 flex flex-col items-center justify-center">
                            <span id="prob_val" class="font-['Cinzel'] font-bold text-3xl text-parchment">--%</span>
                            <span class="text-[10px] font-mono text-parchmentMuted tracking-widest uppercase">CHURN RISK</span>
                        </div>
                    </div>

                    <div class="flex-1 space-y-2">
                        <div class="flex justify-between items-center">
                            <span class="text-xs font-mono text-parchmentMuted">RISK CLASSIFICATION:</span>
                            <span id="status_pill" class="text-xs font-mono font-bold px-3 py-1 rounded bg-oxblood text-parchment border border-brass/40 tracking-wider">CALCULATING</span>
                        </div>
                        <div class="p-3 bg-black/70 rounded border border-obsidianBorder text-xs font-mono">
                            <span class="text-brass block mb-1">OPTIMAL DECISION STATUS (τ* = {{ "%.2f"|format(threshold) }}):</span>
                            <p id="decision_text" class="text-parchmentMuted leading-relaxed">Connecting to inference pipeline...</p>
                        </div>
                    </div>
                </div>

                <!-- Prescriptive Playbook -->
                <div class="p-6 rounded-xl bg-obsidianCard parchment-border space-y-3">
                    <h3 class="text-xs font-bold font-mono text-brass uppercase border-b border-obsidianBorder pb-2 font-['Cinzel'] tracking-wider">Prescriptive Marketing Playbook</h3>
                    <div id="playbook_box" class="space-y-2 text-xs font-mono">
                    </div>
                </div>

            </div>

        </div>
    </div>

    <script>
        const priceMap = {
            "Basic_Ad_Supported": 6.99,
            "Standard_HD": 12.99,
            "Premium_4K": 19.99,
            "Family_Annual": 24.99
        };

        function setPreset(inact, watch, comp, skips, buffers, tickets, plan, renew) {
            document.getElementById('days_since_last_stream').value = inact;
            document.getElementById('weekly_watch_hours').value = watch;
            document.getElementById('avg_completion_rate').value = comp;
            document.getElementById('skips_per_session').value = skips;
            document.getElementById('buffer_events_monthly').value = buffers;
            document.getElementById('support_tickets_raised').value = tickets;
            document.getElementById('plan_type').value = plan;
            document.getElementById('auto_renew').value = renew;
            runInference();
        }

        async function runInference() {
            const plan = document.getElementById('plan_type').value;
            const inact = parseFloat(document.getElementById('days_since_last_stream').value);
            const watch = parseFloat(document.getElementById('weekly_watch_hours').value);
            const comp = parseFloat(document.getElementById('avg_completion_rate').value);
            const tickets = parseInt(document.getElementById('support_tickets_raised').value);
            const buffers = parseInt(document.getElementById('buffer_events_monthly').value);
            const skips = parseInt(document.getElementById('skips_per_session').value);
            const autorenew = parseInt(document.getElementById('auto_renew').value);

            document.getElementById('txt_inactivity').innerText = `${inact} Days`;
            document.getElementById('txt_watch').innerText = `${watch.toFixed(1)} hrs / wk`;
            document.getElementById('txt_comp').innerText = `${Math.round(comp*100)}%`;
            document.getElementById('txt_tickets').innerText = `${tickets} Tickets`;
            document.getElementById('txt_buffers').innerText = `${buffers} Freezes`;
            document.getElementById('txt_skips').innerText = `${skips} Skips`;

            const payload = {
                age: 32,
                gender: "Male",
                plan_type: plan,
                primary_device: "Smart TV",
                auto_renew: autorenew,
                monthly_fee_usd: priceMap[plan],
                tenure_months: 6,
                weekly_watch_hours: watch,
                avg_completion_rate: comp,
                skips_per_session: skips,
                days_since_last_stream: inact,
                buffer_events_monthly: buffers,
                support_tickets_raised: tickets
            };

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                const prob = result.churn_probability;
                const probPct = (prob * 100).toFixed(1);
                const threshPct = (result.locked_threshold * 100).toFixed(1);

                document.getElementById('prob_val').innerText = `${probPct}%`;

                // Update gauge circle
                const circle = document.getElementById('gauge_circle');
                circle.style.strokeDashoffset = 314.159 * (1.0 - prob);

                if (result.is_churn) {
                    document.getElementById('status_pill').innerText = "🚨 HIGH CHURN RISK";
                    document.getElementById('status_pill').className = "text-xs font-mono font-bold px-3 py-1 rounded bg-oxblood text-parchment border border-brass/40 tracking-wider";
                    document.getElementById('decision_text').innerHTML = `<span class="text-oxbloodBright font-bold">EXCEEDS OPTIMAL CUTOFF (${probPct}% ≥ ${threshPct}%).</span> Action required: Preserved LTV exceeds campaign concession cost ($5.00).`;

                    let playHTML = '';
                    if (inact > 7) {
                        playHTML += '<div class="p-2.5 bg-black border border-oxblood rounded text-oxbloodBright">📲 <b>Stage 3 Re-engagement:</b> Send automated Day-5 weekend trailer push.</div>';
                    }
                    if (tickets >= 2) {
                        playHTML += '<div class="p-2.5 bg-black border border-brass rounded text-brass">🎟️ <b>Stage 2 Service Concierge:</b> Issue proactive $5.00 bill credit & route to Senior Care.</div>';
                    }
                    if (autorenew === 0) {
                        playHTML += '<div class="p-2.5 bg-black border border-amber-600 rounded text-amber-400">💳 <b>Stage 4 Billing Friction:</b> Offer 15% discount for switching to Auto-Renew.</div>';
                    }
                    document.getElementById('playbook_box').innerHTML = playHTML || '<div class="p-2.5 bg-black rounded text-parchmentMuted">Multi-variable friction detected. Send personalized genre email.</div>';
                } else {
                    document.getElementById('status_pill').innerText = "🟢 HEALTHY SUBSCRIBER";
                    document.getElementById('status_pill').className = "text-xs font-mono font-bold px-3 py-1 rounded bg-emerald-900 text-emerald-300 border border-emerald-500 tracking-wider";
                    document.getElementById('decision_text').innerHTML = `<span class="text-emerald-400 font-bold">BELOW THRESHOLD (${probPct}% < ${threshPct}%).</span> Subscriber habit loop is stable. No promotional spend required.`;
                    document.getElementById('playbook_box').innerHTML = '<div class="p-3 bg-black border border-emerald-950 rounded text-emerald-400">✓ Healthy engagement equilibrium. Standard content recommendation engine active.</div>';
                }

            } catch (err) {
                console.error("Backend fetch error:", err);
            }
        }

        window.onload = runInference;
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, threshold=LOCKED_THRESHOLD, model_name=CHAMPION_NAME)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model": CHAMPION_NAME,
        "locked_threshold": LOCKED_THRESHOLD
    })

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json(force=True)
    row = pd.DataFrame([data])

    # Reconstruct exact RFLH feature interactions
    row['R_inactivity_tenure_ratio'] = row['days_since_last_stream'] / ((row['tenure_months'] * 30.4) + 1.0)
    row['F_watch_hours_per_dollar'] = (row['weekly_watch_hours'] * 4.33) / (row['monthly_fee_usd'] + 0.01)
    row['L_tenure_months'] = row['tenure_months']
    row['H_completion_to_skip_ratio'] = row['avg_completion_rate'] / (row['skips_per_session'] + 1.0)
    row['support_intensity'] = row['support_tickets_raised'] / (row['tenure_months'] + 0.1)
    row['friction_index'] = (row['buffer_events_monthly'] * 1.5) + row['skips_per_session']
    row['habit_decay_velocity'] = row['days_since_last_stream'] / (row['weekly_watch_hours'] + 0.5)
    row['friction_per_dollar'] = row['friction_index'] / (row['monthly_fee_usd'] + 0.01)
    row['service_saturation'] = row['support_tickets_raised'] * row['buffer_events_monthly']
    row['low_engagement_flag'] = ((row['weekly_watch_hours'] < 6.0) & (row['days_since_last_stream'] > 7)).astype(int)

    X_mat = preprocessor.transform(row)
    prob = float(model.predict_proba(X_mat)[0, 1])

    return jsonify({
        "churn_probability": prob,
        "locked_threshold": LOCKED_THRESHOLD,
        "is_churn": bool(prob >= LOCKED_THRESHOLD),
        "model_used": CHAMPION_NAME
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)