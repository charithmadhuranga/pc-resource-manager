import sys
import os
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, GLib
from monitor_logic import SystemMonitor


def format_bytes(bytes_val: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} PB"


def format_speed(bytes_per_sec: float) -> str:
    return f"{format_bytes(bytes_per_sec)}/s"


class GraphWidget(Gtk.DrawingArea):
    def __init__(self, max_points=60, color="#4a90d9"):
        super().__init__()
        self.max_points = max_points
        self.data = [0] * max_points
        self.color = color
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_draw_func(self._draw)

    def add_value(self, value):
        self.data = self.data[1:] + [value]
        self.queue_draw()

    def _draw(self, area, context, width, height):
        context.set_source_rgba(0.1, 0.1, 0.18, 1)
        context.rectangle(0, 0, width, height)
        context.fill()

        if not self.data:
            return

        max_val = max(max(self.data), 1)

        r, g, b = self._hex_to_rgb(self.color)
        context.set_source_rgba(r, g, b, 0.8)
        context.set_line_width(2)

        for i, val in enumerate(self.data):
            x = (i / (self.max_points - 1)) * width
            y = height - (val / max_val) * (height - 10) - 5

            if i == 0:
                context.move_to(x, y)
            else:
                context.line_to(x, y)

        context.stroke()

        context.set_source_rgba(r, g, b, 0.3)
        context.line_to(width, height)
        context.line_to(0, height)
        context.close_path()
        context.fill()

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        return (r, g, b)


CSS = """
window {
    background: #0f0f1a;
}

.card {
    background: linear-gradient(145deg, #1a1a2e, #16213e);
    border-radius: 16px;
    padding: 16px;
    border: 1px solid rgba(99, 102, 241, 0.2);
}

.card-light {
    background: linear-gradient(145deg, #f5f5fa, #ffffff);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card:hover {
    border: 1px solid rgba(99, 102, 241, 0.4);
}

.card-title {
    font-size: 12px;
    font-weight: 600;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.card-value {
    font-size: 18px;
    font-weight: 600;
    color: #e5e7eb;
}

.card-subtitle {
    font-size: 11px;
    color: #6b7280;
}

progressbar > trough {
    background: #1f2937;
    border-radius: 6px;
    min-height: 6px;
}

progressbar > progress {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    border-radius: 6px;
}

.notebook tab {
    background: transparent;
    color: #6b7280;
    padding: 12px 24px;
    border-radius: 12px 12px 0 0;
    font-weight: 600;
    font-size: 14px;
}

.notebook tab:checked {
    background: #1a1a2e;
    color: #ffffff;
    border-top: 2px solid #6366f1;
}

.notebook tab:hover:not(:checked) {
    background: rgba(99, 102, 241, 0.1);
    color: #9ca3af;
}

treeview {
    background: #16162a;
    color: #e5e7eb;
    border: 1px solid #1f2937;
    border-radius: 8px;
}

treeview header {
    background: #1a1a2e;
    color: #9ca3af;
    font-weight: 600;
    font-size: 12px;
}

treeview row:nth-child(odd) {
    background: rgba(255, 255, 255, 0.02);
}

treeview row:nth-child(even) {
    background: rgba(0, 0, 0, 0.1);
}

treeview row:hover {
    background: rgba(99, 102, 241, 0.2);
}

treeview row:selected {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: #ffffff;
}

treeview row:selected:hover {
    background: linear-gradient(90deg, #7c7ff2, #a78bfa);
    color: #ffffff;
}

treeview cell {
    color: #e5e7eb;
}

headerbar {
    background: linear-gradient(90deg, #1a1a2e, #16213e);
    border-bottom: 1px solid #1f2937;
    color: #ffffff;
}

button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #ffffff;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    font-weight: 600;
    font-size: 13px;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

button:hover {
    background: linear-gradient(135deg, #818cf8, #a78bfa);
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

button.danger {
    background: linear-gradient(135deg, #ef4444, #f87171);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

button.danger:hover {
    background: linear-gradient(135deg, #f87171, #fca5a5);
}

scrollbar > slider {
    background: #374151;
    border-radius: 6px;
}

scrollbar > slider:hover {
    background: #4b5563;
}

scrollbar > trough {
    background: #1f2937;
    border-radius: 6px;
}

.label-metric {
    color: #ffffff;
    font-weight: 700;
    font-size: 20px;
}

.label-title {
    color: #9ca3af;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.frame {
    background: #1a1a2e;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #1f2937;
}

scrolledwindow {
    border: none;
}

combobox {
    background: #1f2937;
    color: #e5e7eb;
    border-radius: 8px;
    padding: 8px;
}

combobox button {
    background: #1f2937;
}

entry {
    background: #1f2937;
    color: #e5e7eb;
    border-radius: 8px;
    border: 1px solid #374151;
}
"""


class PCResourceManager(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.pcresource.manager")
        self.monitor = SystemMonitor()
        self.cpu_history = []
        self.ram_history = []
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        display = Gdk.Display.get_default()
        if display is None:
            print("No display available")
            return

        self.setup_css()

        self.win = Gtk.ApplicationWindow(application=app)
        self.win.set_title("PC Resource Manager")
        self.win.set_default_size(1200, 800)

        self.header = Gtk.HeaderBar()
        self.header.set_title_widget(Gtk.Label(label="PC Resource Manager"))
        self.win.set_titlebar(self.header)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.win.set_child(self.main_box)

        self.create_notebook()
        self.start_monitoring()

        self.win.present()

    def setup_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def create_notebook(self):
        self.notebook = Gtk.Notebook()
        self.notebook.set_show_tabs(True)
        self.notebook.add_css_class("notebook")
        self.main_box.append(self.notebook)

        self.notebook.append_page(self.create_dashboard_view(), Gtk.Label(label="Dashboard"))
        self.notebook.append_page(self.create_process_view(), Gtk.Label(label="Processes"))
        self.notebook.append_page(self.create_disk_view(), Gtk.Label(label="Storage"))
        self.notebook.append_page(self.create_system_view(), Gtk.Label(label="System"))

    def create_dashboard_view(self):
        scroll = Gtk.ScrolledWindow()
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        container.set_margin_top(24)
        container.set_margin_bottom(24)
        container.set_margin_start(24)
        container.set_margin_end(24)

        cpu_section = self._create_section("CPU Usage")
        container.append(cpu_section)

        cpu_grid = Gtk.Grid()
        cpu_grid.set_column_spacing(16)
        cpu_grid.set_row_spacing(16)
        container.append(cpu_grid)

        self.cpu_graph = GraphWidget(max_points=60, color="#6366f1")
        self.cpu_graph.set_size_request(-1, 140)
        cpu_grid.attach(self.cpu_graph, 0, 0, 2, 1)

        self.cpu_cores_grid = Gtk.Grid()
        self.cpu_cores_grid.set_column_spacing(12)
        self.cpu_cores_grid.set_row_spacing(12)
        cpu_grid.attach(self.cpu_cores_grid, 0, 1, 1, 1)

        cpu_overall_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        cpu_overall_box.set_halign(Gtk.Align.CENTER)
        cpu_overall_box.set_valign(Gtk.Align.CENTER)

        self.cpu_overall_label = Gtk.Label(label="0%")
        self.cpu_overall_label.add_css_class("label-metric")
        self.cpu_overall_label.set_size_request(100, -1)

        self.cpu_cores_label = Gtk.Label(label="Total CPU")
        self.cpu_cores_label.add_css_class("label-title")

        cpu_overall_box.append(self.cpu_cores_label)
        cpu_overall_box.append(self.cpu_overall_label)
        cpu_grid.attach(cpu_overall_box, 1, 1, 1, 1)

        mem_section = self._create_section("Memory")
        container.append(mem_section)

        mem_grid = Gtk.Grid()
        mem_grid.set_column_spacing(16)
        mem_grid.set_row_spacing(16)
        container.append(mem_grid)

        self.ram_graph = GraphWidget(max_points=60, color="#10b981")
        self.ram_graph.set_size_request(-1, 120)
        mem_grid.attach(self.ram_graph, 0, 0, 1, 1)

        self.swap_graph = GraphWidget(max_points=60, color="#f59e0b")
        self.swap_graph.set_size_request(-1, 120)
        mem_grid.attach(self.swap_graph, 1, 0, 1, 1)

        self.ram_info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.ram_info_box.set_halign(Gtk.Align.CENTER)

        self.ram_info_label = Gtk.Label(label="0 / 0 GB")
        self.ram_info_label.add_css_class("label-metric")

        self.ram_percent_label = Gtk.Label(label="RAM Usage")
        self.ram_percent_label.add_css_class("label-title")

        self.ram_info_box.append(self.ram_percent_label)
        self.ram_info_box.append(self.ram_info_label)
        mem_grid.attach(self.ram_info_box, 2, 0, 1, 1)

        net_section = self._create_section("Network")
        container.append(net_section)

        net_grid = Gtk.Grid()
        net_grid.set_column_spacing(16)
        net_grid.set_row_spacing(16)
        container.append(net_grid)

        self.net_sent_graph = GraphWidget(max_points=60, color="#22c55e")
        self.net_sent_graph.set_size_request(-1, 100)
        net_grid.attach(self.net_sent_graph, 0, 0, 1, 1)

        self.net_recv_graph = GraphWidget(max_points=60, color="#3b82f6")
        self.net_recv_graph.set_size_request(-1, 100)
        net_grid.attach(self.net_recv_graph, 1, 0, 1, 1)

        self.net_info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.net_info_box.set_halign(Gtk.Align.CENTER)

        self.net_sent_label = Gtk.Label(label="↑ 0 B/s")
        self.net_sent_label.add_css_class("label-metric")

        self.net_recv_label = Gtk.Label(label="↓ 0 B/s")
        self.net_recv_label.add_css_class("label-metric")

        self.net_info_box.append(self.net_sent_label)
        self.net_info_box.append(self.net_recv_label)
        net_grid.attach(self.net_info_box, 2, 0, 1, 1)

        disk_section = self._create_section("Disk I/O")
        container.append(disk_section)

        disk_grid = Gtk.Grid()
        disk_grid.set_column_spacing(16)
        disk_grid.set_row_spacing(16)
        container.append(disk_grid)

        self.disk_read_graph = GraphWidget(max_points=60, color="#ec4899")
        self.disk_read_graph.set_size_request(-1, 100)
        disk_grid.attach(self.disk_read_graph, 0, 0, 1, 1)

        self.disk_write_graph = GraphWidget(max_points=60, color="#f97316")
        self.disk_write_graph.set_size_request(-1, 100)
        disk_grid.attach(self.disk_write_graph, 1, 0, 1, 1)

        self.disk_info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.disk_info_box.set_halign(Gtk.Align.CENTER)

        self.disk_read_label = Gtk.Label(label="R: 0 B/s")
        self.disk_read_label.add_css_class("label-metric")

        self.disk_write_label = Gtk.Label(label="W: 0 B/s")
        self.disk_write_label.add_css_class("label-metric")

        self.disk_info_box.append(self.disk_read_label)
        self.disk_info_box.append(self.disk_write_label)
        disk_grid.attach(self.disk_info_box, 2, 0, 1, 1)

        scroll.set_child(container)
        return scroll

    def _create_section(self, title):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        label = Gtk.Label(label=title)
        label.add_css_class("card-title")
        label.set_halign(Gtk.Align.START)
        box.append(label)

        return box

    def create_process_view(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(16)
        vbox.set_margin_bottom(16)
        vbox.set_margin_start(16)
        vbox.set_margin_end(16)

        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        toolbar.set_halign(Gtk.Align.CENTER)
        vbox.append(toolbar)

        sort_label = Gtk.Label(label="Sort by:")
        sort_label.add_css_class("card-title")
        toolbar.append(sort_label)

        self.sort_combo = Gtk.ComboBoxText()
        self.sort_combo.append("cpu", "CPU")
        self.sort_combo.append("memory", "Memory")
        self.sort_combo.append("name", "Name")
        self.sort_combo.append("pid", "PID")
        self.sort_combo.set_active_id("cpu")
        self.sort_combo.connect("changed", self.on_sort_changed)
        toolbar.append(self.sort_combo)

        refresh_btn = Gtk.Button(label="Refresh")
        refresh_btn.connect("clicked", self.refresh_process_list)
        toolbar.append(refresh_btn)

        self.selected_process_label = Gtk.Label(label="No process selected")
        self.selected_process_label.set_markup(
            "<span foreground='#22c55e'>No process selected</span>"
        )
        toolbar.append(self.selected_process_label)

        toolbar.append(Gtk.Label())

        self.kill_btn = Gtk.Button(label="Kill Process")
        self.kill_btn.add_css_class("danger")
        self.kill_btn.connect("clicked", self.on_kill_process)
        self.kill_btn.set_sensitive(False)
        toolbar.append(self.kill_btn)

        self.process_store = Gtk.ListStore.new(
            [
                int,
                str,
                str,
                float,
                float,
                str,
            ]
        )

        self.process_tree = Gtk.TreeView(model=self.process_store)
        self.process_tree.set_headers_visible(True)
        self.process_tree.set_hexpand(True)
        self.process_tree.set_vexpand(True)
        self.process_tree.add_css_class("process-tree")

        renderer = Gtk.CellRendererText()
        renderer.set_property("foreground", "#e5e7eb")

        columns = [
            ("PID", 80),
            ("Name", 280),
            ("User", 140),
            ("CPU %", 80),
            ("Memory %", 100),
            ("Status", 100),
        ]

        for i, (title, width) in enumerate(columns):
            col = Gtk.TreeViewColumn(title, renderer, text=i)
            col.set_title(title)
            col.set_fixed_width(width)
            col.set_expand(width == 280)
            col.set_min_width(60)
            self.process_tree.append_column(col)

        self.process_tree.get_selection().connect("changed", self.on_process_selected)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.process_tree)
        scrolled.set_vexpand(True)
        vbox.append(scrolled)

        return vbox

    def create_disk_view(self):
        scroll = Gtk.ScrolledWindow()
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        container.set_margin_top(16)
        container.set_margin_bottom(16)
        container.set_margin_start(16)
        container.set_margin_end(16)
        scroll.set_child(container)

        disk_section = self._create_section("Disk Usage")
        container.append(disk_section)

        self.disk_usage_grid = Gtk.Grid()
        self.disk_usage_grid.set_column_spacing(16)
        self.disk_usage_grid.set_row_spacing(16)
        container.append(self.disk_usage_grid)

        return scroll

    def create_system_view(self):
        scroll = Gtk.ScrolledWindow()
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        container.set_margin_top(16)
        container.set_margin_bottom(16)
        container.set_margin_start(16)
        container.set_margin_end(16)
        scroll.set_child(container)

        sys_card = Gtk.Frame()
        sys_card.add_css_class("card-light")
        container.append(sys_card)

        sys_inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        sys_inner_box.set_margin_start(20)
        sys_inner_box.set_margin_end(20)
        sys_inner_box.set_margin_top(20)
        sys_inner_box.set_margin_bottom(20)
        sys_card.set_child(sys_inner_box)

        sys_section = self._create_section("System Information")
        sys_section.set_margin_bottom(8)
        sys_inner_box.append(sys_section)

        self.sys_info_grid = Gtk.Grid()
        self.sys_info_grid.set_column_spacing(24)
        self.sys_info_grid.set_row_spacing(16)
        sys_inner_box.append(self.sys_info_grid)

        return scroll

    def start_monitoring(self):
        self.update_dashboard()
        self.update_process_list()
        self.update_disk_view()
        self.update_system_info()

        self.notebook.connect("switch-page", self.on_tab_switch)

        GLib.timeout_add(1000, self.update_all)

    def on_tab_switch(self, notebook, page, page_num):
        if page_num == 0:
            self.update_dashboard()
        elif page_num == 1:
            self.update_process_list()
        elif page_num == 2:
            self.update_disk_view()
        elif page_num == 3:
            self.update_system_info()

    def update_all(self):
        self.update_dashboard()
        return True

    def update_dashboard(self):
        cpu_overall = self.monitor.get_cpu_usage_overall()
        self.cpu_graph.add_value(cpu_overall)
        self.cpu_overall_label.set_text(f"{cpu_overall:.1f}%")

        cpu_cores = self.monitor.get_cpu_usage_per_core()

        for child in list(self.cpu_cores_grid.observe_children()):
            self.cpu_cores_grid.remove(child)

        for i, usage in enumerate(cpu_cores):
            frame = Gtk.Frame()
            frame.add_css_class("frame")
            frame.set_size_request(90, 80)

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            vbox.set_halign(Gtk.Align.CENTER)
            vbox.set_valign(Gtk.Align.CENTER)

            label = Gtk.Label(label=f"Core {i}")
            label.add_css_class("label-title")
            vbox.append(label)

            pct = Gtk.Label(label=f"{usage:.0f}%")
            pct.add_css_class("label-metric")
            pct.set_size_request(60, -1)
            vbox.append(pct)

            progress = Gtk.ProgressBar()
            progress.set_fraction(usage / 100)
            progress.set_show_text(False)
            progress.set_size_request(70, -1)
            vbox.append(progress)

            frame.set_child(vbox)
            self.cpu_cores_grid.attach(frame, i % 4, i // 4, 1, 1)

        ram = self.monitor.get_ram_usage()
        self.ram_graph.add_value(ram["percent"])
        self.ram_info_label.set_text(f"{format_bytes(ram['used'])} / {format_bytes(ram['total'])}")
        self.ram_percent_label.set_text(f"RAM {ram['percent']:.1f}%")

        swap = self.monitor.get_swap_memory()
        self.swap_graph.add_value(swap["percent"])

        net = self.monitor.get_network_io()
        self.net_sent_graph.add_value(net["sent_speed"])
        self.net_recv_graph.add_value(net["recv_speed"])
        self.net_sent_label.set_text(f"↑ {format_speed(net['sent_speed'])}")
        self.net_recv_label.set_text(f"↓ {format_speed(net['recv_speed'])}")

        disk_io = self.monitor.get_disk_io_stats()
        self.disk_read_graph.add_value(disk_io["read_speed"])
        self.disk_write_graph.add_value(disk_io["write_speed"])
        self.disk_read_label.set_text(f"R: {format_speed(disk_io['read_speed'])}")
        self.disk_write_label.set_text(f"W: {format_speed(disk_io['write_speed'])}")

    def update_process_list(self):
        sort_by = self.sort_combo.get_active_id() if self.sort_combo.get_active_id() else "cpu"
        processes = self.monitor.get_process_list(sort_by=sort_by, limit=200)

        self.process_store.clear()
        for proc in processes:
            self.process_store.append(
                [
                    proc["pid"],
                    proc["name"],
                    proc["username"],
                    proc["cpu_percent"],
                    proc["memory_percent"],
                    proc["status"],
                ]
            )

    def refresh_process_list(self, widget=None):
        self.update_process_list()

    def on_sort_changed(self, widget):
        self.update_process_list()

    def on_process_selected(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter:
            pid = model.get_value(treeiter, 0)
            name = model.get_value(treeiter, 1)
            self.selected_process_label.set_text(f"Selected: {name} (PID: {pid})")
            self.kill_btn.set_sensitive(True)
        else:
            self.selected_process_label.set_text("No process selected")
            self.kill_btn.set_sensitive(False)

    def on_kill_process(self, widget):
        model, treeiter = self.process_tree.get_selection().get_selected()
        if treeiter:
            pid = model.get_value(treeiter, 0)
            name = model.get_value(treeiter, 1)

            dialog = Gtk.MessageDialog(
                transient_for=self.win,
                modal=True,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.YES_NO,
                text=f"Kill Process '{name}' (PID: {pid})?",
                secondary_text="This may cause data loss. Are you sure?",
            )
            dialog.connect("response", self._confirm_kill, pid)
            dialog.present()

    def _confirm_kill(self, dialog, response, pid):
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            success = self.monitor.kill_process(pid)
            if success:
                self.refresh_process_list()

    def update_disk_view(self):
        for child in list(self.disk_usage_grid.observe_children()):
            self.disk_usage_grid.remove(child)

        partitions = self.monitor.get_all_disks()

        for i, part in enumerate(partitions):
            frame = Gtk.Frame()
            frame.add_css_class("card")
            frame.set_size_request(220, 120)

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

            name = Gtk.Label(label=f"{part['device']}")
            name.add_css_class("card-title")
            name.set_halign(Gtk.Align.START)
            vbox.append(name)

            mount = Gtk.Label(label=part["mountpoint"])
            mount.add_css_class("card-subtitle")
            mount.set_halign(Gtk.Align.START)
            vbox.append(mount)

            pct = Gtk.Label(label=f"{part['percent']:.1f}%")
            pct.add_css_class("label-metric")
            pct.set_halign(Gtk.Align.START)
            vbox.append(pct)

            progress = Gtk.ProgressBar()
            progress.set_fraction(part["percent"] / 100)
            progress.set_show_text(False)
            vbox.append(progress)

            info = Gtk.Label(label=f"{format_bytes(part['used'])} / {format_bytes(part['total'])}")
            info.add_css_class("card-subtitle")
            info.set_halign(Gtk.Align.START)
            vbox.append(info)

            frame.set_child(vbox)
            self.disk_usage_grid.attach(frame, i % 3, i // 3, 1, 1)

    def update_system_info(self):
        for child in list(self.sys_info_grid.observe_children()):
            self.sys_info_grid.remove(child)

        info = self.monitor.get_system_info()

        items = [
            ("Operating System", f"{info['os']} {info['release']}"),
            ("Version", info["version"]),
            ("Machine", info["machine"]),
            ("CPU Cores (Logical)", str(info["cpu_count"])),
            ("CPU Cores (Physical)", str(info["cpu_count_physical"])),
            ("Total Memory", format_bytes(info["total_memory"])),
        ]

        for i, (label, value) in enumerate(items):
            lbl = Gtk.Label(label=f"{label}:")
            lbl.set_markup(f"<span foreground='#000000' font_weight='bold'>{label}:</span>")
            lbl.set_halign(Gtk.Align.END)
            lbl.set_size_request(180, -1)
            self.sys_info_grid.attach(lbl, 0, i, 1, 1)

            val = Gtk.Label(label=value)
            val.set_markup(f"<span foreground='#000000'>{value}</span>")
            val.set_halign(Gtk.Align.START)
            self.sys_info_grid.attach(val, 1, i, 1, 1)


def main():
    app = PCResourceManager()
    app.run(None)


if __name__ == "__main__":
    main()
