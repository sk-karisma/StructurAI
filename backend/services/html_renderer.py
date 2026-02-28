from jinja2 import Template
import os
from datetime import datetime

OUTPUT_DIR = "generated_projects"

def generate_html(structure: dict):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{structure['page_name'].replace(' ', '_')}_{timestamp}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)

    template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
    </style>
</head>
<body class="bg-[#F8FAFC] text-slate-900">
    <div class="flex h-screen overflow-hidden">
        <aside class="w-64 bg-white border-r border-slate-200 flex flex-col hidden md:flex">
            <div class="p-6 flex items-center gap-3">
                <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold">D</div>
                <span class="font-bold text-xl tracking-tight">Analytics</span>
            </div>
            <nav class="flex-1 px-4 space-y-1 mt-4">
                <a href="#" class="flex items-center gap-3 p-3 bg-indigo-50 text-indigo-700 rounded-xl font-semibold">
                    <span class="text-lg">📊</span> Overview
                </a>
                <a href="#" class="flex items-center gap-3 p-3 text-slate-500 hover:bg-slate-50 rounded-xl transition">
                    <span class="text-lg">📁</span> Projects
                </a>
                <a href="#" class="flex items-center gap-3 p-3 text-slate-500 hover:bg-slate-50 rounded-xl transition">
                    <span class="text-lg">📈</span> Reports
                </a>
            </nav>
            <div class="p-6 border-t border-slate-100">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-slate-200"></div>
                    <div>
                        <p class="text-sm font-bold">John Doe</p>
                        <p class="text-xs text-slate-400">Pro Account</p>
                    </div>
                </div>
            </div>
        </aside>

        <main class="flex-1 overflow-y-auto custom-scrollbar p-8">
            <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-4">
                <div>
                    <h1 class="text-3xl font-bold tracking-tight text-slate-900">{{ page_name }}</h1>
                    <p class="text-slate-500 mt-1">Review your latest design architecture and components.</p>
                </div>
                <div class="flex gap-3">
                    <div class="bg-white border border-slate-200 px-4 py-2 rounded-xl text-sm font-medium text-slate-600 shadow-sm">
                        Last edited: Just now
                    </div>
                    <button class="bg-indigo-600 text-white px-5 py-2.5 rounded-xl font-bold hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition">
                        + New Action
                    </button>
                </div>
            </header>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                <div class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
                    <p class="text-slate-400 text-xs font-bold uppercase tracking-widest">Efficiency</p>
                    <h3 class="text-2xl font-bold mt-2">94.2%</h3>
                    <p class="text-emerald-500 text-xs font-bold mt-2">↑ 2.4% <span class="text-slate-300 ml-1">vs last week</span></p>
                </div>
                <div class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
                    <p class="text-slate-400 text-xs font-bold uppercase tracking-widest">Active Users</p>
                    <h3 class="text-2xl font-bold mt-2">1,284</h3>
                    <p class="text-indigo-500 text-xs font-bold mt-2">+12 <span class="text-slate-300 ml-1">new today</span></p>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {% for section in sections %}
                    {% if "Sidebar" not in section.name %}
                    <section class="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm hover:shadow-md transition">
                        <div class="flex justify-between items-center mb-6">
                            <h2 class="text-xl font-bold text-slate-800">{{ section.name }}</h2>
                            <span class="text-indigo-600 text-xs font-bold bg-indigo-50 px-3 py-1 rounded-full uppercase">{{ layout_type }}</span>
                        </div>
                        <p class="text-slate-500 mb-8 text-sm leading-relaxed">{{ section.purpose }}</p>

                        <div class="space-y-4">
                            {% for comp in section.components_in_section %}
                                {% if "chart" in comp.type|lower %}
                                    <div class="h-56 bg-slate-50 rounded-2xl border border-slate-100 flex items-end justify-center p-6 gap-2">
                                        {% for i in range(10) %}
                                            <div class="flex-1 bg-indigo-400 opacity-60 rounded-t-lg" style="height: {{ [30, 70, 45, 90, 60, 85, 40, 75]|random }}%"></div>
                                        {% endfor %}
                                    </div>
                                {% elif "button" in comp.type|lower %}
                                    <button class="w-full py-4 bg-slate-900 text-white rounded-2xl font-bold hover:bg-slate-800 transition">
                                        {{ comp.type }}
                                    </button>
                                {% else %}
                                    <div class="p-5 bg-white border border-slate-100 rounded-2xl flex items-center gap-4">
                                        <div class="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-lg">✨</div>
                                        <div>
                                            <p class="font-bold text-sm">{{ comp.type }}</p>
                                            <p class="text-xs text-slate-400">{{ comp.purpose }}</p>
                                        </div>
                                    </div>
                                {% endif %}
                            {% endfor %}
                        </div>
                    </section>
                    {% endif %}
                {% endfor %}
            </div>
        </main>
    </div>
</body>
</html>
""")

    rendered = template.render(
        page_name=structure["page_name"],
        layout_type=structure["layout_type"],
        sections=structure["sections"]
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(rendered)

    return filename